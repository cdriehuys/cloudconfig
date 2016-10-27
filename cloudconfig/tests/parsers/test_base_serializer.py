import pytest

from cloudconfig.exceptions import NotImplementedWarning
from cloudconfig.serializers import BaseSerializer


class TestBaseSerializer(object):
    """Test cases for the base serializer."""

    def test_serialize(self):
        """Test serializing data with the base parser.

        For the base parser, this should emit a NotImplementedWarning.
        """
        with pytest.warns(NotImplementedWarning):
            dumped = BaseSerializer.serialize({'foo': 'bar'})

        assert dumped == ''

    def test_deserialize(self):
        """Test deserializing data.

        For the base parser, this should emit a NotImplementedWarning.
        """
        with pytest.warns(NotImplementedWarning):
            parsed = BaseSerializer.deserialize('foo: bar')

        assert parsed == {}
