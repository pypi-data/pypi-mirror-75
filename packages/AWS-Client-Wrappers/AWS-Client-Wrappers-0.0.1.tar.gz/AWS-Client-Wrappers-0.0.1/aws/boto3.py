import base64
import json
import logging

import boto3
from botocore.exceptions import ClientError

API = 'secretsmanager'
REGION = 'eu-west-1'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def _get_client():
    # Create a Secrets Manager client
    session = boto3.session.Session()#profile_name='bns')
    client = session.client(
        service_name=API,
        region_name=REGION,
    )
    return client


def _secret_fetch(key):
    client = _get_client()
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=key
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            return json.loads(get_secret_value_response['SecretString'])
        else:
            return base64.b64decode(get_secret_value_response['SecretBinary'])


def get_application_secret(secret_key):
    if not secret_key:
        raise ValueError('Needs a secrets key. Please provide a key')
    return _secret_fetch(secret_key)


def get_database_secret():
    secret_name = "prod/mysql"
    return _secret_fetch(secret_name)
