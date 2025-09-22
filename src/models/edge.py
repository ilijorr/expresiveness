"""
Edge model for graph connections
"""

import uuid
from typing import Any, Dict, Optional
from .node import Node


class Edge:
    """Graph edge connecting two nodes."""

    def __init__(
        self,
        source: Node,
        target: Node,
        edge_type: str = "default",
        directed: bool = True,
        label: str = "",
        properties: Optional[Dict[str, Any]] = None
    ):
        self.id = str(uuid.uuid4())
        self.source = source
        self.target = target
        self.edge_type = edge_type
        self.directed = directed
        self.label = label
        self.properties = properties or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert edge to dictionary."""
        return {
            "id": self.id,
            "source_id": self.source.id,
            "target_id": self.target.id,
            "edge_type": self.edge_type,
            "directed": self.directed,
            "label": self.label,
            "properties": self.properties.copy()
        }

    def __repr__(self) -> str:
        arrow = "->" if self.directed else "--"
        return f"Edge({self.source.label} {arrow} {self.target.label})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Edge):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)