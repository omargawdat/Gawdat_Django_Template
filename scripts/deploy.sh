#!/usr/bin/env bash
set -euo pipefail

# Parse command-line arguments
KEY=""
DOMAIN_NAME=""
PARENT_DOMAIN=""  # New variable for parent domain
ECR_IMAGE_IDENTIFIER=""
CONTAINER_PORT=""
S3_BUCKET_NAME=""
AWS_SECRET_MANAGER_NAME=""
DB_NAME=""
REGION=""
STATE_BUCKET=""
DYNAMODB_TABLE=""
APPRUNNER_ECR_ROLE_ARN=""
APPRUNNER_INSTANCE_ROLE_ARN=""

# Parse parameters
while [[ $# -gt 0 ]]; do
    case "$1" in
        --key)                   KEY="$2"; shift 2 ;;
        --domain-name)           DOMAIN_NAME="$2"; shift 2 ;;
        --parent-domain)         PARENT_DOMAIN="$2"; shift 2 ;;  # New parameter
        --ecr-image-identifier)  ECR_IMAGE_IDENTIFIER="$2"; shift 2 ;;
        --container-port)        CONTAINER_PORT="$2"; shift 2 ;;
        --media-bucket-name)     S3_BUCKET_NAME="$2"; shift 2 ;;
        --secret-manager-name)   AWS_SECRET_MANAGER_NAME="$2"; shift 2 ;;
        --db-name)               DB_NAME="$2"; shift 2 ;;
        --region)                REGION="$2"; shift 2 ;;
        --state-bucket)          STATE_BUCKET="$2"; shift 2 ;;
        --dynamodb-table)        DYNAMODB_TABLE="$2"; shift 2 ;;
        --apprunner-ecr-role-arn) APPRUNNER_ECR_ROLE_ARN="$2"; shift 2 ;;
        --apprunner-instance-role-arn) APPRUNNER_INSTANCE_ROLE_ARN="$2"; shift 2 ;;
        -h|--help)
            echo "Usage: $(basename "$0") --key VALUE --domain-name VALUE --parent-domain VALUE --region VALUE --state-bucket VALUE --dynamodb-table VALUE --apprunner-ecr-role-arn VALUE --apprunner-instance-role-arn VALUE [other options]"
            exit 0 ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1 ;;
    esac
done

# Validate required parameters
MISSING=()
[[ -z "$KEY" ]] && MISSING+=("--key")
[[ -z "$DOMAIN_NAME" ]] && MISSING+=("--domain-name")
[[ -z "$PARENT_DOMAIN" ]] && MISSING+=("--parent-domain")  # Validate parent domain
[[ -z "$ECR_IMAGE_IDENTIFIER" ]] && MISSING+=("--ecr-image-identifier")
[[ -z "$CONTAINER_PORT" ]] && MISSING+=("--container-port")
[[ -z "$S3_BUCKET_NAME" ]] && MISSING+=("--media-bucket-name")
[[ -z "$AWS_SECRET_MANAGER_NAME" ]] && MISSING+=("--secret-manager-name")
[[ -z "$DB_NAME" ]] && MISSING+=("--db-name")
[[ -z "$REGION" ]] && MISSING+=("--region")
[[ -z "$STATE_BUCKET" ]] && MISSING+=("--state-bucket")
[[ -z "$DYNAMODB_TABLE" ]] && MISSING+=("--dynamodb-table")
[[ -z "$APPRUNNER_ECR_ROLE_ARN" ]] && MISSING+=("--apprunner-ecr-role-arn")
[[ -z "$APPRUNNER_INSTANCE_ROLE_ARN" ]] && MISSING+=("--apprunner-instance-role-arn")

if [[ ${#MISSING[@]} -gt 0 ]]; then
    echo "Missing required parameters: ${MISSING[*]}" >&2
    exit 1
fi

# Build Terraform variables
TF_VARS=(
    "aws_region=${REGION}"
    "apprunner_ecr_access_role_arn=${APPRUNNER_ECR_ROLE_ARN}"
    "apprunner_instance_role_arn=${APPRUNNER_INSTANCE_ROLE_ARN}"
    "domain_name=${DOMAIN_NAME}"
    "parent_domain=${PARENT_DOMAIN}"  # Add parent domain to Terraform variables
    "ecr_image_identifier=${ECR_IMAGE_IDENTIFIER}"
    "container_port=${CONTAINER_PORT}"
    "media_bucket_name=${S3_BUCKET_NAME}"
    "secret_manager_name=${AWS_SECRET_MANAGER_NAME}"
    "db_name=${DB_NAME}"
)

TF_ARGS=()
for var in "${TF_VARS[@]}"; do
    TF_ARGS+=("-var" "${var}")
done

# Navigate to the Terraform directory
echo "Navigating to Terraform directory..."
cd terraform/

# Run Terraform commands
echo "Initializing Terraform..."
terraform init -reconfigure \
    -backend-config="bucket=${STATE_BUCKET}" \
    -backend-config="region=${REGION}" \
    -backend-config="dynamodb_table=${DYNAMODB_TABLE}" \
    -backend-config="key=${KEY}"

echo "Applying AppRunner service and domain association..."
terraform apply "${TF_ARGS[@]}" \
    -target=aws_apprunner_service.example \
    -target=aws_apprunner_custom_domain_association.example \
    -auto-approve

echo "Applying remaining infrastructure..."
terraform apply "${TF_ARGS[@]}" -auto-approve

echo "Infrastructure deployment completed successfully!"
