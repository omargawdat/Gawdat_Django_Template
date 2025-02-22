import json
import os

import boto3

from config.env_settings import EnvSettings


def load_aws_secrets():
    """Load AWS Secrets into the environment variables if they exist"""
    region = os.getenv("AWS_SECRETS_REGION")
    secret_id = os.getenv("AWS_SECRET_ID")
    if not region or not secret_id:
        return

    client = boto3.Session().client("secretsmanager", region_name=region)
    response = client.get_secret_value(SecretId=secret_id)
    secrets_dict = json.loads(response["SecretString"])
    print("Loaded AWS Secrets into environment variables", secrets_dict)
    for key, value in secrets_dict.items():
        os.environ[key.lower()] = str(value)


try:
    load_aws_secrets()
except Exception:  # noqa: BLE001
    print("Could not load AWS Secrets into environment variables")

env = EnvSettings()
