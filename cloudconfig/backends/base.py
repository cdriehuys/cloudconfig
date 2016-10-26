import warnings

from cloudconfig.exceptions import NotImplementedWarning


class BaseConfig(object):
    """The base for all configuration classes."""

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

    def load(self, data):
        """
        Load the given data into the config instance.

        This should be implemented by the child class.

        Args:
            data (str):
                The data to load.
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
