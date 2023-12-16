#!/bin/bash

# Fetch the current S/MIME certificate key ID
key_id=$(security find-identity -p smime -v | grep "YOUR_CA_NAME" | awk '{print $2}')

# Check if key_id is empty
if [ -z "$key_id" ]; then
    echo "No valid S/MIME certificate found"
    exit 1
fi

# Set the key ID for smimesign
git config --global user.signingkey $key_id
