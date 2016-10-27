import configparser

from cloudconfig.backends import S3Config

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


if __name__ == '__main__':
    config = load_local_config()

    bucket_name = get_bucket_name(config)
    config_name = get_config_name(config)

    proj_conf = S3Config(bucket_name, config_name)

    print(proj_conf.get('foo'))
    print(proj_conf.get('bar'))
