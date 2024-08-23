from io import BytesIO

from igraph import Graph, plot

from familytreelib.utils.temp_file import TempFile
from familytreelib.tree.base_model import BaseFamilyTree, T

class IgraphLib(BaseFamilyTree):

    def __new__(cls, *args, **kwargs):
        cls.graph = Graph(directed=True)
        return super().__new__(cls)

    def empty_node(self):
        self.graph.add_vertex(name="0", label="Empty")
        pass

    def add_pair(self, tree: T, root_data: tuple[str, int | None], partner_data: tuple[str, int], root_prefix:str, root_suffix:str, partner_prefix:str, partner_suffix:str):
        root_name, root_id = root_data
        partner_name, partner_id = partner_data
        self.graph.add_vertex(name=str(tree.user_id), label=f"{root_prefix}{root_name}{root_suffix}")
        self.graph.add_vertex(name=str(partner_id), label=f"{partner_prefix}{partner_name}{partner_suffix}")
        if self.user_id == tree.user_id:
            self.graph.add_edge(str(self.user_id), str(partner_id), label='♥️')
        else:
            self.graph.add_edge(str(root_id), str(tree.user_id), label='♥️')
            self.graph.add_edge(str(tree.user_id), str(partner_id))

    def render(self, visual_style: dict | None = None):
        layout = self.graph.layout_reingold_tilford(root=[0])
        if visual_style is None:
            visual_style = {
                "vertex_size": 30,
                "margin": 40,
                "layout": layout,
                "vertex_color": "lightblue",
                "vertex_label_dist": -2.25,
                "edge_width": 2
            }
        else:
            visual_style["layout"] = layout
        with TempFile(suffix=".png") as file:
            plot(self.graph, target=file.path, **visual_style)
            img_stream = BytesIO(file.read())
            img_stream.seek(0)
            return img_stream
