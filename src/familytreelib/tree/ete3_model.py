from io import BytesIO

import ete3
from ete3 import Tree
from ete3.treeview import faces

from familytreelib.utils.temp_file import TempFile
from familytreelib.tree.base_model import BaseFamilyTree, T


class Ete3Lib(BaseFamilyTree):

    def __new__(cls, *args, **kwargs):
        cls.tree = Tree()
        return super().__new__(cls)

    def empty_node(self):
        self.tree.add_child(name="Empty")
        pass

    def add_pair(self, tree: T, root_data: tuple[str, int | None], partner_data: tuple[str, int], root_prefix:str, root_suffix:str, partner_prefix:str, partner_suffix:str):
        root_name, root_id = root_data
        partner_name, partner_id = partner_data
        if root_id is None:
            root_node = self.tree.add_child(name=f"{root_prefix}{root_name}{root_suffix}")
        else:
            root_node = getattr(self, str(root_id)).add_child(name=f"👼 {root_name}")
        _ = root_node.add_child(name=f"{partner_prefix}{partner_name}{partner_suffix}")
        root_node.add_face(ete3.AttrFace("name"), column=0, position="branch-top")
        setattr(self, str(tree.user_id), root_node)

    def render(self):
        style = ete3.TreeStyle()
        style.title.add_face(faces.TextFace(f"🤔Семейное древо", fsize=20), column=0)
        style.show_leaf_name = True
        style.show_scale = False

        with TempFile(suffix=".png") as file:
            self.tree.render(file.path, units="px", tree_style=style)
            img_stream = BytesIO(file.read())
            img_stream.seek(0)
        return img_stream