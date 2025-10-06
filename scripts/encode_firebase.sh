#!/bin/bash
# Script to encode Firebase credentials to base64 and update .env file
# Usage: ./scripts/encode_firebase.sh path/to/firebase.json

set -e

# Check if firebase.json path is provided
if [ -z "$1" ]; then
    echo "❌ Error: Please provide path to firebase.json"
    echo "Usage: ./scripts/encode_firebase.sh path/to/firebase.json"
    exit 1
fi

FIREBASE_JSON_PATH="$1"

# Check if file exists
if [ ! -f "$FIREBASE_JSON_PATH" ]; then
    echo "❌ Error: File not found: $FIREBASE_JSON_PATH"
    exit 1
fi

# Validate JSON
if ! jq empty "$FIREBASE_JSON_PATH" 2>/dev/null; then
    echo "❌ Error: Invalid JSON file"
    exit 1
fi

# Encode to base64 (single line)
ENCODED=$(base64 -i "$FIREBASE_JSON_PATH" | tr -d '\n')

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "Run: cp dummy.env .env"
    exit 1
fi

# Update .env file
if grep -q "^FIREBASE_CREDENTIALS_B64=" .env; then
    # Replace existing value
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s|^FIREBASE_CREDENTIALS_B64=.*|FIREBASE_CREDENTIALS_B64=$ENCODED|" .env
    else
        # Linux
        sed -i "s|^FIREBASE_CREDENTIALS_B64=.*|FIREBASE_CREDENTIALS_B64=$ENCODED|" .env
    fi
    echo "✅ Updated FIREBASE_CREDENTIALS_B64 in .env"
else
    echo "❌ Error: FIREBASE_CREDENTIALS_B64 not found in .env"
    exit 1
fi

echo ""
echo "✅ Firebase credentials encoded successfully!"
echo ""
echo "Next steps:"
echo "  1. Review .env file to verify the update"
echo "  2. Restart your Django application: just rebuild"
echo ""
echo "⚠️  Remember to add firebase.json to .gitignore if not already there"
