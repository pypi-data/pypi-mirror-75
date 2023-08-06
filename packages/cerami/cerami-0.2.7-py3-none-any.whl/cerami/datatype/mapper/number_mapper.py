from .string_mapper import StringMapper
from .base_datatype_mapper import BaseDatatypeMapper

class NumberMapper(BaseDatatypeMapper):
    """A Mapper class for converting number fields into DynamoDB dictionaries

    At the moment, NumberMappers only support integers. The reconstruction process will
    automatically cast any value as in int.

    For example::

        mapper = NumberMapper(Number())
        mapper.map(30)
        {'N': '30'}

        mapper.reconstruct({'N': '30'})
        30
    """
    def resolve(self, value):
        """convert the number into a string"""
        return str(value)

    def parse(self, value):
        """convert the value into an int"""
        return int(value)

