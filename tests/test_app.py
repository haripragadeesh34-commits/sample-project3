"""
Unit tests for Flask application.
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'


def test_ready_endpoint(client):
    """Test readiness check endpoint."""
    response = client.get('/ready')
    assert response.status_code == 200
    assert response.json['status'] == 'ready'


def test_hello_world_endpoint(client):
    """Test hello world API endpoint."""
    response = client.get('/api/hello')
    assert response.status_code == 200
    assert 'message' in response.json
    assert response.json['message'] == 'Hello, World!'


def test_status_endpoint(client):
    """Test status API endpoint."""
    response = client.get('/api/status')
    assert response.status_code == 200
    assert response.json['status'] == 'running'
    assert 'version' in response.json


def test_404_not_found(client):
    """Test 404 error handling."""
    response = client.get('/nonexistent')
    assert response.status_code == 404
    assert 'error' in response.json


def test_app_creation():
    """Test that app is created correctly."""
    assert app is not None
    assert app.testing is False
