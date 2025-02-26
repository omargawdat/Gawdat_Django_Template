import json
import os
import shlex
import sys

import boto3

try:
    region = os.environ["AWS_SECRETS_REGION"]
    secret_id = os.environ["AWS_SECRET_ID"]
    access_key = os.environ["AWS_ACCESS_KEY_ID"]
    secret_key = os.environ["AWS_SECRET_ACCESS_KEY"]
except KeyError as e:
    print(f"Error: Missing environment variable {e}", file=sys.stderr)
    sys.exit(1)

session = boto3.session.Session(
    aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region
)

client = session.client("secretsmanager")

try:
    response = client.get_secret_value(SecretId=secret_id)
    secret_data = json.loads(response["SecretString"])
    for key, value in secret_data.items():
        quoted_value = shlex.quote(value)
        print(f"export {key}={quoted_value}")
except Exception as e:  # noqa: BLE001
    print(f"Error fetching secrets: {e}", file=sys.stderr)
    sys.exit(1)
