"""
Structure controller
"""

from flask import url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restplus import Resource, Namespace, fields, abort
from geojson import Point, LineString, dumps

from app.model.structure import FitnessTrail, Hospital
from app.service.struct_service import \
    get_all_structure, add_structure, get_structure, delete_structure, get_all_structure_by_user,\
    get_favourites_by_user, update_structure

from app.controller.user_controller import API as USER_API

API = Namespace('Structures', description='Structures related operations', path='/structures')

# ==================================================================================================

STRUCTURE_MODEL = API.model('structure', {
    'id': fields.Integer(required=False, description='Structure identifier'),
    'name': fields.String(required=True, description='Structure name'),
    'description': fields.String(required=False, description='Structure description'),
    'structure_type': fields.String(required=True, description='Structure type', 
                                    enum=["fitness_trail","hospital"])
})

FITNESS_TRAIL_MODEL = API.inherit('fitness trail', STRUCTURE_MODEL, {
    'difficulty': fields.Integer(required=True)
})

HOSPITAL_MODEL = API.inherit('hospital', STRUCTURE_MODEL, {
    'emergency': fields.Boolean(required=True),
    'maternity': fields.Boolean(required=True)
})

# ===

GEOMETRY_MODEL = API.model('GeoJSON geometry', {
    'type': fields.String(required=True),
})

POINT_MODEL = API.inherit('GeoJSON point', GEOMETRY_MODEL, {
    'coordinates': fields.List(fields.Integer())
})

LINESTRING_MODEL = API.inherit('GeoJSON linestring', GEOMETRY_MODEL, {
    'coordinates': fields.List(fields.List(fields.Integer()))
})

# ===

FEATURE_MODEL = API.model('GeoJSON feature', {
    'type': fields.String(default='Feature'),
    'geometry': fields.Polymorph({
        Point: POINT_MODEL,
        LineString: LINESTRING_MODEL
    }),
    'properties': fields.Polymorph({
        FitnessTrail: FITNESS_TRAIL_MODEL,
        Hospital: HOSPITAL_MODEL
    })
})

FEATURE_COLLECTION_MODEL = API.model('GeoJSON feature collection', {
    'type': fields.String(default='FeatureCollection'),
    'features': fields.List(fields.Nested(FEATURE_MODEL))
})


# ==================================================================================================


def structure_to_geojson(structure):
    """Convert structure object to geojson"""
    return {'properties': structure, 'geometry': structure.geometry}


def structures_to_geojson(structure_list):
    """Convert structure list to geojson"""
    return {'features': [structure_to_geojson(
        structure) for structure in structure_list]}


# ==================================================================================================


@API.route('')
class StructureListController(Resource):
    """
    Show a list of all structure or add a new one
    """

    @API.doc('list_resources', security=None)
    @API.marshal_with(FEATURE_COLLECTION_MODEL)
    def get(self):
        """List all structures"""
        # TODO: return urls or object ?
        return structures_to_geojson(get_all_structure())

    @jwt_required
    @API.doc('create_structure')
    @API.expect(FEATURE_MODEL)
    @API.marshal_with(FEATURE_MODEL, code=201)
    def post(self):
        """Create a new structure"""
        props = API.payload['properties']
        if props['structure_type'] == 'fitness_trail':
            struct = FitnessTrail(name=props['name'], description=props['description'],
                                  difficulty=props['difficulty'],
                                  geometry=dumps(API.payload['geometry']),
                                  user_id=get_jwt_identity())
        elif props['structure_type'] == 'hospital':
            struct = Hospital(name=props['name'], description=props['description'],
                              geometry=dumps(API.payload['geometry']), emergency=props['emergency'],
                              maternity=props['maternity'], user_id=get_jwt_identity())
        add_structure(struct)
        return structure_to_geojson(struct), 201, {'Location': url_for(
            'api.Structures_structure_controller', structure_id=struct.id)}


@API.route('/<int:structure_id>')
@API.response(404, 'Structure not found')
@API.param('structure_id', 'The structure identifier')
class StructureController(Resource):
    """
    Show a single structure and lets you update or delete them
    """

    @API.doc('get_structure', security=None)
    @API.marshal_with(FEATURE_MODEL)
    def get(self, structure_id):
        """Get the resource"""
        struct = get_structure(structure_id)

        if struct is None:
            self.not_found(structure_id)

        return structure_to_geojson(struct)

    @jwt_required
    @API.doc('update_structure')
    @API.expect(FEATURE_MODEL)
    @API.marshal_with(FEATURE_MODEL)
    def put(self, structure_id):
        """Update a structure given its identifier"""
        props = API.payload['properties']
        if props['structure_type'] == 'fitness_trail':
            struct = FitnessTrail(id=structure_id, name=props['name'],
                                  description=props['description'],
                                  difficulty=props['difficulty'],
                                  geometry=dumps(API.payload['geometry']),
                                  user_id=get_jwt_identity())
        elif props['structure_type'] == 'hospital':
            struct = Hospital(id=structure_id, name=props['name'], description=props['description'],
                              geometry=dumps(API.payload['geometry']), emergency=props['emergency'],
                              maternity=props['maternity'], user_id=get_jwt_identity())
        update_structure(struct)
        return structure_to_geojson(struct)

    @jwt_required
    @API.doc('delete_structure')
    @API.response(204, 'Structure deleted')
    def delete(self, structure_id):
        """Delete a structure given its identifier"""
        delete_structure(structure_id)
        return '', 204

    # TODO: Replace it by exception
    @staticmethod
    def not_found(structure_id):
        """Wrapper for not found error"""
        abort(404, "Structure %i doesn't exist" % structure_id)


@USER_API.route('/<int:user_id>/structures')
class StructureUserController(Resource):
    """
    Show a list of all structure from a user
    """

    @API.doc('list_resources_from_user', security=None)
    @API.marshal_with(FEATURE_COLLECTION_MODEL)
    def get(self, user_id):
        """List all structures of an user"""
        return structures_to_geojson(get_all_structure_by_user(user_id))

@USER_API.route('/<int:user_id>/favourites')
class FavorisUserController(Resource):
    """
    Show a list of all structure from a user
    """

    @API.doc('list_favourites_of_user', security=None)
    @API.marshal_with(FEATURE_COLLECTION_MODEL)
    def get(self, user_id):
        """List all favourites of an user"""
        return structures_to_geojson(get_favourites_by_user(user_id))
