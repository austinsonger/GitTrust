#!/bin/bash

# Function to fetch S/MIME Key ID using security command (macOS specific)
fetch_smime_key_id_macos() {
    local ca_name="$1"
    local key_id

    # Fetch the current S/MIME certificate key ID from a specific CA
    key_id=$(security find-identity -p smime -v | grep "$ca_name" | awk '{print $2}')

    if [ -z "$key_id" ]; then
        echo "No valid S/MIME certificate found for CA: $ca_name"
        return 1
    else
        echo "Key ID for CA $ca_name: $key_id"
        return 0
    fi
}

# Main logic to fetch key ID and set it for git signing
main() {
    local email_address="user@example.com"  # Replace with the actual email address
    local ca_name="YOUR_CA_NAME"  # Replace with your CA's name

    # Try to fetch key ID using macOS security command
    local key_fetch_output=$(fetch_smime_key_id_macos "$ca_name")

    if [ $? -eq 0 ]; then
        local key_id=$(echo "$key_fetch_output" | awk '{print $6}')
        git config --global user.signingkey "$key_id"
        echo "Git signing key configured: $key_id"
    else
        echo "Falling back to alternative method for fetching key ID..."
        # Add alternative method here if the first method fails
    fi
}
# Execute the main function
main
