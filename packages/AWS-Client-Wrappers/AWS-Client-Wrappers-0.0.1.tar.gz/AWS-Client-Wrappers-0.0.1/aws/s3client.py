from datetime import datetime

import boto3

# Create an S3 client
session = boto3.Session()
s3 = session.client('s3')

filename = 'file.txt'
target_path = 'public/images/{}/{}/'.format(datetime.now().year, datetime.strftime(datetime.now(), '%B').lower())
aws_public_path = 'https://s3-{}.amazonaws.com/{}/{}'


def make_public_url(bucket_name, key):
    bucket_location = s3.get_bucket_location(Bucket=bucket_name)
    path = aws_public_path.format(bucket_location['LocationConstraint'], bucket_name, key)
    return path


def upload(path, image, bucket):
    # Uploads the given file using a managed uploader, which will split up large
    # files automatically and upload parts in parallel.
    source = '{}{}'.format(path, image)
    s3.upload_file(source, bucket, target_path + image, ExtraArgs={'ACL': 'public-read'})
    return make_public_url(bucket, target_path + image)
