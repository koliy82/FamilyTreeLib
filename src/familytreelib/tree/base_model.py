from abc import ABC, abstractmethod
from typing import Optional, Tuple, TypeVar

from pymongo.collection import Collection

from familytreelib.pymongo.family import Family
from familytreelib.pymongo.user import User

T = TypeVar('T', bound='BaseFamilyTree')
class BaseFamilyTree(ABC):
    user_id: int
    brak: Optional['Family'] = None
    first: Optional['User'] = None
    second: Optional['User'] = None
    next: Optional['BaseFamilyTree'] = None

    def __init__(self, user_id: int, *args, **kwargs):
        print(f"Process user_id: {user_id}")
        self.user_id = user_id
        for key, value in kwargs.items():
            setattr(self, key, value)

    def process_data(self, coll: Collection, max_duplicate, is_repeatable_map=None):
        pipeline = [
            {
                '$match': {
                    '$or': [
                        {'first_user_id': self.user_id},
                        {'second_user_id': self.user_id}
                    ]
                }
            },
            {'$limit': 1},
            {'$lookup': {
                'from': 'users',
                'localField': 'first_user_id',
                'foreignField': 'id',
                'as': 'first'
            }},
            {'$lookup': {
                'from': 'users',
                'localField': 'second_user_id',
                'foreignField': 'id',
                'as': 'second'
            }},
            {'$unwind': {'path': '$first', 'preserveNullAndEmptyArrays': True}},
            {'$unwind': {'path': '$second', 'preserveNullAndEmptyArrays': True}},
        ]
        results = coll.aggregate(pipeline)
        for result in results:
            self.brak = Family.from_mongo(result)
            if self.brak is None:
                continue
            if 'first' in result:
                first_data = result['first']
                if first_data:
                    self.first = User.from_mongo(first_data)
            if 'second' in result:
                second_data = result['second']
                if second_data:
                    self.second = User.from_mongo(second_data)
            if self.brak and self.brak.baby_user_id:
                if is_repeatable_map is None:
                    is_repeatable_map = {self.brak.first_user_id: 0, self.brak.second_user_id: 0}
                is_duplicate = self.is_duplicate_user(self.brak.baby_user_id, max_duplicate, is_repeatable_map)
                if not is_duplicate:
                    self.next = self.__class__(self.brak.baby_user_id)
                    self.next.process_data(coll, max_duplicate, is_repeatable_map)

    def is_duplicate_user(self, user_id, max_duplicate, is_repeatable_map):
        if user_id not in is_repeatable_map:
            is_duplicate = False
            is_repeatable_map[self.brak.baby_user_id] = 0
        else:
            duplicate_count = is_repeatable_map[user_id]
            is_duplicate = duplicate_count >= max_duplicate
            is_repeatable_map[user_id] = duplicate_count + 1
            print(f"duplicate [{user_id}]: {duplicate_count}/{max_duplicate} = {is_duplicate}")
        return is_duplicate



    def root_data(self, unknown_string: str) -> Tuple[str, int]:
        if self.user_id == self.brak.first_user_id:
            if self.first:
                return f"{self.first.first_name} {self.first.last_name}", self.brak.first_user_id
            else:
                return unknown_string, self.brak.first_user_id
        else:
            if self.second:
                return f"{self.second.first_name} {self.second.last_name}", self.brak.second_user_id
            else:
                return unknown_string, self.brak.second_user_id

    def partner_data(self, unknown_string) -> Tuple[str, int]:
        if self.user_id != self.brak.first_user_id:
            if self.first:
                return f"{self.first.first_name} {self.first.last_name}", self.brak.first_user_id
            else:
                return unknown_string, self.brak.first_user_id
        else:
            if self.second:
                return f"{self.second.first_name} {self.second.last_name}", self.brak.second_user_id
            else:
                return unknown_string, self.brak.second_user_id

    @abstractmethod
    def empty_node(self):
        """
        Abstract method to add empty node to the tree if data is missing
        """
        pass

    # ROOT + PARTNER = PAIR -> BABY + PARTNER = NEXT PAIR...
    @abstractmethod
    def add_pair(self, tree: T, root_data: tuple[str, int | None], partner_data: tuple[str, int], root_prefix:str, root_suffix:str, partner_prefix:str, partner_suffix:str):
        """
        Abstract method to add pair to the tree
        :param tree:
        :param root_data:
        :param partner_data:
        :param partner_suffix:
        :param partner_prefix:
        :param root_suffix:
        :param root_prefix:
        :return:
        """
        raise NotImplementedError

    def root_node(self):
        """
        Add root pair to the tree
        """
        if self.brak is None:
            self.empty_node()
            return
        root_name, _ = self.root_data(getattr(self, "unknown", "?"))
        partner_data = self.partner_data(getattr(self, "unknown", "?"))
        root_prefix = getattr(self, "root_prefix", '')
        root_suffix = getattr(self, "root_suffix", '')
        return self.add_pair(self, (root_name, None), partner_data, root_prefix, root_suffix, root_prefix, root_suffix)


    def recursive_nodes(self, tree: T, root_id: int):
        """
        Abstract method to add all nodes to the tree recursively
        Should be implemented add_node method
        :param tree:
        :param root_id:
        """
        if tree is None or tree.brak is None:
           return
        first_name, _  = tree.root_data(getattr(self, "unknown", "?"))
        partner_data = tree.partner_data(getattr(self, "unknown", "?"))
        root_prefix = getattr(self, "kid_prefix", '')
        root_suffix = getattr(self, "kid_suffix", '')
        partner_prefix = getattr(self, "partner_prefix", '')
        partner_suffix = getattr(self, "partner_suffix", '')
        self.add_pair(tree, (first_name, root_id), partner_data, root_prefix, root_suffix, partner_prefix, partner_suffix)
        if tree.next:
           self.recursive_nodes(tree.next, tree.user_id)

    def build_tree(self, coll: Collection):
        self.process_data(coll, int(getattr(self, "max_duplicate", 0)))
        self.root_node()
        if self.next:
            self.recursive_nodes(self.next, root_id=self.user_id)