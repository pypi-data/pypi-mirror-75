from .base_datatype import DynamoDataType
from .mapper import StringMapper

class BaseString(DynamoDataType):
    """A Base class for all String datatypes"""

    def __init__(self, mapper_cls=StringMapper, default=None, column_name=""):
        """constructor for the BaseString

        Parameters:
            default: a default value for the column. It can be a value or function
            column_name: a string defining the name of the column on the table
            mapper_cls: A mapper class to manipulate data to/from dynamodb.
                Defaults to the StringMapper
        """
        super(BaseString, self).__init__(
            mapper_cls=mapper_cls,
            condition_type="S",
            default=default,
            column_name=column_name)
