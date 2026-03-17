"""
Flask API REST v2.0.0 - Backend Profesional
CRUD completo para Productos con SQLAlchemy y Marshmallow
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import Config

# Extensions
db = SQLAlchemy()
ma = Marshmallow()


def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    
    # Register blueprints
    from app.api.products import bp as products_bp
    from app.api.health import bp as health_bp
    
    app.register_blueprint(products_bp, url_prefix='/api/v1/products')
    app.register_blueprint(health_bp, url_prefix='/api/v1')
    
    # Register error handlers
    register_error_handlers(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app


def register_error_handlers(app):
    """Register global error handlers"""
    
    @app.errorhandler(400)
    def bad_request(error):
        return {
            'success': False,
            'error': {
                'code': 400,
                'message': 'Bad Request',
                'details': str(error.description) if hasattr(error, 'description') else 'Invalid request data'
            }
        }, 400
    
    @app.errorhandler(404)
    def not_found(error):
        return {
            'success': False,
            'error': {
                'code': 404,
                'message': 'Not Found',
                'details': 'The requested resource was not found'
            }
        }, 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return {
            'success': False,
            'error': {
                'code': 405,
                'message': 'Method Not Allowed',
                'details': 'The HTTP method is not allowed for this endpoint'
            }
        }, 405
    
    @app.errorhandler(422)
    def unprocessable_entity(error):
        return {
            'success': False,
            'error': {
                'code': 422,
                'message': 'Unprocessable Entity',
                'details': str(error.description) if hasattr(error, 'description') else 'Validation error'
            }
        }, 422
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return {
            'success': False,
            'error': {
                'code': 500,
                'message': 'Internal Server Error',
                'details': 'An unexpected error occurred'
            }
        }, 500


# Import models for SQLAlchemy
from app.models import Product