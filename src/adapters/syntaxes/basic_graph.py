"""
Basic graph syntax adapter
"""

from ..base import ISyntaxAdapter
from ...models.graph import Graph, Node, Edge


class BasicGraphAdapter(ISyntaxAdapter):
    """Basic graph syntax adapter"""

    def get_syntax_name(self) -> str:
        return "basic_graph"

    def get_version(self) -> str:
        return "1.0.0"

    def parse(self, input_data: str) -> Graph:
        """Parse basic graph format: node1 -> node2"""
        graph = Graph(name="Basic Graph", directed=True)

        lines = input_data.strip().split('\n')
        for line in lines:
            line = line.strip()
            if '->' in line:
                parts = line.split('->')
                if len(parts) == 2:
                    source_name = parts[0].strip()
                    target_name = parts[1].strip()

                    # Create or get nodes
                    source = self._get_or_create_node(graph, source_name)
                    target = self._get_or_create_node(graph, target_name)

                    # Create edge
                    edge = Edge(
                        source=source,
                        target=target,
                        edge_type="basic",
                        directed=True
                    )
                    graph.add_edge(edge)

        return graph

    def _get_or_create_node(self, graph: Graph, name: str) -> Node:
        """Get existing node or create new one"""
        for node in graph.nodes:
            if node.label == name:
                return node

        node = Node(
            label=name,
            node_type="basic",
            properties={"name": name}
        )
        graph.add_node(node)
        return node

    def export(self, graph: Graph) -> str:
        """Export graph to basic format"""
        lines = []
        for edge in graph.edges:
            lines.append(f"{edge.source.label} -> {edge.target.label}")
        return '\n'.join(lines)

    def validate(self, input_data: str) -> bool:
        """Validate basic graph syntax"""
        try:
            lines = input_data.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line and '->' not in line:
                    return False
            return True
        except:
            return False