import yaml

from cloudconfig.serializers import YAMLSerializer


class TestYAMLSerializer(object):
    """Test cases for the YAML serializer"""

    def test_deserialize(self):
        """Test deserializing YAML into a dict.

        Deserializing YAML should create a dict with the same
        information.
        """
        data = 'foo: bar\nbar: baz'
        expected = {
            'bar': 'baz',
            'foo': 'bar',
        }

        assert YAMLSerializer.deserialize(data) == expected

    def test_serialize(self):
        """Test serializing a dict to YAML.

        Serializing a dict should return its YAML representation.
        """
        data = {'foo': 'bar'}
        expected = yaml.dump(data)

        assert YAMLSerializer.serialize(data) == expected
