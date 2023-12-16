###########
# PURPOSE: The script should interact with the JAMF API to manage certificates on devices, ensuring they are appropriately used for signing commits. 
# Please note, this script assumes you have already set up S/MIME certificates in JAMF Pro and these certificates are being used on the devices for signing commits. 
###########
import json
import os
import requests

# Constants
JAMF_URL = "https://your-jamf-instance-url"
JAMF_USERNAME = os.environ['JAMF_USERNAME']
JAMF_PASSWORD = os.environ['JAMF_PASSWORD']
DEVICE_GROUP_ID = "your-device-group-id-for-smime"  # ID of the device group in JAMF with S/MIME certs

def get_jamf_auth_token():
    """
    Authenticate with the JAMF API and get a session token.
    """
    auth_response = requests.get(f"{JAMF_URL}/uapi/auth/tokens", auth=(JAMF_USERNAME, JAMF_PASSWORD))
    auth_response.raise_for_status()
    return auth_response.json().get('token')

def get_devices_with_smime_certs(jamf_token):
    """
    Get a list of devices that are part of the S/MIME certificate group.
    """
    headers = {"Authorization": f"Bearer {jamf_token}"}
    response = requests.get(f"{JAMF_URL}/uapi/computer-groups/id/{DEVICE_GROUP_ID}", headers=headers)
    response.raise_for_status()
    return response.json().get('computers', [])

def verify_commit_signature(commit_data, device_list):
    """
    Verify if the commit is signed by a device that is managed and contains an S/MIME certificate.
    
    Args:
        commit_data (dict): Data about the commit, including author information and signature.
        device_list (list): List of devices that contain S/MIME certificates.

    Returns:
        bool: True if the commit signature is verified, False otherwise.
    """
    # Extract necessary information from commit_data
    author_email = commit_data.get('commit', {}).get('author', {}).get('email')
    signature = commit_data.get('signature')  # Assuming this is how the signature is stored

    # Check if the author's device is in the managed device list
    author_device = get_device_from_email(author_email, device_list)
    if not author_device:
        return False

    # Verify the commit signature (Placeholder for actual signature verification logic)
    # Need to replace this with a proper method to verify S/MIME signatures
    return verify_smime_signature(signature, author_device)

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
    # Placeholder for actual S/MIME signature verification logic
    # This should involve using the device's S/MIME certificate to verify the signature
    return True  # Placeholder return value

def lambda_handler(event, context):
    """
    AWS Lambda function handler for verifying commit signatures.
    """
    jamf_token = get_jamf_auth_token()
    managed_devices = get_devices_with_smime_certs(jamf_token)

    commit_data = event.get("commit_data")  # Replace with actual commit data from the event
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
