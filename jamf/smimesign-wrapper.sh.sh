#!/bin/bash

# Global constants
email_address="user@example.com"  # Replace with the actual email address
ca_name="YOUR_CA_NAME"  # Replace with your CA's name

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
    # Try to fetch key ID using macOS security command
    local key_fetch_output=$(fetch_smime_key_id_macos "$ca_name")

    if [ $? -eq 0 ]; then
        # Use smimesign to sign the commit with the fetched key ID
        smimesign --status-fd=2 -bsau "$key_fetch_output"
    fi
}

main
