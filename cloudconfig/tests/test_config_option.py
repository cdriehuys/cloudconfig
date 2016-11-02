import pytest

from cloudconfig.backends import BaseConfig
from cloudconfig.core import ConfigOption


class TestConfigOption(object):
    """Test cases for the config option class"""

    def test_create_child(self):
        """Test creating a config option that is a child of another.

        Config options should be creatable with another config option
        as its parent class.
        """
        conf = BaseConfig()
        parent = ConfigOption(conf)
        child = ConfigOption(parent)

        assert child.data == {}
        assert child.parent == parent
        assert child.value is None

    def test_create_invalid_parent(self):
        """Test creating a config option with an invalid parent.

        If the parent is not of the correct type, an AssertionError
        should be raised.
        """
        with pytest.raises(AssertionError):
            ConfigOption(3)

    def test_create_top_level(self):
        """Test creating a config option as a top-level child.

        Config options should be creatable with a subclass of
        `BaseConfig` as its parent.
        """
        conf = BaseConfig()
        opt = ConfigOption(conf)

        assert opt.data == {}
        assert opt.parent == conf
        assert opt.value is None

    def test_create_with_value(self):
        """Test creating an option with a value.

        Config options should be able to store a value as well as child
        data.
        """
        conf = BaseConfig()
        opt = ConfigOption(conf, 'foo')

        assert opt.data == {}
        assert opt.value == 'foo'

    def test_get(self):
        """Test getting data from a config option.

        The get method should return the data at the given key.
        """
        conf = BaseConfig()
        opt = ConfigOption(conf)
        opt.data['foo'] = 'bar'

        assert opt.get('foo') == 'bar'

    def test_get_missing(self):
        """Test getting data at a non-existent key.

        If the key doesn't exist, `None` should be returned.
        """
        conf = BaseConfig()
        opt = ConfigOption(conf)

        assert opt.get('foo') is None

    def test_magic_get(self):
        """Test getting data from a config option by subscript.

        Config option data should be accessible through subscripts.
        """
        conf = BaseConfig()
        opt = ConfigOption(conf)
        opt.data['foo'] = 'bar'

        assert opt['foo'] == 'bar'

    def test_magic_get_missing(self):
        """Test accessing a non-existent key.

        If the key doesn't exist, an empty config option should be
        created at that key and returned.
        """
        conf = BaseConfig()
        opt = ConfigOption(conf)

        val = opt['foo']

        assert val.value is None
        assert opt.data['foo'] is not None

    def test_magic_get_nested(self):
        """Test getting nested data by subscript.

        With nested config options, child data should be accessible
        from the parent option.
        """
        conf = BaseConfig()
        parent = ConfigOption(conf)
        child = ConfigOption(parent)
        parent.data['foo'] = child

        child.data['bar'] = 'baz'

        assert parent['foo']['bar'] == 'baz'

    def test_magic_set(self):
        """Test setting config option data via subscript.

        Config option data should be settable using subscripts.
        """
        conf = BaseConfig()
        opt = ConfigOption(conf)

        opt['foo'] = 'bar'

        assert isinstance(opt.data['foo'], ConfigOption)
        assert opt.data['foo'].value == 'bar'

    def test_magic_set_nested(self):
        """Test setting a nested config option.

        Setting a nested value should create missing config options.
        """
        conf = BaseConfig()
        opt = ConfigOption(conf)

        opt['foo']['bar'] = 'baz'

        assert isinstance(opt.data['foo'], ConfigOption)
        assert isinstance(opt.data['foo'].data['bar'], ConfigOption)

        assert opt.data['foo'].data['bar'].value == 'baz'
