import requests
from requests.auth import HTTPBasicAuth
import base64

# JAMF Pro instance URL
url = "https://your-jamf-pro-instance-url/JSSResource/configurationprofiles/id/0"

# Encode your credentials
username = 'your_username'
password = 'your_password'
encoded_credentials = base64.b64encode(f"{username}:{password}".encode()).decode()

# Set headers
headers = {
    'Authorization': f'Basic {encoded_credentials}',
    'Content-Type': 'application/xml'
}

# Data payload
data = """
<configuration_profile>
    <general>
        <name>Certificate Profile</name>
        <!-- other general settings -->
    </general>
    <certificates>
        <!-- certificate details -->
    </certificates>
    <!-- other payloads -->
</configuration_profile>
"""

# Make the POST request
try:
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    print("Configuration Profile created successfully.")
    # Optionally, print response details or process further as needed
except requests.exceptions.HTTPError as err:
    print(f"HTTP Error occurred: {err}")
except Exception as e:
    print(f"An error occurred: {e}")
