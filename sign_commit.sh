#!/bin/bash

# Fetch the latest certificate ID
certificate_id=$(./fetch_certificate.sh)

# Check if certificate_id is retrieved
if [ -z "$certificate_id" ]; then
    echo "Error: Unable to fetch certificate ID."
    exit 1
fi

# Configure Git to use the fetched certificate ID
git config --local user.signingkey $certificate_id

# Perform the Git commit with sign
git commit -S -m "$1"
