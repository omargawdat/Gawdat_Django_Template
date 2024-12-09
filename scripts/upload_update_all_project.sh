#!/bin/bash
set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." &>/dev/null && pwd)"
TERRAFORM_DIR="$PROJECT_ROOT/terraform"
ENV_FOLDER_PATH="$PROJECT_ROOT/.envs"

# Logging function
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Terraform functions
get_terraform_output() {
    terraform -chdir="$TERRAFORM_DIR" output -raw "$1" || echo "N/A"
}

# SSH and SCP functions
run_remote_command() {
    ssh -i "$SSH_KEY_PATH" -o StrictHostKeyChecking=no -o ConnectTimeout=10 ec2-user@"$SERVER_IP" "$1"
}

run_scp_command() {
    scp -r -i "$SSH_KEY_PATH" -o StrictHostKeyChecking=no -o ConnectTimeout=10 "$1" ec2-user@"$SERVER_IP":"$2"
}

# Repository setup function
setup_repository() {
    if run_remote_command "[ -d $REPO_FOLDER_NAME ]"; then
        log "Repository exists. Pulling latest changes..."
        run_remote_command "cd $REPO_FOLDER_NAME && git fetch && git checkout $BRANCH && git pull origin $BRANCH"
    else
        log "Cloning GitHub repository..."
        run_remote_command "git clone -b $BRANCH $GITHUB_REPO_URL $REPO_FOLDER_NAME"
    fi

    current_commit=$(run_remote_command "cd $REPO_FOLDER_NAME && git rev-parse HEAD")
    log "Current commit hash: $current_commit"
}

# Environment file transfer function
transfer_env_files() {
    local env_subfolder=".${WORKSPACE/dev/dev}"
    env_subfolder="${env_subfolder/prod/production}"
    local source_env_path="$ENV_FOLDER_PATH/$env_subfolder"

    log "Transferring $env_subfolder folder to server ($SERVER_IP)..."
    if [ ! -d "$source_env_path" ]; then
        log "Error: $env_subfolder folder not found at $source_env_path"
        exit 1
    fi

    run_remote_command "mkdir -p $SERVER_DEST_PATH/.envs/$env_subfolder"
    if run_scp_command "$source_env_path/." "$SERVER_DEST_PATH/.envs/$env_subfolder/"; then
        log "Folder contents transferred successfully to $SERVER_DEST_PATH/.envs/$env_subfolder on the server!"
        run_remote_command "ls -R $SERVER_DEST_PATH/.envs/$env_subfolder"
    else
        log "Error: Folder transfer failed."
        return 1
    fi
}

# Docker build and run function
docker_build_and_run() {
    local docker_compose_file="docker-compose.${WORKSPACE}.yml"

    log "Building and running Docker containers..."
    run_remote_command "cd $REPO_FOLDER_NAME && \
        docker-compose -f $docker_compose_file down && \
        docker-compose -f $docker_compose_file build && \
        docker-compose -f $docker_compose_file up -d && \
        docker system prune -f"


    if [ $? -eq 0 ]; then
        log "Docker containers built and started successfully."
    else
        log "Error: Failed to build and start Docker containers."
        return 1
    fi
}

# Validation function
validate_inputs() {
    local required_vars=("SERVER_IP" "WORKSPACE" "REPO_FOLDER_NAME" "SSH_KEY_PATH" "BRANCH")
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ] || [ "${!var}" = "N/A" ]; then
            log "Error: Missing required variable: $var"
            exit 1
        fi
    done

    if [ ! -d "$ENV_FOLDER_PATH" ]; then
        log "Error: .envs folder not found at $ENV_FOLDER_PATH"
        ls -la "$(dirname "$ENV_FOLDER_PATH")"
        exit 1
    fi
}

# Main execution function
main() {
    # Get Terraform outputs
    SERVER_IP=${EC2_PUBLIC_IP:-$(get_terraform_output "ec2_instance_public_ip")}
    GITHUB_REPO_URL=${GITHUB_REPO_URL:-$(get_terraform_output "github_repo_url")}
    REPO_FOLDER_NAME=${REPO_FOLDER_NAME:-$(get_terraform_output "repo_folder_name")}
    SSH_KEY_PATH=${SSH_KEY_PATH:-$(get_terraform_output "ssh_key_path")}
    WORKSPACE=${TERRAFORM_WORKSPACE:-$(get_terraform_output "environment")}

    SERVER_DEST_PATH="/home/ec2-user/${REPO_FOLDER_NAME}"
    BRANCH=$([ "$WORKSPACE" == "prod" ] && echo "main" || echo "dev")

    validate_inputs

    chmod 600 "$SSH_KEY_PATH"

    log "Using server IP: $SERVER_IP"
    log "Using workspace: $WORKSPACE"
    log "Using branch: $BRANCH"
    log "Using repo folder: $REPO_FOLDER_NAME"
    log "Using key path: $SSH_KEY_PATH"
    log "Using .envs folder path: $ENV_FOLDER_PATH"

    setup_repository
    transfer_env_files
    docker_build_and_run

    log "Repository setup, .envs transfer, and Docker deployment completed successfully."
}


main "$@"
