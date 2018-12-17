"""
User controller
"""

from flask_jwt_extended import jwt_required
from flask_restplus import Resource, Namespace, fields
from app.service.user_service import get_all_user, add_user, get_user, update_user, delete_user
from app.model.user import User


API = Namespace('User', description='User related operations', path='/users')

USER_MODEL = API.model('user', {
    'id': fields.Integer(required=False, description='User identifier'),
    'username': fields.String(required=True, description='Username of the user'),
    'password_hash': fields.String(required=False, description='User password hash'),
    'created_on': fields.DateTime(required=False, description='User creation date')
})

USER_CREATE = API.model('user', {
    'username': fields.String(required=True, description='Username of the user'),
    'password': fields.String(required=True, description='User password'),
})

USER_UPDATE = API.model('user', {
    'username': fields.String(required=True, description='Username of the user'),
    'password': fields.String(required=False, description='User password'),
})

@API.route('')
class UserListController(Resource):
    """
    Show a list of all users
    """

    @API.doc('list_users', security=None)
    @API.marshal_with(USER_MODEL)
    def get(self):
        """List all users"""
        return get_all_user()


    @API.doc('create_user', security=None)
    @API.expect(USER_CREATE)
    @API.marshal_with(USER_CREATE, code=201)
    def post(self):
        """Add a new user"""
        user = User(username=API.payload['username'], password=API.payload['password'])
        add_user(user)
        return API.payload, 201


@API.route('/<int:user_id>')
@API.response(404, 'User not found')
@API.param('user_id', 'The user identifier')
class UserController(Resource):
    """
    Show, delete or update a defined user.
    """

    @API.doc('get_structure', security=None)
    @API.marshal_with(USER_MODEL)
    def get(self, user_id):
        """Get the user"""
        return get_user(user_id)


    @jwt_required
    @API.doc('update_user')
    @API.expect(USER_UPDATE)
    @API.marshal_with(USER_UPDATE)
    def put(self, user_id):
        """Update the user"""
        user = get_user(user_id)
        updated_user = User(id=user_id, username=API.payload['username'],
                            password_hash=user.password_hash,
                            created_on=user.created_on,
                            structures=user.structures)
        if "password" in API.payload.keys():
            updated_user.password = API.payload['password']
        update_user(updated_user)
        return updated_user


    @jwt_required
    @API.doc('delete_user')
    @API.response(204, 'User deleted')
    def delete(self, user_id):
        """Delete a user given its identifier"""
        delete_user(user_id)
        return '', 204
