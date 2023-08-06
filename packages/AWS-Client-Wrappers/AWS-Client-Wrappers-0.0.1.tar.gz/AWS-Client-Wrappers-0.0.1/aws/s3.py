from typing import Optional

import boto3
import botocore

from aws.base import AWSClientBase

AWSS3_PUBLIC_URL = 'https://s3-{}.amazonaws.com/{}/{}'


class S3Client(AWSClientBase):

    def __init__(self):
        super().__init__()
        self.client = self.session.client('s3')
        self.llclient = boto3.client('s3', config=botocore.client.Config(signature_version=botocore.UNSIGNED))

    def list_dirs(self, bucket, prefix=''):
        if prefix != '':
            prefix = prefix + '/'
        response = self.llclient.list_objects(
            Bucket=bucket,
            Prefix=prefix,
            Delimiter='/'
        )
        folders = [i.get('Prefix') for i in response.get('CommonPrefixes')]
        return folders

    def list_objects(self, bucket, prefix=''):
        return self.client.list_objects(Bucket=bucket, Prefix=prefix).get('Contents', None)

    def make_public_url(self, bucket_name, key):
        """
        Gets the public URL from the bucket name and object key

        :param bucket_name: S3 bucket name
        :param key: object key
        :return:
        """
        bucket_location = self.client.get_bucket_location(Bucket=bucket_name)
        path = AWSS3_PUBLIC_URL.format(bucket_location['LocationConstraint'], bucket_name, key)
        return path

    def presigned_post(self, bucket, key, acl=None):
        if acl is None:
            acl = [{'acl': 'public-read'}]
        return self.client.generate_presigned_post(bucket, key, Conditions=acl)

    def delete(self, bucket, key) -> bool:
        """
        Handles the delete operation for bucket objects.

        :param bucket: S3 bucket name
        :param key: Object key within the bucket
        :return: operation status
        :rtype bool
        """

        status = self.client.delete_object(bucket=bucket, key=key)
        return status.get('DeleteMarker')

    def upload(self, path, image, bucket, target_path=None, geturl=False, public=False) -> Optional[str]:
        """
        Handles the upload procedure from local filesystem to S3 bucket. This API splits up
        large files automatically. Parts are then uploaded in parallel.

        :param path: The path where the file is located
        :param image: The filename and extension
        :param bucket: The bucket name that we wish to post to
        :param target_path: The directory within the bucket. I.e <bucket>/images/
        :param geturl: Whether to return the public URL of the object uploaded

        :return: The S3 public access URL for the image once uploaded
        :rtype str
        """

        if not target_path:
            target_path = ''

        source = '{}{}'.format(path, image)

        if target_path[-1] != '/':
            target_path = target_path + '/'
        s3target = '{}{}'.format(target_path, image)

        args = {}
        if public:
            args = {'ACL': 'public-read'}
        self.client.upload_file(source, bucket, s3target, ExtraArgs=args)

        if geturl:
            return self.__make_public_url(bucket, s3target)
        return True
