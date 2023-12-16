# This script is designed to be used as an AWS Lambda function.
###########
# PURPOSE: The WS Lambda function interacts with the JAMF API to manage certificates on devices, ensuring they are appropriately used for signing commits. 
# Please note, this script assumes you have already set up S/MIME certificates in JAMF Pro and these certificates are being used on the devices for signing commits. 
###########
import json
import os
import requests
import boto3
import smime
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.hashes import SHA256
import json


# Constants
JAMF_URL = "https://your-jamf-instance-url"
JAMF_API_TOKEN_SECRET_ID = 'JAMF_API_TOKEN'
DEVICE_GROUP_ID = "your-device-group-id-for-smime"  # ID of the device group in JAMF with S/MIME certs

def get_smime_key_id():
    # Create a Secrets Manager client
    client = boto3.client('secretsmanager')
    # Retrieve the secret value
    response = client.get_secret_value(SecretId='SMIME_KEY_ID')
    # Get the key ID from the secret value
    key_id = response['SecretString']
    return key_id

def get_jamf_auth_token():
    """
    Retrieve the JAMF API token from a secure storage and use it for authentication.
    """
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=JAMF_API_TOKEN_SECRET_ID)
    jamf_api_token = response['SecretString']
    return jamf_api_token

def get_devices_with_smime_certs(jamf_token):
    """
    Get a list of devices that are part of the S/MIME certificate group.
    """
    headers = {"Authorization": f"Bearer {jamf_token}"}
    response = requests.get(f"{JAMF_URL}/uapi/computer-groups/id/{DEVICE_GROUP_ID}", headers=headers)
    response.raise_for_status()
    return response.json().get('computers', [])

def verify_smime_signature(signature, device):
    """
    Verify the S/MIME signature using the device information.
    
    Args:
        signature (str): The signature to be verified.
        device (dict): Information about the device.

    Returns:
        bool: True if the signature is valid, False otherwise.
    """
    # Convert the signature from base64 to bytes
    signature_bytes = base64.b64decode(signature)

    # Load the device's S/MIME certificate
    smime_cert = smime.load_certificate(device['smime_certificate'])

    # Verify the signature using the S/MIME certificate
    is_valid = smime.verify_signature(signature_bytes, smime_cert)

    return is_valid

def get_device_from_email(email, device_list):
    """
    Retrieve the device associated with the given email from the device list.
    
    Args:
        email (str): The email address of the commit author.
        device_list (list): List of devices to search from.

    Returns:
        dict: The device associated with the email, if found.
    """
    for device in device_list:
        if device.get('email') == email:
            return device
    return None

def verify_smime_signature(signature, device):
    """
    Verify the S/MIME signature using the device information.
    
    Args:
        signature (str): The signature to be verified.
        device (dict): Information about the device.

    Returns:
        bool: True if the signature is valid, False otherwise.
    """
    # Load the device's S/MIME certificate
    smime_cert = serialization.load_pem_public_key(device['smime_certificate'].encode())

    # Verify the signature using the S/MIME certificate
    try:
        smime_cert.verify(
            signature=base64.b64decode(signature),
            data=device['commit_data'].encode(),
            padding=padding.PKCS1v15(),
            algorithm=SHA256()
        )
        return True
    except Exception:
        return False

def lambda_handler(event, context):
    def verify_commit_signature(commit_data, managed_devices):
        """
        Verify the commit signature using the managed devices.
        
        Args:
            commit_data (dict): Data of the commit.
            managed_devices (list): List of managed devices.

        Returns:
            bool: True if the signature is valid, False otherwise.
        """
        for device in managed_devices:
            signature = commit_data.get('signature')  # Replace with the actual signature field from commit_data
            if verify_smime_signature(signature, device):
                return True
        return False

    """
    AWS Lambda function handler for verifying commit signatures.
    """
    # Get the S/MIME Key ID
    key_id = get_smime_key_id()
    jamf_token = get_jamf_auth_token()
    managed_devices = get_devices_with_smime_certs(jamf_token)

    commit_data = event.get("commit_data")  
    verification_result = verify_commit_signature(commit_data, managed_devices)

    return {
        'statusCode': 200,
        'body': json.dumps({'verification_result': verification_result})
    }

if __name__ == "__main__":
    # Test the Lambda function locally
    test_event = {
        'commit_data': {
            'commit': {
                'author': {
                    'email': 'author@example.com'
                }
            },
            'signature': 'example-signature'
        }
    }
    print(lambda_handler(test_event, None))
