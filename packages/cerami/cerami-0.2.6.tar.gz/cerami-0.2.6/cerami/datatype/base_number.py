from .base_datatype import DynamoDataType
from .mapper import NumberMapper
from .expression import ArithmeticExpression

class BaseNumber(DynamoDataType):
    """A Base class for all Number datatypes"""

    def __init__(self, mapper_cls=NumberMapper, default=None, column_name=""):
        """constructor for the BaseNumber

        Parameters:
            default: a default value for the column. It can be a value or function
            column_name: a string defining the name of the column on the table
            mapper_cls: A mapper class to manipulate data to/from dynamodb.
                Defaults to the NumberMapper
        """
        super(BaseNumber, self).__init__(
            mapper_cls=mapper_cls,
            condition_type="N",
            default=default,
            column_name=column_name)

    def add(self, value):
        """add value to number for an UpdateRequest

        Parameters:
            value: a number to add

        Returns:
            An ArithmeticExpression

        For example::

            Person.update.key(Person.email.eq("test@test.com")).set(Person.age.add(10))
        """
        return ArithmeticExpression('+', self, value)

    def subtract(self, value):
        """subtract value from number for an UpdateRequest

        Parameters:
            value: a number to subtract

        For example::

            Person.update \\
                .key(Person.email.eq("test@test.com")) \\
                .set(Person.age.subtract(10))
        """
        return ArithmeticExpression('-', self, value)
