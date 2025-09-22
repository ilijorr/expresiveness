"""
Position model for graph nodes
"""

from typing import Dict, Any


class Position:
    """Represents a 2D position with x and y coordinates."""

    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self.x = x
        self.y = y

    def to_dict(self) -> Dict[str, float]:
        """Convert position to dictionary."""
        return {"x": self.x, "y": self.y}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Position':
        """Create position from dictionary."""
        return cls(x=data.get("x", 0.0), y=data.get("y", 0.0))

    def __repr__(self) -> str:
        return f"Position(x={self.x}, y={self.y})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Position):
            return False
        return self.x == other.x and self.y == other.y