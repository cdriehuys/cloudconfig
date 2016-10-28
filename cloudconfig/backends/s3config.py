import logging
from io import BytesIO

import boto3
from botocore.exceptions import ClientError

import yaml


from cloudconfig.backends import BaseConfig
from cloudconfig.exceptions import BucketDoesNotExistException


class S3Config(BaseConfig):
    ENCODING = 'utf-8'

    def __init__(self, bucket_name, config_name, logger=None):
        """
        Create a new S3Config instance.

        Args:
            bucket_name (str):
                The name of the S3 bucket that the config file is saved
                in.
            config_name (str):
                The name of the config file to load data from.
            logger:
                The logger to use for the class. If it is not provided,
                one will be created.
        """
        super(S3Config, self).__init__()

        self.bucket_name = bucket_name
        self.config_name = config_name
        self.logger = logger or logging.getLogger(__name__)

        self.client = boto3.client('s3')
        self.resource = boto3.resource('s3')
        self._validate_bucket()

        # Since bucket has been validated, we can attempt to load our data.
        self.load()

        self.logger.debug(("Created S3Config instance with bucket '{bucket}' "
                           "and file '{file}'.").format(
                                bucket=self.bucket_name,
                                file=self.config_name))

    def load(self):
        """
        Load the data from the remote config file.

        Returns:
            str:
                The contents of the remote config file. If the file
                could not be opened, an empty string is returned.
        """
        try:
            self.resource.meta.client.head_object(
                Bucket=self.bucket_name,
                Key=self.config_name)
        except ClientError as e:
            error_code = int(e.response['Error']['Code'])

            if error_code == 404:
                self.logger.info("Could not read remote config file.")
                self.data = {}

                return

            self.logger.exception('Error reading remote config', exc_info=e)

            raise e

        handle = BytesIO()
        self.client.download_fileobj(
            self.bucket_name,
            self.config_name,
            handle)

        serializer = self.get_serializer()
        self.data = serializer.deserialize(handle.getvalue().decode('utf-8'))

    def save(self):
        """
        Save the currently stored data to S3.
        """
        serializer = self.get_serializer()

        handle = BytesIO()
        handle.write(serializer.serialize(self.data).encode(self.ENCODING))
        handle.seek(0)

        self.client.upload_fileobj(
            handle,
            self.bucket_name,
            self.config_name,)

    def _validate_bucket(self):
        """
        Validate that the instance's bucket exists.

        Raises:
            BucketDoesNotExistException:
                if the instance's bucket does not exist.
        """
        try:
            self.resource.meta.client.head_bucket(Bucket=self.bucket_name)
        except ClientError as e:
            error_code = int(e.response['Error']['Code'])

            if error_code == 404:
                new_error = BucketDoesNotExistException(self.bucket_name)
                self.logger.exception(
                    "Could not find bucket.",
                    exc_info=new_error)

                raise new_error

            self.logger.exception(
                "Error trying to validate bucket.",
                exc_info=e)

            raise e
