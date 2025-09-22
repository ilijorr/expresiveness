"""
Hierarchy syntax adapter
"""

from ..base import ISyntaxAdapter
from ...models.graph import Graph, Node, Edge


class HierarchyAdapter(ISyntaxAdapter):
    """Hierarchy syntax adapter for tree structures"""

    def get_syntax_name(self) -> str:
        return "hierarchy"

    def get_version(self) -> str:
        return "1.0.0"

    def parse(self, input_data: str) -> Graph:
        """Parse hierarchy format using indentation"""
        graph = Graph(name="Hierarchy", directed=True)
        node_stack = []  # Stack to track parent nodes

        lines = input_data.strip().split('\n')
        for line in lines:
            if not line.strip():
                continue

            # Calculate indentation level
            indent_level = (len(line) - len(line.lstrip())) // 2
            node_name = line.strip()

            # Create node
            node = Node(
                label=node_name,
                node_type="hierarchy_node",
                properties={"level": indent_level, "name": node_name}
            )
            graph.add_node(node)

            # Adjust stack to current level
            while len(node_stack) > indent_level:
                node_stack.pop()

            # Add edge from parent if exists
            if node_stack:
                parent = node_stack[-1]
                edge = Edge(
                    source=parent,
                    target=node,
                    edge_type="parent_child",
                    directed=True
                )
                graph.add_edge(edge)

            # Add to stack
            node_stack.append(node)

        return graph

    def export(self, graph: Graph) -> str:
        """Export graph to hierarchy format"""
        # Find root nodes (no incoming edges)
        root_nodes = []
        for node in graph.nodes:
            has_parent = any(edge.target == node for edge in graph.edges)
            if not has_parent:
                root_nodes.append(node)

        lines = []
        for root in root_nodes:
            self._export_node_hierarchy(root, graph, lines, 0)

        return '\n'.join(lines)

    def _export_node_hierarchy(self, node: Node, graph: Graph, lines: list, level: int):
        """Recursively export node hierarchy"""
        indent = "  " * level
        lines.append(f"{indent}{node.label}")

        # Find children
        children = []
        for edge in graph.edges:
            if edge.source == node:
                children.append(edge.target)

        for child in children:
            self._export_node_hierarchy(child, graph, lines, level + 1)

    def validate(self, input_data: str) -> bool:
        """Validate hierarchy syntax"""
        try:
            lines = input_data.strip().split('\n')
            prev_level = -1

            for line in lines:
                if not line.strip():
                    continue

                indent_level = (len(line) - len(line.lstrip())) // 2

                # Level can increase by at most 1
                if indent_level > prev_level + 1:
                    return False

                prev_level = indent_level

            return True
        except:
            return False