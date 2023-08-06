from .base_datatype_mapper import BaseDatatypeMapper

class BooleanMapper(BaseDatatypeMapper):
    """A Mapper class for converting fields into DynamoDB booleans

    For example::
    
        mapper = BooleanMapper(Boolean())
        mapper.map(True)
        {'BOOL': 1}

        mapper.reconstruct({'BOOL': 1})
        True
    """

    def resolve(self, value):
        return 1 if bool(value) else 0

    def parse(self, value):
        return bool(value)
