import gzip
import os
from io import BytesIO, StringIO, TextIOWrapper
from os.path import dirname
from os import makedirs

import boto3
s3 = boto3.client('s3')

from .base import Base


class AWSLambda(Base):
    def __init__(self, bucket, filename):
        self.bucket = bucket
        super().__init__(filename)

    def open_for_read(self):
        print(self.bucket, self.filename)
        obj = s3.get_object(Bucket=self.bucket, Key=self.filename)
        return TextIOWrapper(gzip.GzipFile(fileobj=obj['Body'], mode='r'))

    def put_to_s3(self, path, data):
        return s3.put_object(
            Bucket=self.bucket,
            Key=path,
            Body=gzip.compress(bytearray(data, 'utf-8'))
        )

class S3File(BytesIO):
    def __init__(self, bucket, key):
        self.bucket = bucket
        self.key = key
        super().__init__(b'')

    def close(self):
        print(self.bucket, self.key, len(self))
        super().close()
        super().seek(0)
        s3.put_object(Bucket=self.bucket, Key=self.key, Body=self, storage_class="STANDARD_IA")
        print("putted")
