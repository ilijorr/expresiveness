# ExpresiVeNess

**A platform for graph management and visualization with software design pattern integration**

Authors: Vuk Vićentić, Ilija Jordanovski, Miloš Milosavljević

## Project Overview

ExpresiVeNess is a Python-based platform for creating, managing, and visualizing graphs, built around key software design patterns. The project supports multiple graph types through a flexible architecture that leverages Factory, Observer, Adapter, and Builder patterns.

## Features

- **Graph creation and management** – Add, remove, and modify nodes and edges  
- **Multi-syntax support** – Basic Graph, Hierarchy, Process Flow  
- **Web interface** – Flask-based graph visualization  
- **Observer pattern** – Track model changes  
- **Factory pattern** – Create graphs of different types  
- **Adapter pattern** – Support for multiple graph syntaxes  
- **Builder pattern** – Incremental construction of complex graphs  

## Project Structure

```
expressivenness/
├── src/
│   ├── models/          # Core models (Node, Edge, Graph, Position)
│   │   ├── graph.py     # Main graph class
│   │   ├── node.py      # Node model
│   │   ├── edge.py      # Edge model
│   │   ├── position.py  # Node position
│   │   └── observers.py # Observer pattern implementation
│   ├── platform/        # Platform core
│   │   ├── model_manager.py  # Graph model management
│   │   └── factories.py      # Factory pattern for graph creation
│   ├── adapters/        # Adapter pattern for syntax handling
│   │   ├── base.py      # Base adapter
│   │   └── syntaxes/    # Syntax-specific adapters
│   │       ├── basic_graph.py  # Basic graph adapter
│   │       ├── hierarchy.py    # Hierarchy graph adapter
│   │       └── process.py      # Process flow adapter
│   └── web/             # Flask web application
│       ├── app.py       # Main Flask app
│       ├── templates/   # HTML templates
│       └── static/      # CSS and JS files
├── setup.py             # Installation script
└── test.py              # Test suite
```

## Installation

### Prerequisites
- Python 3.8 or higher  
- pip package manager  

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd expressivenness
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   # or
   pip install flask flask-cors
   ```

3. **Install the project:**
   ```bash
   pip install -e .
   ```

## Running the Application

### 1. Start the web application
```bash
python src/web/app.py
```
The app will be available at `http://localhost:5000`

### 2. Run the test suite
```bash
python test.py
```

### 3. Programmatic usage
```python
from src.models import Graph, Node, Edge, Position
from src.platform import ModelManager, GraphFactory

# Create a graph
graph = Graph("My Graph")

# Create nodes
node1 = Node("Node1", Position(0, 0))
node2 = Node("Node2", Position(100, 100))

# Add nodes to the graph
graph.add_node(node1)
graph.add_node(node2)

# Create an edge
edge = Edge(node1, node2, "link")
graph.add_edge(edge)

# Use ModelManager
manager = ModelManager()
model_id = manager.add_model(graph)
```

## System Components

### 1. **Models** (`src/models/`)
- **Graph**: Core structure with nodes and edges  
- **Node**: Graph node with position and properties  
- **Edge**: Connection between two nodes  
- **Position**: 2D coordinates for nodes  
- **Observers**: Observer pattern for change tracking  

### 2. **Platform** (`src/platform/`)
- **ModelManager**: Centralized graph management  
- **GraphFactory**: Factory pattern for graph instantiation  

### 3. **Adapters** (`src/adapters/`)
- **SyntaxRegistry**: Registry of available syntaxes  
- **Basic Graph**: Adapter for basic graphs  
- **Hierarchy**: Adapter for hierarchical graphs  
- **Process**: Adapter for process flow graphs  

### 4. **Web Interface** (`src/web/`)
- **Flask application** for graph visualization  
- **REST API** for graph operations  
- **Interactive UI** for user interaction  

## API Endpoints

- `GET /` – Home page  
- `GET /graph` – Graph view  
- `GET /api/syntaxes` – List of available syntaxes  
- `GET /api/graph/<syntax>` – Graph for specific syntax  
- `GET /api/graph/current` – Currently active graph  
- `GET /health` – Health check  

## Testing

The project includes a complete test suite covering:
- Module imports  
- Graph creation  
- Node and edge operations  
- Model manager functionality  
- Serialization and deserialization  
- Web application behavior  

Run tests with:
```bash
python test.py
```

## Design Patterns Used

1. **Observer Pattern** – For tracking model changes  
2. **Factory Pattern** – For creating different graph types  
3. **Adapter Pattern** – For supporting multiple syntaxes  
4. **Builder Pattern** – For incremental graph construction  
5. **Model-View-Controller** – Web application architecture  

## Development Guide

To add a new syntax:
1. Create a new adapter in `src/adapters/syntaxes/`  
2. Register it in `SyntaxRegistry`  
3. Add corresponding tests  

To add new functionality:
1. Add a model in `src/models/`  
2. Update `ModelManager` if needed  
3. Add an API endpoint in `app.py`  
4. Update the test suite  

---

*This project was developed as part of the course "Software Patterns and Components"*  
