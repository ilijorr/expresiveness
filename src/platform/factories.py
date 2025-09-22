"""
GraphFactory for ExpresiVeNess
"""

import uuid
from typing import Any
from ..models.graph import Graph, Node, Edge
from ..models.observers import ModelSubject, ModelEvent


class GraphFactory(ModelSubject):
    """Graph factory"""

    def __init__(self, factory_name: str):
        super().__init__()
        self.factory_name = factory_name

    def create_graph(self, graph_type: str = "default", **kwargs: Any) -> Graph:
        """Create a new graph"""
        graph_id = kwargs.get('id', str(uuid.uuid4()))
        graph_name = kwargs.get('name', f"{graph_type} graph")

        graph = Graph(name=graph_name, directed=True)
        graph.id = graph_id

        # Add some default nodes for demonstration
        if graph_type == "default":
            node1 = Node(label="Node A", node_type="default")
            node2 = Node(label="Node B", node_type="default")
            edge = Edge(source=node1, target=node2, edge_type="default")

            graph.add_node(node1)
            graph.add_node(node2)
            graph.add_edge(edge)

        self.notify_observers(ModelEvent.GRAPH_LOADED, {
            'graph_id': graph_id,
            'graph': graph
        })

        return graph

    def create_node(self, node_type: str = "default", **kwargs: Any) -> Node:
        """Create a new node"""
        node = Node(
            label=kwargs.get('label', 'New Node'),
            node_type=node_type,
            properties=kwargs.get('properties', {})
        )
        return node

    def create_edge(self, source: Node, target: Node, edge_type: str = "default", **kwargs: Any) -> Edge:
        """Create a new edge"""
        edge = Edge(
            source=source,
            target=target,
            edge_type=edge_type,
            directed=kwargs.get('directed', True),
            label=kwargs.get('label', ''),
            properties=kwargs.get('properties', {})
        )
        return edge

    def get_supported_node_types(self) -> list:
        """Get supported node types"""
        return ["default", "process", "hierarchy"]

    def has_node_type(self, node_type: str) -> bool:
        """Check if node type is supported"""
        return node_type in self.get_supported_node_types()

    def get_supported_edge_types(self) -> list:
        """Get supported edge types"""
        return ["default", "process_flow", "parent_child"]

    def has_edge_type(self, edge_type: str) -> bool:
        """Check if edge type is supported"""
        return edge_type in self.get_supported_edge_types()

    def get_factory_name(self) -> str:
        """Get factory name"""
        return self.factory_name