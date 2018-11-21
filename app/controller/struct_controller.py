"""
Structure controller
"""

from flask import url_for
from flask_restplus import Resource, Namespace, fields, abort
from flask_jwt_extended import jwt_required

from app.model.structure import Structure
from app.service.struct_service import get_all_structure, add_structure, get_structure, delete_structure

API = Namespace('struct', description='structures related operations', path='/')

STRUCTURE_MODEL = API.model('structure', {
    'name': fields.String(required=True, description='Structure name'),
    'description': fields.String(required=False, description='Structure description'),
    'geometry': fields.String(required=True, description='Structure geometry')
}, skip_none=True)


@API.route('/structures')
class StructureListController(Resource):
    """
    Show a list of all structure or add a new one
    """

    @API.doc('list_resources', security=None)
    @API.marshal_list_with(STRUCTURE_MODEL)
    def get(self):
        """List all structures"""
        # todo: return urls or object ?
        return get_all_structure()

    @jwt_required
    @API.doc('create_structure')
    @API.expect(STRUCTURE_MODEL)
    @API.marshal_with(STRUCTURE_MODEL, code=201)
    def post(self):
        """Create a new structure"""
        data = API.payload
        struct = Structure(name=data['name'], description=data['description'], geom=data['geometry']) # todo: check null element + convertion
        add_structure(struct)
        return struct, 201, {'Location': url_for('api.struct_structure_controller', id=struct.id)}


@API.route('/structures/<int:id>')
@API.response(404, 'Structure not found')
@API.param('id', 'The structure identifier')
class StructureController(Resource):
    """
    Show a single structure and lets you update or delete them
    """

    @API.doc('get_structure', security=None)
    @API.marshal_with(STRUCTURE_MODEL)
    def get(self, id):
        """Get the resource"""
        struct = get_structure(id)

        if struct is not None:
            return struct

        self.not_found(id)

    @jwt_required
    @API.doc('update_structure')
    @API.expect(STRUCTURE_MODEL)
    @API.marshal_with(STRUCTURE_MODEL)
    def put(self, id):
        """Update a structure given its identifier"""
        # todo: do something
        pass

    @jwt_required
    @API.doc('delete_structure')
    @API.response(204, 'Structure deleted')
    def delete(self, id):
        """Delete a structure given its identifier"""
        delete_structure(id)
        return '', 204

    # todo: Replace it by exception
    @staticmethod
    def not_found(id):
        """Wrapper for not found error"""
        abort(404, "Structure %i doesn't exist" % id)
