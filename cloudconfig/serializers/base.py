import warnings

from cloudconfig.exceptions import NotImplementedWarning


class BaseSerializer(object):
    """
    Base class for all serializers.
    """

    @staticmethod
    def serialize(data: dict) -> str:
        """
        Serialize the given data into a string.

        This should be implemented by a child class.

        Args:
            data:
                The data to serialize.

        Returns:
            An empty string.
        """
        warnings.warn("This method has no effect.", NotImplementedWarning)

        return ''

    @staticmethod
    def deserialize(data: str) -> dict:
        """
        Deserialize the given data.

        This should be implemented by the child class.

        Args:
            data:
                The data to deserialize.

        Returns:
            An empty dictionary.
        """
        warnings.warn("This method has no effect.", NotImplementedWarning)

        return {}
