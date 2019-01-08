"""
Structure service
"""

from geojson import dumps, Feature, FeatureCollection
from sqlalchemy import func
from sqlalchemy.orm import with_polymorphic

from app.app import DB
from app.model.structure import StructureType, Structure, \
    MedicalOffice, FitnessTrail, Hospital, Gym


def get_all_structure(query=None, bounds=None):
    """Get all structures."""

    result = DB.session.query(with_polymorphic(Structure, '*'))

    if query is not None:
        query = str(query)
        result = result.filter(
            Structure.name.contains(query) |
            Structure.description.contains(query)
        )

    if bounds is not None and len(bounds) == 4:
        bbox = ('POLYGON((' + ', '.join(['{} {}'] * 5) + '))').format(
            bounds[0], bounds[1],
            bounds[2], bounds[1],
            bounds[2], bounds[3],
            bounds[0], bounds[3],
            bounds[0], bounds[1]
        )
        result = result.filter(func.ST_Within(Structure.geom, func.ST_GeomFromText(bbox)))

    return result


def get_all_structure_by_user(user_id):
    """Get all structures from user"""
    return DB.session.query(with_polymorphic(Structure, '*')).filter(Structure.user_id == user_id)


def get_favourites_by_user(user_id):
    """Get all favourites of an user"""
    return DB.session.query(with_polymorphic(Structure, '*')).filter(
        Structure.favourites_of.any(id=user_id))


def add_structure(struct):
    """Add a structure in the database."""
    DB.session.add(struct)
    DB.session.commit()


def get_structure(structure_id):
    """Get a structure from the DB given its identifier"""
    return Structure.query.get(structure_id)


def update_structure(structure):
    """Update a defined structure"""
    DB.session.merge(structure)
    DB.session.commit()


def delete_structure(structure_id):
    """Delete a structure from the DB given its identifier"""
    struct = get_structure(structure_id)

    if struct is not None:
        DB.session.delete(struct)
        DB.session.commit()


def structure_to_geojson(structure, extras=None):
    """Convert structure object to geojson"""
    return Feature(None, structure.geometry, structure, **(extras or {}))


def structures_to_geojson(structure_list):
    """Convert structure list to geojson"""
    bounding_box = []
    structs_geojson = []
    for structure in structure_list:
        if not bounding_box:
            for _ in range(2):
                bounding_box.append(DB.session.scalar(structure.geom.ST_Centroid().ST_X()))
                bounding_box.append(DB.session.scalar(structure.geom.ST_Centroid().ST_Y()))        
        bounding_box[0] = min(
            DB.session.scalar(structure.geom.ST_Centroid().ST_X()), bounding_box[0])
        bounding_box[1] = min(
            DB.session.scalar(structure.geom.ST_Centroid().ST_Y()), bounding_box[1])
        bounding_box[2] = max(
            DB.session.scalar(structure.geom.ST_Centroid().ST_X()), bounding_box[2])
        bounding_box[3] = max(
            DB.session.scalar(structure.geom.ST_Centroid().ST_Y()), bounding_box[3])
        structs_geojson.append(structure_to_geojson(structure))
    return FeatureCollection(structs_geojson, bbox=bounding_box)


def geojson_to_structure(geo, structure_id, user_id):
    """Convert geojson to structure"""
    structure_class = {
        StructureType.MEDICAL_OFFICE: MedicalOffice,
        StructureType.FITNESS_TRAIL: FitnessTrail,
        StructureType.HOSPITAL: Hospital,
        StructureType.GYM: Gym
    }

    properties = {**(geo['properties']), 'user_id': user_id, 'geometry': dumps(geo['geometry'])}
    structure_type = properties['structure_type'] = StructureType(properties['structure_type'])

    if structure_id is not None:
        properties['id'] = structure_id

    return structure_class[structure_type](**properties)
