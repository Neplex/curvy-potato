"""
Structure controller
"""

from flask import url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restplus import Resource, Namespace, fields
from geojson import Point, LineString

from app.model.structure import StructureType, MedicalOffice, FitnessTrail, Hospital, Gym
from app.service.struct_service import get_structure, structure_to_geojson, geojson_to_structure, \
    update_structure, delete_structure, add_structure, structures_to_geojson, get_all_structure

API = Namespace('Structures', description='Structures related operations', path='/structures')

# ==================================================================================================

STRUCTURE_MODEL = API.model('structure', {
    'id': fields.Integer(required=False, readonly=True, description='Structure identifier'),
    'name': fields.String(required=True, description='Structure name'),
    'description': fields.String(required=False, description='Structure description'),
    'structure_type': fields.String(required=True, description='Structure type', attribute='type',
                                    enum=[x.value for x in StructureType])
})

FITNESS_TRAIL_MODEL = API.inherit(StructureType.FITNESS_TRAIL.value, STRUCTURE_MODEL, {
    'difficulty': fields.Integer(required=True, min=0)
})

HOSPITAL_MODEL = API.inherit(StructureType.HOSPITAL.value, STRUCTURE_MODEL, {
    'emergency': fields.Boolean(required=True),
    'maternity': fields.Boolean(required=True),
    'phone': fields.String(required=True)
})

MEDICAL_OFFICE_MODEL = API.inherit(StructureType.MEDICAL_OFFICE.value, STRUCTURE_MODEL, {
    'phone': fields.String(required=True),
    'specialities': fields.List(fields.String(), required=True)
})

GYM_MODEL = API.inherit(StructureType.GYM.value, STRUCTURE_MODEL, {
    'phone': fields.String(required=True),
    'price': fields.Float(required=True)
})

# ===

GEOMETRY_MODEL = API.model('GeoJSON geometry', {
    'type': fields.String(required=True, enum=['Point', 'LineString']),
})

POINT_MODEL = API.inherit('GeoJSON point', GEOMETRY_MODEL, {
    'coordinates': fields.List(fields.Float)
})

LINESTRING_MODEL = API.inherit('GeoJSON linestring', GEOMETRY_MODEL, {
    'coordinates': fields.List(fields.List(fields.Float))
})

# ===

FEATURE_MODEL = API.model('GeoJSON feature', {
    'type': fields.String(enum=['Feature']),
    'geometry': fields.Polymorph({
        Point: POINT_MODEL,
        LineString: LINESTRING_MODEL
    }, example=Point((0, 0))),
    'properties': fields.Polymorph({
        MedicalOffice: MEDICAL_OFFICE_MODEL,
        FitnessTrail: FITNESS_TRAIL_MODEL,
        Hospital: HOSPITAL_MODEL,
        Gym: GYM_MODEL
    }),
    'distance': fields.Float(required=False, readonly=True, description='Distance to the structure')
})

FEATURE_COLLECTION_MODEL = API.model('GeoJSON feature collection', {
    'type': fields.String(enum=['FeatureCollection']),
    'bbox': fields.List(fields.Float, required=False, readonly=True, example=[0] * 4),
    'features': fields.List(fields.Nested(FEATURE_MODEL, skip_none=True))
})

# ===

STRUCTURE_LIST_OPTIONS = API.parser()
STRUCTURE_LIST_OPTIONS.add_argument('query', type=str, trim=True)
STRUCTURE_LIST_OPTIONS.add_argument('bounds', type=float, action='split')

STRUCTURE_OPTIONS = API.parser()
STRUCTURE_OPTIONS.add_argument('distanceFrom', type=float, action='split')


# ==================================================================================================


@API.route('')
class StructureListController(Resource):
    """
    Show a list of all structure or add a new one
    """

    @API.doc('list_resources', security=None)
    @API.expect(STRUCTURE_LIST_OPTIONS)
    @API.marshal_with(FEATURE_COLLECTION_MODEL)
    def get(self):
        """List all structures"""
        args = STRUCTURE_LIST_OPTIONS.parse_args()
        return structures_to_geojson(get_all_structure(**args))

    @jwt_required
    @API.doc('create_structure')
    @API.expect(FEATURE_MODEL)
    @API.marshal_with(FEATURE_MODEL, code=201)
    def post(self):
        """Create a new structure"""
        structure = geojson_to_structure(API.payload, None, get_jwt_identity())
        add_structure(structure)
        return structure_to_geojson(structure), 201, {'Location': url_for(
            'api.Structures_structure_controller', structure_id=structure.id)}


@API.route('/<int:structure_id>')
@API.response(404, 'Structure not found')
@API.param('structure_id', 'The structure identifier')
class StructureController(Resource):
    """
    Show a single structure and lets you update or delete them
    """

    @API.doc('get_structure', security=None)
    @API.expect(STRUCTURE_OPTIONS)
    @API.marshal_with(FEATURE_MODEL, skip_none=True)
    def get(self, structure_id):
        """Get the resource"""
        args = STRUCTURE_OPTIONS.parse_args()
        structure = get_structure(structure_id)
        return structure_to_geojson(structure, {
            'distance': structure.get_distance_from(args['distanceFrom'])
        })

    @jwt_required
    @API.doc('update_structure')
    @API.expect(FEATURE_MODEL)
    @API.marshal_with(FEATURE_MODEL, skip_none=True)
    def put(self, structure_id):
        """Update a structure given its identifier"""
        structure = geojson_to_structure(API.payload, structure_id, get_jwt_identity())
        update_structure(structure)
        return structure_to_geojson(structure)

    @jwt_required
    @API.doc('delete_structure')
    @API.response(204, 'Structure deleted')
    def delete(self, structure_id):
        """Delete a structure given its identifier"""
        delete_structure(structure_id)
        return '', 204
