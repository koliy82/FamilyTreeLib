from io import BytesIO

from familytreelib.utils.temp_file import TempFile
from familytreelib.tree.base_model import BaseFamilyTree, T
import networkx
from networkx import DiGraph
import matplotlib.pyplot as plt

class NetworkxLib(BaseFamilyTree):

    def __new__(cls, *args, **kwargs):
        cls.graph = DiGraph()
        return super().__new__(cls)

    def empty_node(self):
        self.graph.add_node(self.user_id, name="Empty")
        pass

    def add_pair(self, tree: T, root_data: tuple[str, int | None], partner_data: tuple[str, int], root_prefix:str, root_suffix:str, partner_prefix:str, partner_suffix:str):
        root_name, root_id = root_data
        partner_name, partner_id = partner_data
        self.graph.add_node(tree.user_id, name=root_name)
        self.graph.add_node(partner_id, name=partner_name)
        self.graph.add_edge(tree.user_id, partner_id)
        if root_id is not None:
            self.graph.add_edge(root_id, tree.user_id)

    def render(self, prog="dot"):
        labels = networkx.get_node_attributes(self.graph, 'name')
        pos = networkx.nx_agraph.graphviz_layout(self.graph, prog=prog, args="")
        networkx.draw(
            self.graph, pos, node_size=20, alpha=0.5, node_color="blue",
            with_labels=True, labels=labels, arrows=True,
            width=2, font_size=10, font_color="black", linewidths=1.0, node_shape="s",
            # font_family=['Sawasdee', 'Gentium Book Basic', 'FreeMono', ]
        )
        plt.axis("equal")

        with TempFile(suffix=".png") as file:
            plt.savefig(file.path, format='png')
            img_stream = BytesIO(file.read())
            img_stream.seek(0)
            plt.close()
        return img_stream