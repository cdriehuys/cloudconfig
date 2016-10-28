import warnings

from cloudconfig.exceptions import NotImplementedWarning
from cloudconfig.serializers import BaseSerializer
from cloudconfig.serializers import YAMLSerializer


class BaseConfig(object):
    """The base for all configuration classes."""
    serializer_class = YAMLSerializer       # type: BaseSerializer

    def __init__(self):
        """
        Initialize data to be an empty dict.
        """
        self.data = {}

    def get(self, key):
        """
        Get the data with the specified key.

        Args:
            key (str):
                The key of the data to pull from the config instance.

        Returns:
            str:
                The data at the specified key if it exists, `None`
                otherwise.
        """
        return self.data.get(key)

    def get_serializer(self) -> BaseSerializer:
        """
        Get the serializer class to use for this config instance.

        Returns:
            The serializer class to use for the instance.
        """
        return self.serializer_class

    def load(self):
        """
        Load the data for the given config instance.

        This should be implemented by the child class.
        """
        warnings.warn('This method is not implemented in this backend.',
                      NotImplementedWarning)

    def save(self):
        """
        Save the data currently stored in the instance.

        This should be implemented by the child class.
        """
        warnings.warn('This method is not implemented in this backend.',
                      NotImplementedWarning)
