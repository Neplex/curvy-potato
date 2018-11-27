"""
Structure controller
"""

from flask import url_for
from flask_restplus import Resource, Namespace, fields, abort
from flask_jwt_extended import jwt_required
from geojson import Point, LineString

from app.model.structure import *
from app.service.struct_service import get_all_structure, add_structure, get_structure, delete_structure

API = Namespace('struct', description='structures related operations', path='/')

# ======================================================================================================================

STRUCTURE_MODEL = API.model('structure', {
    'id': fields.Integer(required=True, description='Structure identifier'),
    'name': fields.String(required=True, description='Structure name'),
    'description': fields.String(required=False, description='Structure description'),
    'structure_type': fields.String(required=True, description='Structure type')
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

# ======================================================================================================================


def structure_to_geojson(s):
    return {'properties': s, 'geometry': s.geometry}


def structures_to_geojson(sl):
    return {'features': [structure_to_geojson(s) for s in sl]}

# ======================================================================================================================


@API.route('/structures')
class StructureListController(Resource):
    """
    Show a list of all structure or add a new one
    """

    @API.doc('list_resources', security=None)
    @API.marshal_with(FEATURE_COLLECTION_MODEL)
    def get(self):
        """List all structures"""
        # todo: return urls or object ?
        return structures_to_geojson(get_all_structure())

    #@jwt_required
    @API.doc('create_structure')
    @API.expect(FEATURE_MODEL)
    @API.marshal_with(FEATURE_MODEL, code=201)
    def post(self):
        """Create a new structure"""
        data = API.payload
        # todo: check null element + convertion
        struct = FitnessTrail(name="fitness trail", description="trail", difficulty=10, geom="LINESTRING(30 10, 20 20)")
        add_structure(struct)
        return structure_to_geojson(struct), 201, {'Location': url_for('api.struct_structure_controller', id=struct.id)}


@API.route('/structures/<int:id>')
@API.response(404, 'Structure not found')
@API.param('id', 'The structure identifier')
class StructureController(Resource):
    """
    Show a single structure and lets you update or delete them
    """

    @API.doc('get_structure', security=None)
    @API.marshal_with(FEATURE_MODEL)
    def get(self, id):
        """Get the resource"""
        struct = get_structure(id)

        if struct is not None:
            return structure_to_geojson(struct)

        self.not_found(id)

    @jwt_required
    @API.doc('update_structure')
    @API.expect(FEATURE_MODEL)
    @API.marshal_with(FEATURE_MODEL)
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
