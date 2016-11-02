from cloudconfig.backends import BaseConfig


class ConfigOption(object):
    """
    Storage container for configuration options.

    A `ConfigOption` can be a child of a `BaseConfig` instance (or some
    subclass), or a child of another `ConfigOption` instance.

    The class serves as both a container for a value, and as a
    container for other config options. This allows it to serve as a
    leaf in the configuration tree, or some other node.
    """

    def __init__(self, parent, value=None):
        """
        Create a new `ConfigOption` instance.

        Args:
            parent (BaseConfig,ConfigOption):
                The parent of the instance. This can be an instance of
                `BaseConfig`, or another `ConfigOption` instance.
            value:
                The value to store in the instance.

        Raises:
            AssertionError:
                If `parent` is not an instance of `BaseConfig` or
                `ConfigOption`.
        """
        assert isinstance(parent, (BaseConfig, ConfigOption))

        self.parent = parent
        self.value = value

        self.data = {}

    def __getitem__(self, key):
        """
        Get the data at `key`.

        Args:
            key:
                The key to retrieve data from.

        Returns:
            The data at `key`. If that key doesn't exist, *it is
            created*, and `None` is returned.
        """
        if key not in self.data:
            self.data[key] = ConfigOption(self)

        return self.data[key]

    def __setitem__(self, key, value):
        """
        Set the data at `key` to `value`.

        Args:
            key:
                The key to store `value` at.
            value:
                The value to store.
        """
        self.data[key] = ConfigOption(self, value)

    def get(self, key):
        """
        Get the data at `key`.

        Args:
            key:
                The key to retrieve data from.

        Returns:
            The data at `key` if it exists, `None` otherwise.
        """
        return self.data.get(key)
