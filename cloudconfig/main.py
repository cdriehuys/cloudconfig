import configparser
from io import BytesIO

import boto3

import yaml


LOCAL_CONFIG_FILE = '.cloudconfigrc'
LOCAL_CONFIG_SECTION = 'cloudconfig'


class Config(object):

    def get(self, key):
        """Get the data with the given key"""
        return self.config[key]

    def load(self, raw_data):
        """Parse YAML data"""
        self.config = yaml.load(raw_data)


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

    return handle.getvalue().decode('utf-8')


if __name__ == '__main__':
    config = load_local_config()

    bucket_name = get_bucket_name(config)
    config_name = get_config_name(config)

    proj_conf = Config()
    proj_conf.load(read_cloud_config(bucket_name, config_name))

    print(proj_conf.get('foo'))
