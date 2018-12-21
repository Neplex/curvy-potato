"""
Structure object
"""

import enum

import geojson
from geoalchemy2 import Geometry
from sqlalchemy import func

from app.app import DB


class StructureType(enum.Enum):
    """Structure class"""

    FITNESS_TRAIL = 'fitness_trail'
    HOSPITAL = 'hospital'
    MEDICAL_OFFICE = 'medical_office'
    GYM = 'gym'


class Structure(DB.Model):
    """Base class for Structures."""

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    name = DB.Column(DB.String(50), nullable=False)
    description = DB.Column(DB.String(300))
    structure_type = DB.Column(DB.Enum(StructureType))
    geom = DB.Column(Geometry, nullable=False)

    user_id = DB.Column(DB.Integer, DB.ForeignKey("user.id"))

    __mapper_args__ = {'polymorphic_on': structure_type}

    @property
    def geometry(self):
        """Get geometry as GeoJSON object"""
        return geojson.loads(DB.session.scalar(func.ST_AsGeoJSON(self.geom)))

    @geometry.setter
    def geometry(self, geometry):
        """Set geometry from GeoJSON object"""
        self.geom = func.ST_GeomFromGeoJSON(geometry)

    @property
    def type(self):
        """Get structure type as string"""
        return self.structure_type.value

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.name)
