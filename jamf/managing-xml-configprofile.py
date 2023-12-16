import requests

url = "https://your-jamf-pro-instance-url/JSSResource/configurationprofiles/id/0"
headers = {
    'Authorization': 'Basic YOUR_ENCODED_CREDENTIALS',
    'Content-Type': 'application/xml'
}
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
response = requests.post(url, headers=headers, data=data)
