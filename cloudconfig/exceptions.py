class BucketDoesNotExistException(Exception):

    def __init__(self, bucket_name):
        msg = ("The bucket '{bucket_name}' was not found. Make sure that the "
               "bucket exists, and that the current AWS user has access to "
               "it.").format(bucket_name=bucket_name)

        super().__init__(msg)


class NotImplementedWarning(RuntimeWarning):
    pass
