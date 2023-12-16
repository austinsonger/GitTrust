# This script is designed to be used as an AWS Lambda function.
############
# PURPOSE: This script will interact with GitHub APIs to fetch commit data and then validate it against criteria such as S/MIME signatures, device trust status from JAMF, or other verification methods you have in place.
# Triggered by GitHub webhook events for new commits. 
############

import json
import os
import requests

# Constants
GITHUB_TOKEN = os.environ['GITHUB_TOKEN']  # GitHub access token
JAMF_AUTH_TOKEN = os.environ['JAMF_AUTH_TOKEN']  # JAMF API token
JAMF_URL = "https://your-jamf-instance-url"

def get_commit_data(repo_name, commit_sha):
    """
    Fetch commit data from GitHub.
    """
    url = f"https://api.github.com/repos/{repo_name}/commits/{commit_sha}"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def verify_commit_with_jamf(commit_data):
    """
    Verify the commit with JAMF for device trust and certificate status.
    
    Args:
        commit_data (dict): Data about the commit, including author information.

    Returns:
        bool: True if the commit is verified, False otherwise.
    """
    # Extract author's details from commit_data
    author_email = commit_data['commit']['author']['email']

    # Placeholder for JAMF API request to get device details and Replace 'device_id' with the appropriate identifier from JAMF
    device_id = get_device_id_from_email(author_email)
    device_info = get_device_info_from_jamf(device_id)

    # Check if the device is managed and compliant
    is_compliant = check_device_compliance(device_info)

    return is_compliant

def get_device_id_from_email(email):
    """
    Get the device ID associated with the given email from JAMF.
    
    Args:
        email (str): The email address of the commit author.

    Returns:
        str: The device ID associated with the email.
    """
    url = f"{JAMF_URL}/api/v1/devices"
    headers = {"Authorization": f"Bearer {JAMF_AUTH_TOKEN}"}
    params = {"filter": f"email={email}"}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    devices = response.json().get("devices", [])
    if devices:
        return devices[0]["id"]
    else:
        return None

def get_device_info_from_jamf(device_id):
    """
    Retrieve device information from JAMF using the device ID.
    
    Args:
        device_id (str): The device ID.

    Returns:
        dict: Information about the device.
    """
    url = f"{JAMF_URL}/api/v1/devices/{device_id}"
    headers = {"Authorization": f"Bearer {JAMF_AUTH_TOKEN}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def check_device_compliance(device_info):
    """
    Check if the device meets the organization's security policies.
    
    Args:
        device_info (dict): Information about the device.

    Returns:
        bool: True if the device is compliant, False otherwise.
    """
    # Check if the device is managed and compliant
    return device_info.get('managed', False) and device_info.get('compliant', False)

def create_check_run(repo_name, commit_sha, conclusion, output):
    """
    Create a check run on GitHub for the commit.
    
    Args:
        repo_name (str): The name of the repository.
        commit_sha (str): The SHA of the commit.
        conclusion (str): The conclusion of the check run (e.g., "success", "failure").
        output (dict): The output of the check run.

    Returns:
        dict: The response from the GitHub API.
    """
    url = f"https://api.github.com/repos/{repo_name}/check-runs"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    payload = {
        "name": "Commit Verification",
        "head_sha": commit_sha,
        "status": "completed",
        "conclusion": conclusion,
        "output": output
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

def lambda_handler(event, context):
    """
    AWS Lambda function handler for GitHub commit verification.

    Parameters:
    - event (dict): The event data passed to the Lambda function.
    - context (object): The runtime information of the Lambda function.

    Returns:
    - dict: The response data returned by the Lambda function.
    """
    # Get the repo name and commit SHA from the event
    repo_name = event.get("repository").get("name")
    commit_sha = event.get("commit").get("sha")

    # Get commit data
    commit_data = get_commit_data(repo_name, commit_sha)

    # Verify the commit with JAMF
    is_verified = verify_commit_with_jamf(commit_data)

    # Create a check run or commit status based on the verification result
    if is_verified:
        conclusion = "success"
        output = {
            "title": "Commit Verification",
            "summary": "The commit has been verified successfully."
        }
    else:
        conclusion = "failure"
        output = {
            "title": "Commit Verification",
            "summary": "The commit failed verification."
        }

    # Create a check run on GitHub
    response = create_check_run(repo_name, commit_sha, conclusion, output)

    return {
        'statusCode': 200,
        'body': json.dumps({'verification_result': is_verified})
    }

if __name__ == "__main__":
    # Test the Lambda function locally with dummy data
    test_event = {
        'body': json.dumps({
            'repository': {'full_name': 'your-repo/name'},
            'head_commit': {'id': 'commit-sha'}
        })
    }
    print(lambda_handler(test_event, None))
