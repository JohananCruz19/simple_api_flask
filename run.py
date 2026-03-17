"""Application entry point"""
from app import create_app, db
from config import config_by_name
import os

env = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_class=config_by_name.get(env, config_by_name['default']))


@app.shell_context_processor
def make_shell_context():
    """Auto-imports for Flask shell"""
    return {
        'db': db,
        'Product': __import__('app.models', fromlist=['Product']).Product
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)