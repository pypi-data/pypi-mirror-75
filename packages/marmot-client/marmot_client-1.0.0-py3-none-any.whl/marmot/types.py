from enum import Enum, unique

@unique
class TypeClass(Enum):
    NULL = 0
    BYTE = 1; SHORT = 2; INT = 3; LONG = 4
    FLOAT = 5; DOUBLE = 6
    BOOLEAN = 7; STRING = 8; BINARY = 9
    DATE = 10; TIME = 11; DATETIME = 12
    COORDINATE = 13; ENVELOPE = 14
    POINT = 15; MULTI_POINT = 16; LINESTRING = 17; MULTI_LINESTRING = 18
    POLYGON = 19; MULTI_POLYGON = 20; GEOM_COLLECTION = 21; GEOMETRY = 22
    LIST = 23
    RECORD = 24

class DataType:
    def __init__(self, id, tc):
        self.id = id
        self.tc = tc

    def display_name(self):
        raise NotImplementedError
    def isPrimitiveType(self):
        return False
    def isGeometryType(self):
        return False

    @staticmethod
    def from_type_index(idx):
        try:
            return IDX_TO_TYPES[int(idx)]
        except ValueError:
            import re
            pat = re.compile('(\d+)\((\d+)\)')
            matches = pat.search(idx)
            geom_type = IDX_TO_TYPES[int(matches.group(1))]
            srid = 'EPSG:' + matches.group(2)
            return geom_type.duplicate(srid)

class PrimitiveType(DataType):
    def __init__(self, tc):
        super().__init__('{0}'.format(tc.value), tc)

    def display_name(self):
        return self.tc.name
    def isPrimitiveType(self):
        return True

    def __str__(self):
        return self.display_name()
    def __repr__(self):
        return self.display_name()

class GeometryDataType(DataType):
    def __init__(self, tc, srid):
        super().__init__('{0}'.format(tc.value), tc)
        self.srid = srid
        self.display_name = self.__encode_type_name(tc, srid)

    def get_display_name(self):
        return '{0}({1})'.format(self.tc.name, self.srid)
    def isGeometryType(self):
        return True
    
    def duplicate(self, srid):
        return GeometryDataType(self.tc, srid)

    def __str__(self):
        return self.get_display_name()

    def __repr__(self):
        return self.get_display_name()

    @staticmethod
    def __encode_type_id(tc, srid):
        if ( srid.startswith('EPSG:') ):
            srid = srid[5:]
        return '{0}({1})'.format(tc.value, srid)

    @staticmethod
    def __encode_type_name(tc, srid):
        if srid is None:
            srid = '?'
        elif ( srid.startswith('EPSG:') ):
            srid = srid[5:]
        return '{0}({1})'.format(tc.name, srid)

class ListType(DataType):
    def __init__(self, elm_type):
        super().__init__('[{0}]'.format(elm_type.id), TypeClass.LIST)
        self.elm_type = elm_type
        self.display_name = 'list[{0}]'.format(elm_type.display_name)

    def display_name(self):
        return self.display_name

class RecordType(DataType):
    def __init__(self, schema):
        super().__init__('[{0}]'.format(elm_type.id), TypeClass.LIST)
        self.schema = schema
        self.display_name = 'list[{0}]'.format(elm_type.display_name)

    def display_name(self):
        return self.display_name

    @staticmethod
    def __encode_type_id(tc, srid):
        pass

from datetime import datetime, time, date
NULL = PrimitiveType(TypeClass.NULL)
BYTE = PrimitiveType(TypeClass.BYTE)
SHORT = PrimitiveType(TypeClass.SHORT)
INT = PrimitiveType(TypeClass.INT)
LONG = PrimitiveType(TypeClass.LONG)
FLOAT = PrimitiveType(TypeClass.FLOAT)
DOUBLE = PrimitiveType(TypeClass.DOUBLE)
STRING = PrimitiveType(TypeClass.STRING)
BOOLEAN = PrimitiveType(TypeClass.BOOLEAN)
BINARY = PrimitiveType(TypeClass.BINARY)
DATETIME = PrimitiveType(TypeClass.BINARY)
DATE = PrimitiveType(TypeClass.BINARY)
TIME = PrimitiveType(TypeClass.BINARY)
COORDINATE = PrimitiveType(TypeClass.COORDINATE)
ENVELOPE = PrimitiveType(TypeClass.ENVELOPE)

POINT = GeometryDataType(TypeClass.POINT, None)
MULTI_POINT = GeometryDataType(TypeClass.MULTI_POINT, None)
LINESTRING = GeometryDataType(TypeClass.LINESTRING, None)
MULTI_LINESTRING = GeometryDataType(TypeClass.MULTI_LINESTRING, None)
POLYGON = GeometryDataType(TypeClass.POLYGON, None)
MULTI_POLYGON = GeometryDataType(TypeClass.MULTI_POLYGON, None)
GEOM_COLLECTION = GeometryDataType(TypeClass.GEOM_COLLECTION, None)
GEOMETRY = GeometryDataType(TypeClass.GEOMETRY, None)

IDX_TO_TYPES = [
    NULL, BYTE, SHORT, INT, LONG, FLOAT, DOUBLE, STRING,
    BOOLEAN, BINARY, DATETIME, DATE, TIME, COORDINATE, ENVELOPE,
    POINT, MULTI_POINT, LINESTRING, MULTI_LINESTRING, POLYGON,
    MULTI_POLYGON, GEOM_COLLECTION, GEOMETRY
]

NAME_TO_PRIMITIVE_TYPES = {
    'NULL': NULL,
    'BYTE': BYTE, 'SHORT': SHORT, 'INT': INT, 'LONG': LONG,
    'FLOAT': FLOAT, 'DOUBLE': DOUBLE,
    'STRING': STRING, 'BOOLEAN': BOOLEAN, 'BINARY': BINARY,
    'DATETIME': DATETIME, 'DATE': DATE, 'TIME': TIME,
    'COORDINATE': COORDINATE, 'ENVELOPE': ENVELOPE }


from collections import namedtuple
Coordinate = namedtuple("Coordinate", 'x y')
Envelope = namedtuple("Envelope", 'tl br')