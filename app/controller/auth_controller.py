"""
Authentication controller
"""

from flask_jwt_extended import jwt_required, create_access_token, get_raw_jwt
from flask_restplus import Resource, Namespace, fields, abort

from app.app import JWT_MANAGER
from app.service.auth_service import get_user, revoke_jti, jti_is_revoked

API = Namespace('auth', description='authentication related operations')

AUTH_MODEL = API.model('auth_details', {
    'username': fields.String(required=True, description='User name'),
    'password': fields.String(required=True, description='User password')
})

JWT_MODEL = API.model('jwt_response', {
    'token': fields.String(required=True, description='JSON Web Token', example="Bearer <JWT>")
})


@JWT_MANAGER.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    """Check if a token is blacklisted or not"""
    jti = decrypted_token['jti']
    return jti_is_revoked(jti)


@API.route('/login')
class Login(Resource):
    """
    Login Resource
    """

    @API.doc('login', security=None)
    @API.expect(AUTH_MODEL)
    @API.marshal_with(JWT_MODEL, description='Successfully logged in')
    @API.response(400, 'Invalid payload')
    @API.response(401, 'Wrong credentials')
    def post(self):
        """Generate a JWT"""
        data = API.payload
        user = get_user(data['username'], data['password'])

        if user is not None:
            access_token = create_access_token(identity=user.id)
            return {'token': 'Bearer ' + access_token}

        return abort(401, 'Wrong credentials')


@API.route('/logout')
class Logout(Resource):
    """
    Logout Resource
    """

    @jwt_required
    @API.doc('logout')
    @API.response(200, '')
    @API.response(401, 'Invalid authentication token')
    def post(self):
        """Blacklist a JWT"""
        jti = get_raw_jwt()['jti']
        revoke_jti(jti)
        return {'message': 'Token revoked successfully'}
