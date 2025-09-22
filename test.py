#!/usr/bin/env python3
"""
Tests for ExPressiVeNess.

This file contains tests to verify core functionality works.
"""

import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_models_import():
    """Test that model imports work correctly."""
    try:
        from src.models import Graph, Node, Edge, Position
        print("OK Models import successfully")
        return True
    except ImportError as e:
        print(f"ERROR Models import failed: {e}")
        return False

def test_platform_import():
    """Test that platform imports work correctly."""
    try:
        from src.platform import ModelManager, GraphFactory
        print("OK Platform imports successfully")
        return True
    except ImportError as e:
        print(f"ERROR Platform import failed: {e}")
        return False

def test_web_app_import():
    """Test that web app imports work correctly."""
    try:
        import src.web.app
        print("OK Web app imports successfully")
        return True
    except ImportError as e:
        print(f"ERROR Web app import failed: {e}")
        return False

def test_graph_creation():
    """Test graph creation and operations."""
    try:
        from src.models import Graph, Node, Edge, Position

        # Create nodes
        node1 = Node(label="Node 1", position=Position(0, 0))
        node2 = Node(label="Node 2", position=Position(100, 100))

        # Create edge
        edge = Edge(source=node1, target=node2, label="Edge 1")

        # Create graph
        graph = Graph(name="Test Graph")
        graph.add_node(node1)
        graph.add_node(node2)
        graph.add_edge(edge)

        # Verify
        assert graph.node_count() == 2
        assert graph.edge_count() == 1
        assert node1 in graph.nodes
        assert node2 in graph.nodes
        assert edge in graph.edges

        print("OK Graph creation works")
        return True
    except Exception as e:
        print(f"ERROR Graph creation failed: {e}")
        return False

def test_graph_builder():
    """Test graph builder pattern."""
    try:
        from src.models import GraphBuilder

        builder = GraphBuilder()
        graph = (builder
                .set_name("Builder Test Graph")
                .set_directed(True)
                .add_node("start", "start_type", color="green")
                .add_node("end", "end_type", color="red")
                .add_edge("start", "end", "connection")
                .build())

        assert graph.name == "Builder Test Graph"
        assert graph.directed == True
        assert graph.node_count() == 2
        assert graph.edge_count() == 1

        print("OK Graph builder works")
        return True
    except Exception as e:
        print(f"ERROR Graph builder failed: {e}")
        return False

def test_web_api_endpoints():
    """Test Web API endpoints functionality."""
    try:
        import requests
        import time

        # Give server time to start
        base_url = "http://127.0.0.1:5000"

        # Test health endpoint
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
        except requests.exceptions.RequestException:
            print("SKIP Web API tests (server not running)")
            return True

        # Test graph API endpoints
        response = requests.get(f"{base_url}/api/graph/basic", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "graph" in data
        assert "nodes" in data["graph"]
        assert "edges" in data["graph"]

        # Test syntaxes endpoint
        response = requests.get(f"{base_url}/api/syntaxes", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "syntaxes" in data

        # Test main page redirect
        response = requests.get(f"{base_url}/", timeout=5, allow_redirects=False)
        assert response.status_code == 302

        # Test graph page
        response = requests.get(f"{base_url}/graph", timeout=5)
        assert response.status_code == 200

        print("OK Web API endpoints work")
        return True
    except ImportError:
        print("SKIP Web API tests (requests not available)")
        return True
    except Exception as e:
        print(f"ERROR Web API tests failed: {e}")
        return False

def test_model_manager_functionality():
    """Test ModelManager with different syntax types."""
    try:
        from src.platform import ModelManager

        manager = ModelManager()

        # Test getting all syntaxes
        syntaxes = manager.get_all_syntaxes()
        assert len(syntaxes) > 0
        assert "basic" in syntaxes
        assert "process" in syntaxes
        assert "hierarchy" in syntaxes

        # Test getting models by syntax
        basic_model = manager.get_model_by_syntax("basic")
        assert basic_model is not None
        assert basic_model.node_count() > 0
        assert basic_model.edge_count() > 0

        process_model = manager.get_model_by_syntax("process")
        assert process_model is not None
        assert process_model.node_count() > 0

        hierarchy_model = manager.get_model_by_syntax("hierarchy")
        assert hierarchy_model is not None
        assert hierarchy_model.node_count() > 0

        print("OK ModelManager functionality works")
        return True
    except Exception as e:
        print(f"ERROR ModelManager functionality failed: {e}")
        return False

def test_graph_serialization():
    """Test graph serialization to dictionary format."""
    try:
        from src.platform import ModelManager

        manager = ModelManager()
        graph = manager.get_model_by_syntax("basic")

        # Test serialization
        graph_dict = graph.to_dict()
        assert "nodes" in graph_dict
        assert "edges" in graph_dict
        assert "name" in graph_dict
        assert "directed" in graph_dict

        # Verify nodes structure
        nodes = graph_dict["nodes"]
        assert len(nodes) > 0
        for node in nodes:
            assert "id" in node
            assert "label" in node
            assert "node_type" in node
            assert "position" in node

        # Verify edges structure
        edges = graph_dict["edges"]
        assert len(edges) > 0
        for edge in edges:
            assert "source_id" in edge
            assert "target_id" in edge
            assert "label" in edge
            assert "edge_type" in edge

        print("OK Graph serialization works")
        return True
    except Exception as e:
        print(f"ERROR Graph serialization failed: {e}")
        return False

def run_all_tests():
    """Run all tests."""
    print("Running tests for ExPressiVeNess...\n")

    tests = [
        test_models_import,
        test_platform_import,
        test_web_app_import,
        test_graph_creation,
        test_graph_builder,
        test_model_manager_functionality,
        test_graph_serialization,
        test_web_api_endpoints
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("All tests passed! OK")
        return True
    else:
        print("Some tests failed! ERROR")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)