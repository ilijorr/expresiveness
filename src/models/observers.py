from abc import ABC, abstractmethod
from typing import Any, Dict, List
from enum import Enum


class ModelEvent(Enum):
    """Types of events in the model layer"""
    NODE_ADDED = "node_added"
    NODE_REMOVED = "node_removed"
    NODE_UPDATED = "node_updated"
    EDGE_ADDED = "edge_added"
    EDGE_REMOVED = "edge_removed"
    EDGE_UPDATED = "edge_updated"
    GRAPH_CLEARED = "graph_cleared"
    GRAPH_LOADED = "graph_loaded"
    MODEL_CREATED = "model_created"
    MODEL_REMOVED = "model_removed"
    MODEL_SWITCHED = "model_switched"


class ModelObserver(ABC):
    """Base interface for model layer observers"""
    
    @abstractmethod
    def on_model_changed(self, event_type: ModelEvent, data: Dict[str, Any]) -> None:
        """
        Called when the model changes

        Args:
            event_type: Event type
            data: Event data (node/edge objects, old/new state, etc.)
        """
        pass


class ModelSubject(ABC):
    """Interface for subjects that can have observers"""
    
    def __init__(self):
        self._observers: List[ModelObserver] = []
    
    def attach_observer(self, observer: ModelObserver) -> None:
        """Adds observer"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach_observer(self, observer: ModelObserver) -> None:
        """Removes observer"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify_observers(self, event_type: ModelEvent, data: Dict[str, Any]) -> None:
        """Notifies all observers about the change"""
        for observer in self._observers:
            observer.on_model_changed(event_type, data)


class ViewObserver(ABC):
    """Interface for view layer observers (for web notifications)"""
    
    @abstractmethod
    def on_view_action(self, action: str, parameters: Dict[str, Any]) -> None:
        """
        Called when the user performs an action in the view layer

        Args:
            action: Action name (zoom, filter, select, etc.)
            parameters: Action parameters
        """
        pass


class ControllerSubject(ABC):
    """Base controller that can receive view actions"""
    
    def __init__(self):
        self._view_observers: List[ViewObserver] = []
    
    def attach_view_observer(self, observer: ViewObserver) -> None:
        """Adds view observer"""
        if observer not in self._view_observers:
            self._view_observers.append(observer)
    
    def detach_view_observer(self, observer: ViewObserver) -> None:
        """Removes view observer"""
        if observer in self._view_observers:
            self._view_observers.remove(observer)
    
    def notify_view_observers(self, action: str, parameters: Dict[str, Any]) -> None:
        """Notifies view observers about the action"""
        for observer in self._view_observers:
            observer.on_view_action(action, parameters)


# Concrete observer for logging (useful for debugging)
class LoggingObserver(ModelObserver):
    """Observer that logs all model changes"""
    
    def __init__(self, logger_name: str = "src"):
        import logging
        self.logger = logging.getLogger(logger_name)
    
    def on_model_changed(self, event_type: ModelEvent, data: Dict[str, Any]) -> None:
        """Logs model changes"""
        self.logger.info(f"Model event: {event_type.value}, data: {data}")


# Utility functions for creating observer connections
def connect_model_to_controller(model: ModelSubject, controller: ModelObserver) -> None:
    """Connects model with controller"""
    model.attach_observer(controller)


def connect_view_to_controller(view: ControllerSubject, controller: ViewObserver) -> None:
    """Connects view with controller"""
    view.attach_view_observer(controller)