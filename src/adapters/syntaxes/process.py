"""
Process diagram syntax adapter
"""

from ..base import ISyntaxAdapter
from ...models.graph import Graph, Node, Edge


class ProcessAdapter(ISyntaxAdapter):
    """Process diagram adapter"""

    def __init__(self):
        self.name = "process"
        self.version = "1.0.0"

    def get_syntax_name(self) -> str:
        return self.name

    def get_version(self) -> str:
        return self.version

    def parse(self, input_data: str) -> Graph:
        """Parse process diagram from text"""
        graph = Graph(name="Process Diagram", directed=True)

        lines = input_data.strip().split('\n')
        for line in lines:
            line = line.strip()
            if '->' in line:
                # Process step relationship
                parts = line.split('->')
                if len(parts) == 2:
                    source_name = parts[0].strip()
                    target_name = parts[1].strip()

                    # Create or get nodes
                    source = self._get_or_create_node(graph, source_name, "process_step")
                    target = self._get_or_create_node(graph, target_name, "process_step")

                    # Create edge
                    edge = Edge(
                        source=source,
                        target=target,
                        edge_type="process_flow",
                        directed=True
                    )
                    graph.add_edge(edge)

        return graph

    def _get_or_create_node(self, graph: Graph, name: str, node_type: str) -> Node:
        """Get existing node or create new one"""
        for node in graph.nodes:
            if node.label == name:
                return node

        node = Node(
            label=name,
            node_type=node_type,
            properties={"name": name}
        )
        graph.add_node(node)
        return node

    def export(self, graph: Graph) -> str:
        """Export graph to process diagram text"""
        lines = []
        for edge in graph.edges:
            lines.append(f"{edge.source.label} -> {edge.target.label}")
        return '\n'.join(lines)

    def validate(self, input_data: str) -> bool:
        """Validate process diagram syntax"""
        try:
            lines = input_data.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line and '->' not in line:
                    return False
            return True
        except:
            return False