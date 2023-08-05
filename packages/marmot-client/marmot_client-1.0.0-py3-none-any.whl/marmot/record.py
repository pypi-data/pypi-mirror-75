from marmot.types import DataType
from collections import namedtuple, OrderedDict

class ColumnNotFound(Exception):
    def __init__(self, name):
        self.name = name

class ColumnExists(Exception):
    def __init__(self, name):
        self.name = name

Column = namedtuple("Column", 'name type ordinal')
class Columns:
    def __init__(self, columns):
        self.column_map = columns
        self.columns = list(columns.values())

    def __len__(self):
        return len(self.columns)

    def __iter__(self):
        return (col for col in self.columns)

    def __getitem__(self, idx):
        if type(idx) == str:
            return self.column_map[idx]
        else:
            return self.columns[idx]

    def __getattr__(self, name):
        return self.column_map[name]

class RecordSchema:
    def __init__(self, columns):
        self.columns = Columns(columns)
        self.display_name = self.__to_type_name()
        
    def __str__(self):
        return self.display_name
        
    def __to_type_name(self):
        return '{' + ','.join(['%s:%s'% col[0:2] for col in self.columns]) + '}'

    @staticmethod
    def from_type_id(type_id):
        col_expr_list = type_id[1:-1].split(",")

        builder = RecordSchemaBuilder()
        for col_expr in col_expr_list:
            parts = col_expr.split(":")
            type = DataType.from_type_index(parts[1])
            builder.add(parts[0], type)
        return builder.build()

class RecordSchemaBuilder:
    def __init__(self):
        self.columns = OrderedDict()
        self.__next_idx = 0

    def add(self, name, data_type):
        if name in self.columns:
            raise ColumnExists(name)
        self.columns[name] = Column(name, data_type, self.__next_idx)
        self.__next_idx += 1
        return self

    def build(self):
        return RecordSchema(self.columns)

class Record:
    def __init__(self, schema, values=None):
        self.schema = schema
        if values:
            self.values = values
        else:
            self.values = tuple(None for col in schema.columns)

    def __len__(self):
        return len(self.values)

    def __iter__(self):
        return iter(self.values)

    def __getitem__(self, idx):
        col = self.schema.columns[idx]
        if type(col) == Column:
            return self.values[col.ordinal]
        elif type(col) == list:
            return tuple(self.values[c.ordinal] for c in col)

    def __getattr__(self, name):
        col = self.schema.columns[name]
        return self.values[col.ordinal]
        
    def __repr__(self):
        return '(' + ', '.join(['%s:%s' % (col[0], self[col[2]]) for col in self.schema.columns]) + ')'
        
    def __str__(self):
        return '(' + ', '.join(['%s' % (self.values[col[2]]) for col in self.schema.columns]) + ')'
