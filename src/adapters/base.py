"""
Basic adapter interfaces and registry
"""

from abc import ABC, abstractmethod
from typing import Dict, List
from ..models.graph import Graph


class ISyntaxAdapter(ABC):
    """Interface for syntax adapters"""

    @abstractmethod
    def get_syntax_name(self) -> str:
        """Get syntax name"""
        pass

    @abstractmethod
    def get_version(self) -> str:
        """Get adapter version"""
        pass

    @abstractmethod
    def parse(self, input_data: str) -> Graph:
        """Parse input data to graph"""
        pass

    @abstractmethod
    def export(self, graph: Graph) -> str:
        """Export graph to string format"""
        pass

    @abstractmethod
    def validate(self, input_data: str) -> bool:
        """Validate input data"""
        pass


class SyntaxRegistry:
    """Simple registry for syntax adapters"""

    def __init__(self):
        self._adapters: Dict[str, ISyntaxAdapter] = {}
        self._register_default_adapters()

    def register_adapter(self, adapter: ISyntaxAdapter):
        """Register syntax adapter"""
        self._adapters[adapter.get_syntax_name()] = adapter

    def get_adapter(self, syntax_name: str) -> ISyntaxAdapter:
        """Get adapter by syntax name"""
        if syntax_name not in self._adapters:
            raise ValueError(f"Unknown syntax: {syntax_name}")
        return self._adapters[syntax_name]

    def get_available_syntaxes(self) -> List[str]:
        """Get list of available syntax names"""
        return list(self._adapters.keys())

    def _register_default_adapters(self):
        """Register default adapters"""
        try:
            from .syntaxes.basic_graph import BasicGraphAdapter
            self.register_adapter(BasicGraphAdapter())
        except ImportError:
            pass

        try:
            from .syntaxes.hierarchy import HierarchyAdapter
            self.register_adapter(HierarchyAdapter())
        except ImportError:
            pass

        try:
            from .syntaxes.process import ProcessAdapter
            self.register_adapter(ProcessAdapter())
        except ImportError:
            pass