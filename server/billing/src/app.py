"""Main application module."""
import os
from flask import Flask
from pythonjsonlogger import jsonlogger
import logging
from dotenv import load_dotenv

from .routes import billing_bp
from .database import init_db

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(billing_bp)
    
    # Initialize database
    init_db()
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 errors."""
        return {"error": "Not found"}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        return {"error": "Internal server error"}, 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) 