from tests.helpers.testbase import TestBase
from cerami.datatype import Boolean
from cerami.datatype.mapper import BooleanMapper

class TestBooleanMapper(TestBase):
    def setUp(self):
        self.dt = Boolean()
        self.mapper = BooleanMapper(self.dt)

    def test_resolve(self):
        """it returns 1 for True 0 for False"""
        assert self.mapper.resolve(True) == 1
        assert self.mapper.resolve(False) == 0

    def test_parse(self):
        """it returns True for truthy values False for falsey values"""
        assert self.mapper.parse(1)
        assert not self.mapper.parse(0)

