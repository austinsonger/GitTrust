> JAMF Pro uses XML configuration profiles for certificate deployment. While JAMF Pro doesn't support direct scripting for profile creation, you can automate the process using its API.

## Overview

1. The Amazon Private CA issues X.509 Okta Device Trust certificates to MacBooks. These certificates are stored in the macOS Keychain.
2. When you want to make a signed commit, the `fetch_smime_key_id_macos` function in `mimesign-wrapper.sh`` is called. This function fetches the S/MIME Key ID of the certificate from the macOS Keychain.
3. The fetched Key ID is then used by `smimesign` to sign the commit. 
4. The `jamf-commit-signing.py` AWS Lambda Function can then be used to enforce commit signing on the JAMF server.
5. The `jamf-github-commit-verifier.py` AWS Lambda Function can be used to verify the signed commits on GitHub.


### smimesign-wrapper.sh
It fetches the S/MIME Key ID using the security command on macOS. It then sets the fetched key ID for git signing using the smimesign command. The script also includes error handling to check if a valid S/MIME certificate is found. 

1. The script defines a function `fetch_smime_key_id_macos` that takes one argument, `ca_name`, which is the name of the Certificate Authority (CA) from which you want to fetch the S/MIME Key ID.
2. Inside this function, it uses the `security` command, a built-in macOS command-line utility, to find identities in the keychain that match the S/MIME policy and are valid. It pipes this output to `grep` to filter for the specified CA name.
3. The filtered output is then piped to `awk`, which extracts the second field from each line (the Key ID).
4. If a Key ID is found (`-z "$key_id"` checks if the `key_id` variable is empty), it prints a success message with the Key ID and returns 0 (indicating success). If no Key ID is found, it prints an error message and returns 1 (indicating failure).


### jamf-commit-signing.py
This AWS Lambda Function interacts with the JAMF API to manage certificates on devices. 

1. **Import Statements**: The script imports several Python modules that it needs to function. `json` is used for parsing and creating JSON data, `os` is used for interacting with the operating system, `requests` is used for making HTTP requests, and `boto3` is the Amazon Web Services (AWS) Software Development Kit (SDK) for Python, which allows Python developers to write software that makes use of AWS services like Amazon S3, Amazon EC2, etc.
2. **Constants**: The script defines several constants at the top of the file. `JAMF_URL` is the URL of your JAMF instance, `JAMF_USERNAME` and `JAMF_PASSWORD` are the username and password for your JAMF instance (retrieved from environment variables), and `DEVICE_GROUP_ID` is the ID of the device group in JAMF that has S/MIME certificates.
3. **get_smime_key_id() Function**: This function uses the `boto3` client for AWS Secrets Manager to retrieve the S/MIME key ID. It creates a Secrets Manager client, retrieves the secret value associated with the 'SMIME_KEY_ID' secret, extracts the key ID from the secret value, and returns it.
4. **get_jamf_auth_token() Function**: This function is defined to authenticate with the JAMF API and get a session token. The function body isn't included in the provided excerpt, but it likely sends a request to the JAMF API with the `JAMF_USERNAME` and `JAMF_PASSWORD` to authenticate and retrieve a session token.


### jamf-github-commit-verifier.py
This AWS Lambda Function fetches commit data from GitHub and verifies it with JAMF. It is triggered by a GitHub webhook on new commit events. The commit data fetched by this AWS Lambda Function us passed to jamf-commit-signing.py for verification.

1. The `lambda_handler` function takes two parameters: `event` and `context`. These parameters are automatically passed to the function by the AWS Lambda service when it invokes the function.
2. The function starts by extracting the repository name and commit SHA from the `event` parameter. These values are used to fetch commit data from GitHub.
3. The `get_commit_data` function is called to fetch commit data from GitHub. It takes the repository name and commit SHA as arguments and makes a GET request to the GitHub API using the `requests.get` function. The response is then converted to JSON format using the `response.json()` method and returned.
4. After obtaining the commit data, the function creates an AWS Lambda client using the `boto3.client` function. This client is used to invoke another Lambda function called `jamf-commit-signing` (the name is a placeholder and should be replaced with the actual name of the function).
5. The `client.invoke` method is called to invoke the `jamf-commit-signing` function. It takes several parameters:
    - `FunctionName`: The name of the function to invoke.
    - `InvocationType`: The type of invocation. In this case, it is set to `'RequestResponse'`, which means the Lambda function will wait for a response before returning.
    - `Payload`: The payload to pass to the function. In this case, it is a JSON string containing the `commit_data` obtained earlier.
6. The response from invoking the `jamf-commit-signing` function is stored in the `response` variable. The response contains the verification result.
7. The verification result is extracted from the response using the `json.loads` function. The `response['Payload'].read()` method is used to read the response payload as a string, and then `json.loads` is called to parse the string and convert it to a Python object.
8. Finally, the function returns a dictionary with a `'statusCode'` of 200 (indicating a successful response) and a `'body'` containing the verification result as a JSON string.
Overall, this code fetches commit data from GitHub, invokes another Lambda function (`jamf-commit-signing`), and returns the verification result.


### Make the script executable:

```bash
chmod +x smimesign-wrapper.sh
```

### Enforcing commit signing in a JAMF environment

#### Configure Git to use the wrapper

```bash
git config gpg.format x509
git config gpg.x509.program /path/to/smimesign-wrapper.sh
git config user.signingkey ""
```

1. **Configure Git to use S/MIME for commit signing**: You can do this by setting the `gpg.program` configuration option to `smimesign`. Here's how you can do it:

`git config --global gpg.program smimesign`

2. **Configure Git to enforce commit signing**: You can enforce commit signing by setting the `commit.gpgSign` configuration option to `true`. Here's how you can do it:

`git config --global commit.gpgSign true`

3. **Fetch the S/MIME Key ID from the macOS Keychain**: You can use the `fetch_smime_key_id_macos` function in `smimesign-wrapper.sh`` to do this. You need to call this function with your CA's name as an argument.

4. **Use the fetched Key ID to sign your commits**: You can use the `smimesign` command with the fetched Key ID to sign your commits. This is done in the `main` function in your script.

5. **Enforce commit signing on the JAMF server**:  `jamf-commit-signing.py`AWS Lambda Function is used to enforce commit signing on the JAMF server. This AWS Lambda Function uses the JAMF API to ensure that all commits are signed.

6. **Verify the signed commits on GitHub**: `jamf-github-commit-verifier.py`AWS Lambda Function is used to verify the signed commits on GitHub. This AWS Lambda Function checks the commit signatures against a list of approved signatories.
