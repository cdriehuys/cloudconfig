import configparser
from io import BytesIO

import boto3


LOCAL_CONFIG_FILE = '.cloudconfigrc'
LOCAL_CONFIG_SECTION = 'cloudconfig'


def get_bucket_name(local_config):
    if local_config.get('bucket_name'):
        return local_config.get('bucket_name')

    return input("Bucket name: ")


def get_config_name(local_config):
    if local_config.get('config_name'):
        return local_config.get('config_name')

    return input("Config name: ")


def load_local_config():
    """Read and return the local config file"""
    config = configparser.ConfigParser()
    config.read(LOCAL_CONFIG_FILE)

    if LOCAL_CONFIG_SECTION in config:
        return config[LOCAL_CONFIG_SECTION]

    return {}


def read_cloud_config(bucket_name, config_name):
    """Read a configuration file from S3.

    Args:
        bucket_name (str):
            The name of the S3 bucket that the config file is located
            in.
        config_name (str):
            The name of the config file to be read.

    Returns:
        bytes:
            The content of the config file.
    """
    s3 = boto3.client('s3')

    handle = BytesIO()
    s3.download_fileobj(bucket_name, config_name, handle)
    print(handle.getvalue())


if __name__ == '__main__':
    config = load_local_config()

    bucket_name = get_bucket_name(config)
    config_name = get_config_name(config)

    print(read_cloud_config(bucket_name, config_name))
