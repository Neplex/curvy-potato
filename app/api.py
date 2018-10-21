"""
API v1
"""

from flask import Blueprint
from flask_restplus import Api

from . import APP, JWT_MANAGER
from .controller.auth_controller import API as auth_ns

AUTHORIZATIONS = {
    'JWT': {
        'type': 'apiKey',
        'name': 'Authorization',
        'in': 'header'
    }
}

# Build API
API_BLUEPRINT = Blueprint('api', __name__, url_prefix='/v1')
API = Api(API_BLUEPRINT, title='', version='1.0',
          description='',
          authorizations=AUTHORIZATIONS, security='JWT', validate=True)

# Add namespaces
API.add_namespace(auth_ns)

# Register blueprint
APP.register_blueprint(API_BLUEPRINT)

# Small hack for flask-restplus error handling system to handle flask-jwt-extended errors
# From: https://github.com/vimalloc/flask-jwt-extended/issues/86#issuecomment-335509456
JWT_MANAGER._set_error_handler_callbacks(API)
