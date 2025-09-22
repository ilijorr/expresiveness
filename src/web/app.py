"""
Flask Web Application for Expressiveness Graph Management
"""

import os
import sys
from pathlib import Path

# Add parent directory to Python path for imports
current_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(current_dir))

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

from src.platform.model_manager import ModelManager
from src.platform.factories import GraphFactory
from src.adapters.base import SyntaxRegistry
from src.models import Graph, Node, Edge, Position
import re



def create_app():
    """Create Flask application"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

    # Enable CORS
    CORS(app)

    # Initialize core components
    model_manager = ModelManager()
    graph_factory = GraphFactory("web")
    syntax_registry = SyntaxRegistry()

    # Store components in app context
    app.model_manager = model_manager
    app.graph_factory = graph_factory
    app.syntax_registry = syntax_registry

    @app.route('/')
    def index():
        """Redirect to main graph view"""
        from flask import redirect, url_for
        return redirect(url_for('graph_view'))

    @app.route('/graph')
    def graph_view():
        """Graph visualization page - view existing graph"""
        return render_template('graph.html', mode='view')


    @app.route('/api/syntaxes')
    def get_syntaxes():
        """Get available syntaxes"""
        try:
            syntaxes = model_manager.get_all_syntaxes()
            return jsonify({
                'success': True,
                'syntaxes': syntaxes
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/graph/<syntax>')
    def get_graph_by_syntax(syntax):
        """Get graph data for specific syntax"""
        try:
            graph = model_manager.get_model_by_syntax(syntax)
            if graph:
                return jsonify({
                    'success': True,
                    'graph': graph.to_dict()
                })
            else:
                return jsonify({
                    'success': False,
                    'error': f'No graph found for syntax: {syntax}'
                }), 404
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500


    @app.route('/api/graph/current')
    def get_current_graph():
        """Get current active graph"""
        try:
            graph = model_manager.get_current_model()
            if graph:
                return jsonify({
                    'success': True,
                    'graph': graph.to_dict()
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'No current graph set'
                }), 404
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500



    @app.route('/health')
    def health_check():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'components': {
                'model_manager': 'ok',
                'graph_factory': 'ok',
                'syntax_registry': 'ok'
            }
        })

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)