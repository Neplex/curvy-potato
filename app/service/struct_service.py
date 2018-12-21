"""
Structure service
"""

from geojson import dumps, Feature, FeatureCollection
from sqlalchemy.orm import with_polymorphic

from app.app import DB
from app.model.structure import StructureType, Structure, \
    MedicalOffice, FitnessTrail, Hospital, Gym


def get_all_structure():
    """Get all structures."""
    return DB.session.query(with_polymorphic(Structure, '*'))


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


def structure_to_geojson(structure):
    """Convert structure object to geojson"""
    return Feature(None, structure.geometry, structure)


def structures_to_geojson(structure_list):
    """Convert structure list to geojson"""
    return FeatureCollection([structure_to_geojson(structure) for structure in structure_list])


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
