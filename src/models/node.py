"""
Node model for graph structures
"""

import uuid
from typing import Any, Dict, Optional
from .position import Position


class Node:
    """Graph node with properties and position."""

    def __init__(
        self,
        label: str,
        node_type: str = "default",
        properties: Optional[Dict[str, Any]] = None,
        position: Optional[Position] = None
    ):
        self.id = str(uuid.uuid4())
        self.label = label
        self.node_type = node_type
        self.properties = properties or {}
        self.position = position or Position()

    def to_dict(self) -> Dict[str, Any]:
        """Convert node to dictionary."""
        return {
            "id": self.id,
            "label": self.label,
            "node_type": self.node_type,
            "properties": self.properties.copy(),
            "position": self.position.to_dict()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Node':
        """Create node from dictionary."""
        node = cls(
            label=data["label"],
            node_type=data.get("node_type", "default"),
            properties=data.get("properties", {}),
            position=Position.from_dict(data.get("position", {}))
        )
        node.id = data.get("id", node.id)
        return node

    def __repr__(self) -> str:
        return f"Node(id={self.id}, label='{self.label}', type='{self.node_type}')"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Node):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)