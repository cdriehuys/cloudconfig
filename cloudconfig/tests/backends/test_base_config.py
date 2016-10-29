from unittest import mock

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

    def test_get_nested(self):
        """Test getting nested data.

        By passing multiple arguments to the get method, we should be
        able to retrieve nested data.
        """
        conf = BaseConfig()
        conf.data = {'foo': {'bar': 'baz'}}

        assert conf.get('foo', 'bar') == conf.data['foo']['bar']

    def test_get_none(self):
        """Test passing no key to `get`.

        If no key is passed in, a `ValueError` should be raised.
        """
        conf = BaseConfig()

        with pytest.raises(ValueError):
            conf.get()

    def test_get_serializer(self):
        """Test getting the serializer for the instance.

        The method should return the `serializer_class` attribute of
        the config class.
        """
        conf = BaseConfig()

        with mock.patch.object(
                conf, 'serializer_class') as mock_serializer:
            serializer = conf.get_serializer()

        assert serializer == mock_serializer

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
