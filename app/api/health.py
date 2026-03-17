"""Health check endpoints"""
from flask import Blueprint, jsonify
from datetime import datetime
import platform

bp = Blueprint('health', __name__)


@bp.route('/health')
def health_check():
    """Basic health check endpoint"""
    return jsonify({
        'success': True,
        'data': {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '2.0.0',
            'environment': platform.node()
        }
    })


@bp.route('/ping')
def ping():
    """Simple ping endpoint"""
    return jsonify({
        'success': True,
        'message': 'pong',
        'version': '2.0.0'
    })


@bp.route('/ready')
def ready_check():
    """Readiness check for Kubernetes/Docker"""
    return jsonify({
        'success': True,
        'data': {
            'ready': True,
            'timestamp': datetime.utcnow().isoformat()
        }
    })