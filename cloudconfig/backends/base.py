import warnings
from typing import List

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

    def get(self, *keys: List[str]):
        """
        Get the data with the specified key.

        The method allows for nested data to be retrieved by passing
        multiple keys in.

        Examples:
            Retrieving nested data::

                config.get('foo', 'bar')

            This returns the data at::

                config.data['foo']['bar']

        Args:
            keys:
                The keys that point to the object to fetch.

        Raises:
            ValueError:
                if the length of `keys` is 0.

        Returns:
            str:
                The data at the specified location if it exists, `None`
                otherwise.
        """
        if not len(keys):
            raise ValueError("There must be at least one key passed in.")

        data = self.data

        for i, key in enumerate(keys):
            val = data.get(key)

            if i + 1 == len(keys) or val is None:
                return val
            else:
                data = val

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
