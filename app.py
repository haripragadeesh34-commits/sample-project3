#!/usr/bin/env python3
"""
Simple Flask application for demonstrating Jenkins and Kubernetes deployment.
"""

from flask import Flask, jsonify
from flask_restful import Api, Resource
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app)

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for Kubernetes liveness/readiness probes."""
    return jsonify({
        'status': 'healthy',
        'service': 'Python Flask App'
    }), 200

@app.route('/ready', methods=['GET'])
def ready():
    """Readiness check endpoint."""
    return jsonify({
        'status': 'ready',
        'service': 'Python Flask App'
    }), 200

# API Resources
class HelloWorld(Resource):
    def get(self):
        """Simple GET endpoint."""
        return {
            'message': 'Hello, World!',
            'version': os.getenv('APP_VERSION', '1.0.0')
        }

class Status(Resource):
    def get(self):
        """Application status endpoint."""
        return {
            'status': 'running',
            'environment': os.getenv('ENV', 'development'),
            'version': os.getenv('APP_VERSION', '1.0.0')
        }

# Register API routes
api.add_resource(HelloWorld, '/api/hello')
api.add_resource(Status, '/api/status')

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f'Internal server error: {error}')
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False') == 'True'
    app.run(host='0.0.0.0', port=port, debug=debug)
