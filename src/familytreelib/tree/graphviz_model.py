from io import BytesIO

from graphviz import Digraph

from familytreelib.tree.base_model import BaseFamilyTree, T


class GraphvizLib(BaseFamilyTree):

    def __new__(cls, *args, **kwargs):
        graph = Digraph(comment="Family Tree",
                    node_attr={'color': 'lightblue2', 'style': 'filled', 'fontname':"Roboto, Noto Color Emoji"}
                )
        graph.attr(bgcolor='purple:pink', label='aboba', fontcolor='white')
        cls.graph = graph
        return super().__new__(cls)

    def empty_node(self):
        self.graph.node("0", "Empty")
        pass

    def add_pair(self, tree: T, root_data: tuple[str, int | None], partner_data: tuple[str, int], root_prefix:str, root_suffix:str, partner_prefix:str, partner_suffix:str):
        root_name, root_id = root_data
        partner_name, partner_id = partner_data
        self.graph.node(str(tree.user_id), f"{root_prefix}👶{root_name}{root_suffix}")
        self.graph.node(str(partner_id), f"{partner_prefix}👶{partner_name}{partner_suffix}", fontname="Roboto, Noto Color Emoji", charset="UTF-8")
        print(f"{root_prefix}{root_name}{root_suffix}")
        print(f"{partner_prefix}{partner_name}{partner_suffix}")
        if self.user_id == tree.user_id:
            self.graph.edge(str(self.user_id), str(partner_id), constraint="false", label='♥️')
        else:
            self.graph.edge(str(root_id), str(tree.user_id), label='♥️')
            self.graph.edge(str(tree.user_id), str(partner_id))

    def render(self):
        image_stream = BytesIO(self.graph.pipe(format="png"))
        image_stream.seek(0)
        return image_stream