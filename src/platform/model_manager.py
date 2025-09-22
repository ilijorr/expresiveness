"""
ModelManager for ExpresiVeNess
"""

from typing import Dict, List, Optional, Any
from ..models.graph import Graph
from ..models.node import Node
from ..models.edge import Edge
from ..models.position import Position
from ..models.observers import ModelSubject, ModelEvent


class ModelManager(ModelSubject):
    """Model manager"""

    def __init__(self):
        super().__init__()
        self._models: Dict[str, Graph] = {}
        self._current_model_id: Optional[str] = None
        self._initialize_sample_data()

    def add_model(self, graph: Graph) -> str:
        """Add a model to the manager"""
        model_id = graph.id if hasattr(graph, 'id') and graph.id else f"model_{len(self._models)}"
        if not hasattr(graph, 'id'):
            graph.id = model_id

        self._models[model_id] = graph
        self._current_model_id = model_id

        self.notify_observers(ModelEvent.MODEL_CREATED, {
            'model_id': model_id,
            'graph': graph
        })

        return model_id

    def get_model(self, model_id: str) -> Optional[Graph]:
        """Get a model by ID"""
        return self._models.get(model_id)

    def get_current_model(self) -> Optional[Graph]:
        """Get the current active model"""
        if self._current_model_id:
            return self._models.get(self._current_model_id)
        return None

    def list_models(self) -> List[str]:
        """List all model IDs"""
        return list(self._models.keys())

    def remove_model(self, model_id: str) -> bool:
        """Remove a model"""
        if model_id in self._models:
            del self._models[model_id]
            if self._current_model_id == model_id:
                self._current_model_id = None

            self.notify_observers(ModelEvent.MODEL_REMOVED, {
                'model_id': model_id
            })
            return True
        return False

    def set_current_model(self, model_id: str) -> bool:
        """Set the current active model"""
        if model_id in self._models:
            self._current_model_id = model_id
            self.notify_observers(ModelEvent.MODEL_SWITCHED, {
                'model_id': model_id
            })
            return True
        return False

    def _initialize_sample_data(self):
        """Initialize sample data for different syntax types"""
        # Create sample graphs for each syntax type
        basic_graph = self._create_basic_sample_graph()
        process_graph = self._create_process_sample_graph()
        hierarchy_graph = self._create_hierarchy_sample_graph()

        # Add them to the manager without notifications during init
        self._models["basic"] = basic_graph
        self._models["process"] = process_graph
        self._models["hierarchy"] = hierarchy_graph

        # Set basic as default
        self._current_model_id = "basic"

    def _create_basic_sample_graph(self) -> Graph:
        """Create a basic node-link graph sample"""
        graph = Graph(name="Basic Graph Example")
        graph.id = "basic"

        # Create nodes
        node1 = Node(label="Node A", node_type="basic", position=Position(100, 100))
        node2 = Node(label="Node B", node_type="basic", position=Position(300, 100))
        node3 = Node(label="Node C", node_type="basic", position=Position(200, 250))
        node4 = Node(label="Node D", node_type="basic", position=Position(400, 200))

        # Add nodes to graph
        graph.add_node(node1)
        graph.add_node(node2)
        graph.add_node(node3)
        graph.add_node(node4)

        # Create edges
        edge1 = Edge(source=node1, target=node2, label="connects to", edge_type="basic")
        edge2 = Edge(source=node1, target=node3, label="links to", edge_type="basic")
        edge3 = Edge(source=node2, target=node4, label="flows to", edge_type="basic")
        edge4 = Edge(source=node3, target=node4, label="merges with", edge_type="basic")

        # Add edges to graph
        graph.add_edge(edge1)
        graph.add_edge(edge2)
        graph.add_edge(edge3)
        graph.add_edge(edge4)

        return graph

    def _create_process_sample_graph(self) -> Graph:
        """Create a process workflow sample"""
        graph = Graph(name="Process Workflow Example")
        graph.id = "process"

        # Create process nodes
        start = Node(label="Start", node_type="start", position=Position(50, 150))
        task1 = Node(label="Review Request", node_type="task", position=Position(200, 150))
        decision = Node(label="Approve?", node_type="decision", position=Position(350, 150))
        task2 = Node(label="Process Request", node_type="task", position=Position(500, 100))
        task3 = Node(label="Reject Request", node_type="task", position=Position(500, 200))
        end1 = Node(label="End - Approved", node_type="end", position=Position(650, 100))
        end2 = Node(label="End - Rejected", node_type="end", position=Position(650, 200))

        # Add nodes
        for node in [start, task1, decision, task2, task3, end1, end2]:
            graph.add_node(node)

        # Create process flow edges
        graph.add_edge(Edge(source=start, target=task1, label="begin", edge_type="flow"))
        graph.add_edge(Edge(source=task1, target=decision, label="review complete", edge_type="flow"))
        graph.add_edge(Edge(source=decision, target=task2, label="yes", edge_type="decision"))
        graph.add_edge(Edge(source=decision, target=task3, label="no", edge_type="decision"))
        graph.add_edge(Edge(source=task2, target=end1, label="complete", edge_type="flow"))
        graph.add_edge(Edge(source=task3, target=end2, label="complete", edge_type="flow"))

        return graph

    def _create_hierarchy_sample_graph(self) -> Graph:
        """Create a hierarchical organization sample"""
        graph = Graph(name="Organization Hierarchy Example", directed=True)
        graph.id = "hierarchy"

        # Create hierarchy nodes
        ceo = Node(label="CEO", node_type="executive", position=Position(300, 50))
        cto = Node(label="CTO", node_type="director", position=Position(150, 150))
        cfo = Node(label="CFO", node_type="director", position=Position(450, 150))
        dev_lead = Node(label="Dev Lead", node_type="manager", position=Position(75, 250))
        qa_lead = Node(label="QA Lead", node_type="manager", position=Position(225, 250))
        finance_mgr = Node(label="Finance Mgr", node_type="manager", position=Position(450, 250))
        dev1 = Node(label="Developer 1", node_type="employee", position=Position(25, 350))
        dev2 = Node(label="Developer 2", node_type="employee", position=Position(125, 350))
        qa1 = Node(label="QA Engineer", node_type="employee", position=Position(225, 350))

        # Add nodes
        for node in [ceo, cto, cfo, dev_lead, qa_lead, finance_mgr, dev1, dev2, qa1]:
            graph.add_node(node)

        # Create hierarchy edges
        graph.add_edge(Edge(source=ceo, target=cto, label="reports to", edge_type="hierarchy"))
        graph.add_edge(Edge(source=ceo, target=cfo, label="reports to", edge_type="hierarchy"))
        graph.add_edge(Edge(source=cto, target=dev_lead, label="manages", edge_type="hierarchy"))
        graph.add_edge(Edge(source=cto, target=qa_lead, label="manages", edge_type="hierarchy"))
        graph.add_edge(Edge(source=cfo, target=finance_mgr, label="manages", edge_type="hierarchy"))
        graph.add_edge(Edge(source=dev_lead, target=dev1, label="supervises", edge_type="hierarchy"))
        graph.add_edge(Edge(source=dev_lead, target=dev2, label="supervises", edge_type="hierarchy"))
        graph.add_edge(Edge(source=qa_lead, target=qa1, label="supervises", edge_type="hierarchy"))

        return graph

    def get_model_by_syntax(self, syntax: str) -> Optional[Graph]:
        """Get a model by syntax type"""
        return self._models.get(syntax)

    def get_all_syntaxes(self) -> List[str]:
        """Get all available syntax types"""
        return ["basic", "process", "hierarchy"]

    def get_system_status(self) -> Dict[str, Any]:
        """Get system status information"""
        return {
            "total_models": len(self._models),
            "current_model": self._current_model_id,
            "available_syntaxes": self.get_all_syntaxes(),
            "models_info": {
                model_id: {
                    "name": graph.name,
                    "nodes": graph.node_count(),
                    "edges": graph.edge_count()
                }
                for model_id, graph in self._models.items()
            }
        }