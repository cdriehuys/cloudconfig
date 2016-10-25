from io import BytesIO

import boto3


def read_cloud_config():
    s3 = boto3.client('s3')

    bucket_name = input("Bucket name: ")
    config_name = input("Config name: ")

    handle = BytesIO()
    s3.download_fileobj(bucket_name, config_name, handle)
    print(handle.getvalue())


if __name__ == '__main__':
    read_cloud_config()
