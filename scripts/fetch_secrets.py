import json
import os
import shlex
import sys

import boto3

# Get required environment variables
try:
    region = os.environ["AWS_REGION_NAME"]
    secret_id = os.environ["AWS_SECRET_MANAGER_NAME"]
except KeyError as e:
    print(f"Error: Missing environment variable {e}", file=sys.stderr)
    sys.exit(1)

# Setup AWS client using default credentials (from IAM role)
session = boto3.session.Session(region_name=region)
client = session.client("secretsmanager")

# Fetch and process secrets
try:
    print(f"# Fetching secrets from {secret_id}", file=sys.stderr)
    response = client.get_secret_value(SecretId=secret_id)
    secret_data = json.loads(response["SecretString"])

    # Output as shell export commands
    for key, value in secret_data.items():
        quoted_value = shlex.quote(str(value))
        print(f"export {key}={quoted_value}")

    print(f"# Successfully loaded {len(secret_data)} secrets", file=sys.stderr)
except Exception as e:  # noqa: BLE001
    print(f"Error fetching secrets: {e}", file=sys.stderr)
    sys.exit(1)
