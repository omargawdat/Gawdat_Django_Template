#!/bin/bash
set -e

# Get the directory of the current script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "Waiting for instance to be ready..."
sleep 30

echo "Calling upload_update_all_project.sh script..."
"$SCRIPT_DIR/upload_update_all_project.sh"


echo "Server setup completed successfully."
