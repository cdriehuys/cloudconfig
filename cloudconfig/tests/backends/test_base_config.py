import pytest

from cloudconfig.backends import BaseConfig
from cloudconfig.exceptions import NotImplementedWarning


class TestBaseConfig(object):
    """Test cases for the `BaseConfig` class"""

    def test_create(self):
        """Test creating a BaseConfig instance.

        Creating a BaseConfig instance should set its `data` attribute
        to `None`."""
        conf = BaseConfig()

        assert {} == conf.data

    def test_get(self):
        """Test getting data from a BaseConfig instance.

        Passing a key to the get method should return the data at that key.
        """
        conf = BaseConfig()
        conf.data['foo'] = 'bar'

        assert conf.data['foo'] == conf.get('foo')

    def test_get_missing(self):
        """Test getting a missing key

        If there is no data at the given key, `None` should be
        returned.
        """
        conf = BaseConfig()

        assert conf.get('foo') is None

    def test_load(self):
        """Test loading data into a BaseConfig instance.

        With the BaseConfig object, a `NotImplementedWarning` should be
        emitted.
        """
        conf = BaseConfig()

        with pytest.warns(NotImplementedWarning):
            conf.load()

    def test_save(self):
        """Test saving data with a BaseConfig instance.

        With the BaseConfig class, a 'NotImplementedWarning' should be
        emitted.
        """
        conf = BaseConfig()

        with pytest.warns(NotImplementedWarning):
            conf.save()
