### 1. Create a GitHub App
- **Log into GitHub** and navigate to your account settings.
- Go to **Developer settings** and choose **GitHub Apps**.
- Click **New GitHub App** and fill in the necessary details:
    - **Name**: Give your app a unique name.
    - **Webhook URL**: This will be the API Gateway URL from AWS, which you'll create later. For now, you can use a placeholder URL and update it later.
    - **Webhook secret**: Set a secret for security.
    - **Permissions**: Set permissions to `Read` access for code, commits, and metadata.
    - **Subscribe to events**: Choose the `push` event.
- After filling in the details, click **Create GitHub App**.

### 2. Install the GitHub App on Your Repositories
- Once the GitHub App is created, go to its settings page.
- Click on **Install App** in the sidebar.
- Choose the repositories you want the app to have access to and install it.

### 3. Create an AWS Lambda Function
- **Log into your AWS Management Console**.
- Navigate to the **Lambda** service and create a new function.
- Choose **Author from scratch** and provide the necessary details:
    - **Name**: Choose a name for your Lambda function.
    - **Runtime**: Select Python, as your existing scripts are in Python.
- In the **Function code** section, upload `github-commit-verifier_lambda.py` and `jamf-github-commit-verifier.py`.
- Make sure the handler is set correctly to the function name in your Python code.
- Set up the **Environment variables**, **Execution role**, and any other necessary configurations.
- Deploy the Lambda function.

### 4. Set up an API Gateway in AWS
- Go to the **API Gateway** service in AWS.
- Create a new API, choosing **REST API**.
- Create a new resource (e.g., `/webhook`) and a POST method for this resource.
- Set the integration type to Lambda Function and link it to the Lambda function you created.
- Deploy the API to a new or existing stage.
- Note the **Invoke URL**; this is what you'll use as the Webhook URL in your GitHub App settings.



## Securely store and retrieve the JAMF API token

 **Store the JAMF API token in AWS Secrets Manager**: Go to the AWS Management Console, navigate to the Secrets Manager service, and store your JAMF API token as a new secret. Make sure to note the secret name.
2. **Give your Lambda function permission to access the secret**: In the IAM role that your Lambda function uses, add a policy that gives it permission to read the secret from Secrets Manager. The policy should look something like this:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "secretsmanager:GetSecretValue",
            "Resource": "arn:aws:secretsmanager:region:account-id:secret:secret-name"
        }
    ]
}

```

Replace `region`, `account-id`, and `secret-name` with your actual AWS region, account ID, and the name of your secret.
3. **Retrieve the secret in your Lambda function**: You can use the `boto3` library to retrieve the secret in your Lambda function. Here's how you can modify your `get_jamf_auth_token` function to do this:

```
import boto3

def get_jamf_auth_token():
	client = boto3.client('secretsmanager')
	response = client.get_secret_value(SecretId='your-secret-name')
	return response['SecretString']
```


Replace `'your-secret-name'` with the name of your secret. The `get_secret_value` function returns a dictionary that includes the secret value under the `'SecretString'` key.