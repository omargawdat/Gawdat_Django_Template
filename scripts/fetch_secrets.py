import json
import os
import shlex

import boto3

region = os.environ["AWS_REGION_NAME"]
secret_id = os.environ["AWS_SECRET_MANAGER_NAME"]


session = boto3.session.Session(region_name=region)
client = session.client("secretsmanager")

response = client.get_secret_value(SecretId=secret_id)
secret_data = json.loads(response["SecretString"])


# Output as shell export commands
for key, value in secret_data.items():
    quoted_value = shlex.quote(str(value))
    print(f"export {key}={quoted_value}")
