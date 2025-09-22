"""
Graph model
"""

import uuid
from typing import Any, Dict, List, Optional
from .node import Node
from .edge import Edge


class GraphValidationError(Exception):
    """exception raised when graph validation fails."""
    pass


class Graph:
    """graph structure with nodes and edges."""

    def __init__(self, name: str = "Graph", directed: bool = True):
        self.id = str(uuid.uuid4())
        self.name = name
        self.directed = directed
        self.nodes: List[Node] = []
        self.edges: List[Edge] = []
        self.properties: Dict[str, Any] = {}

    def add_node(self, node: Node) -> None:
        """add a node to the graph."""
        if node not in self.nodes:
            self.nodes.append(node)

    def remove_node(self, node: Node) -> None:
        """remove a node and all its edges."""
        if node in self.nodes:
            # Remove all edges connected to this node
            self.edges = [edge for edge in self.edges
                         if edge.source != node and edge.target != node]
            self.nodes.remove(node)

    def add_edge(self, edge: Edge) -> None:
        """add an edge to the graph."""
        # Ensure both nodes are in the graph
        if edge.source not in self.nodes:
            self.add_node(edge.source)
        if edge.target not in self.nodes:
            self.add_node(edge.target)

        if edge not in self.edges:
            self.edges.append(edge)

    def remove_edge(self, edge: Edge) -> None:
        """remove an edge from the graph."""
        if edge in self.edges:
            self.edges.remove(edge)

    def get_node_by_id(self, node_id: str) -> Optional[Node]:
        """get node by ID."""
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None

    def get_neighbors(self, node: Node) -> List[Node]:
        """get all neighboring nodes."""
        neighbors = []
        for edge in self.edges:
            if edge.source == node:
                neighbors.append(edge.target)
            elif not self.directed and edge.target == node:
                neighbors.append(edge.source)
        return neighbors

    def node_count(self) -> int:
        """get number of nodes."""
        return len(self.nodes)

    def edge_count(self) -> int:
        """get number of edges."""
        return len(self.edges)

    def clear(self) -> None:
        """clear all nodes and edges."""
        self.nodes.clear()
        self.edges.clear()

    def to_dict(self) -> Dict[str, Any]:
        """convert graph to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "directed": self.directed,
            "nodes": [node.to_dict() for node in self.nodes],
            "edges": [edge.to_dict() for edge in self.edges],
            "properties": self.properties.copy()
        }

    def __repr__(self) -> str:
        return f"Graph(name='{self.name}', nodes={len(self.nodes)}, edges={len(self.edges)})"


class GraphBuilder:
    """builder pattern for creating graphs."""

    def __init__(self):
        self.graph = Graph()

    def set_name(self, name: str) -> 'GraphBuilder':
        """set graph name."""
        self.graph.name = name
        return self

    def set_directed(self, directed: bool) -> 'GraphBuilder':
        """set if graph is directed."""
        self.graph.directed = directed
        return self

    def add_node(self, label: str, node_type: str = "default", **kwargs) -> 'GraphBuilder':
        """add a node to the graph."""
        node = Node(label=label, node_type=node_type, properties=kwargs)
        self.graph.add_node(node)
        return self

    def add_edge(self, source_label: str, target_label: str, edge_type: str = "default") -> 'GraphBuilder':
        """add an edge between nodes with given labels."""
        source = next((n for n in self.graph.nodes if n.label == source_label), None)
        target = next((n for n in self.graph.nodes if n.label == target_label), None)

        if source and target:
            edge = Edge(source=source, target=target, edge_type=edge_type)
            self.graph.add_edge(edge)

        return self

    def build(self) -> Graph:
        """build and return the graph."""
        return self.graph
