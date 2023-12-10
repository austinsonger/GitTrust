#!/bin/bash

# Fetch the latest S/MIME certificate ID from Keychain
# Note: Update the search criteria as per your organization's naming convention
certificate_id=$(security find-certificate -c "Your-Certificate-Common-Name" -p | openssl x509 -inform pem -noout -text | grep 'Serial Number' | awk '{print $NF}')

echo $certificate_id
