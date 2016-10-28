import yaml

from cloudconfig.serializers import BaseSerializer


class YAMLSerializer(BaseSerializer):
    """
    Serializer for YAML.
    """

    @staticmethod
    def deserialize(data: str) -> dict:
        """
        Deserialize the given YAML into a dict.

        Args:
            data:
                The data to deserialize.

        Returns:
            A dict with the same information that was in the YAML data.
        """
        return yaml.load(data)

    @staticmethod
    def serialize(data: dict) -> str:
        """
        Serialize the given data into YAML.

        Args:
            data:
                The data to serialize.

        Returns:
            The specified data in YAML format.
        """
        return yaml.dump(data)
