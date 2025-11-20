"""
Pytest configuration and fixtures for testing.
"""

import pytest
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


@pytest.fixture
def app():
    """Create and configure a test instance of the Flask app."""
    from app import app as flask_app
    from config import Config
    
    # Configure app for testing
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False
    flask_app.config['SECRET_KEY'] = 'test-secret-key'
    
    # Use test database
    flask_app.config['MONGO_URI'] = os.environ.get('MONGO_URI_TEST', 
                                                     flask_app.config.get('MONGO_URI'))
    
    yield flask_app


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test CLI runner for the app."""
    return app.test_cli_runner()
