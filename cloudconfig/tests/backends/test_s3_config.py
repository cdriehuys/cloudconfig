from io import BytesIO
from unittest import mock

import boto3
import yaml
from botocore.exceptions import ClientError

import pytest

from cloudconfig.backends import S3Config
from cloudconfig.exceptions import BucketDoesNotExistException


def mock_downloadobj(bucket_name, config_name, handle):
    handle.write('foo: bar'.encode('utf-8'))


class TestS3Config(object):
    """Test cases for the S3Config class"""

    def setup_method(self):
        """Mock out bucket validation."""
        self.load = S3Config.load
        self.save = S3Config.save
        self._validate_bucket = S3Config._validate_bucket
        S3Config.load = mock.MagicMock(autospec=True)
        S3Config.save = mock.MagicMock(autospec=True)
        S3Config._validate_bucket = mock.MagicMock(autospec=True)

    def teardown_method(self):
        """Restore mocked methods."""
        S3Config.load = self.load
        S3Config.save = self.save
        S3Config._validate_bucket = self._validate_bucket

    def test_create(self):
        """Test creating an S3Config instance.

        The config instance should take a bucket name and file name. It
        should create an S3 client and verify that the bucket exists.
        """
        conf = S3Config('test-bucket', 'test-config')

        assert conf.load.call_count == 1
        assert conf._validate_bucket.call_count == 1

        assert isinstance(
            conf.resource,
            boto3.resources.base.ServiceResource)
        assert conf.bucket_name == 'test-bucket'
        assert conf.config_name == 'test-config'

    def test_load_remote(self):
        """Test loading from the remote config file.

        This method should check if the remote file exists and then attempt to
        download the file.
        """
        conf = S3Config('test-bucket', 'test-config')
        S3Config.load = self.load

        conf.resource.meta.client.head_object = mock.MagicMock(autospec=True)
        conf.client.download_fileobj = mock.MagicMock(
            autospec=True,
            side_effect=mock_downloadobj)

        conf.load()

        assert conf.data == {'foo': 'bar'}

        assert conf.resource.meta.client.head_object.call_count == 1

        _, kwargs = conf.resource.meta.client.head_object.call_args
        assert kwargs['Bucket'] == conf.bucket_name
        assert kwargs['Key'] == conf.config_name

        assert conf.client.download_fileobj.call_count == 1

        args, _ = conf.client.download_fileobj.call_args
        assert conf.bucket_name in args
        assert conf.config_name in args

    def test_load_remote_not_found(self):
        """Test behaviour when the remote config file is not found.

        If the remote file cannot be read, an emtpy string should be
        returned.
        """
        conf = S3Config('test-bucket', 'fake-config')
        S3Config.load = self.load

        conf.resource.meta.client.head_object = mock.MagicMock(
            autospec=True,
            side_effect=ClientError({'Error': {'Code': 404}}, 'test op'))
        conf.client.download_fileobj = mock.MagicMock(autospec=True)

        conf.load()

        assert conf.data == {}

        assert conf.resource.meta.client.head_object.call_count == 1
        assert conf.client.download_fileobj.call_count == 0

    def test_save(self):
        """Test saving the config object.

        Saving the object should upload its contents to S3.
        """
        conf = S3Config('test-bucket', 'test-config')
        conf.data = {'foo': 'bar'}
        S3Config.save = self.save

        conf.client.upload_fileobj = mock.MagicMock(autospec=True)

        conf.save()

        assert conf.client.upload_fileobj.call_count == 1

        args, _ = conf.client.upload_fileobj.call_args
        assert args[1] == conf.bucket_name
        assert args[2] == conf.config_name

        expected_handle = BytesIO()
        expected_handle.write(yaml.dump(conf.data).encode('utf-8'))

        assert args[0].getvalue() == expected_handle.getvalue()

    def test_validate_bucket(self):
        """Test validating a bucket.

        If the meta info call succeeds, the bucket should be reported
        as valid.
        """
        conf = S3Config('test-bucket', 'test-config')
        S3Config._validate_bucket = self._validate_bucket

        conf.resource.meta.client.head_bucket = mock.MagicMock(autospec=True)

        conf._validate_bucket()

        assert conf.resource.meta.client.head_bucket.call_count == 1

    def test_validate_bucket_invalid(self):
        """Test validating an invalid bucket.

        If the meta info call returns a client error with a code other
        than 404, the exception should be raised.
        """
        conf = S3Config('test-bucket', 'test-config')
        S3Config._validate_bucket = self._validate_bucket

        conf.resource.meta.client.head_bucket = mock.MagicMock(
            autospec=True,
            side_effect=ClientError({'Error': {'Code': 403}}, 'test op'))

        with pytest.raises(ClientError):
            conf._validate_bucket()

        assert conf.resource.meta.client.head_bucket.call_count == 1

    def test_validate_bucket_not_found(self):
        """Test validating a bucket that returns a 404 error.

        If the meta info call returns a client error with a code of 404
        then a BucketDoesNotExist exception should be raised.
        """
        conf = S3Config('test-bucket', 'test-config')
        S3Config._validate_bucket = self._validate_bucket

        conf.resource.meta.client.head_bucket = mock.MagicMock(
            autospec=True,
            side_effect=ClientError({'Error': {'Code': 404}}, 'test op'))

        with pytest.raises(BucketDoesNotExistException):
            conf._validate_bucket()

        assert conf.resource.meta.client.head_bucket.call_count == 1
