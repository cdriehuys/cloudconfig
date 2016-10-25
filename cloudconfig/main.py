from io import BytesIO

import boto3


def get_bucket_name():
    return input("Bucket name: ")


def get_config_name():
    return input("Config name: ")


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
    bucket_name = get_bucket_name()
    config_name = get_config_name()

    print(read_cloud_config(bucket_name, config_name))
