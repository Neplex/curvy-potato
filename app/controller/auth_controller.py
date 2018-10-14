"""
Authentication controller
"""

from flask_restplus import Resource, Namespace, fields

API = Namespace('auth', description='authentication related operations')

AUTH_MODEL = API.model('auth_details', {
    'app_name': fields.String(required=True, description='Application name'),
    'app_key': fields.String(required=True, description='Application key')
})


@API.route('/login')
class Login(Resource):
    """
    Login Resource
    """
    @API.doc('login')
    @API.expect(AUTH_MODEL, validate=True)
    def post(self):  # TODO
        """Generate a JWT"""
        pass


@API.route('/logout')
class LogoutI(Resource):
    """
    Logout Resource
    """
    @API.doc('logout')
    def post(self):  # TODO
        """Blacklist a JWT"""
        pass
