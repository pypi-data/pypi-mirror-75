import boto3


class AWSClientBase:

    def __init__(self, profile=None):
        if profile:
            self.session = boto3.session.Session(profile_name=profile)
        else:
            self.session = boto3.session.Session()
