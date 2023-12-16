# GitTrust (GT): Enhanced S/MIME Commit Signing with Device Authentication
> Inspired By: [FIGMA](https://www.figma.com/blog/how-we-enforce-device-trust-on-code-changes/)
--------
To proactively mitigate the risk of malicious code reaching production, GitTrust ensures that code changes merged into GitHub release branches come from trusted, company-managed devices. It does this by S/MIME signing for Git commits in an environment where devices are managed by MDM and access control is managed by Okta. It ensures that only compliant devices can make signed commits to Git repositories.

**PROJECT-WIDE TO-DO**
- [ ] Issue X.509 Okta Device Trust certificates to MacBooks from an Amazon Private Certificate Authority (CA) (The certificates will be distributed through MDM, renew every 30 days, and attest that a laptop meets Endpoint Security Baseline criteria at the time they’re issued.)
  - Enforce [NISTGOV Baselines via macOS Security Compliance Project](https://github.com/usnistgov/macos_security/tree/main/baselines)


**Table of Contents**
- [With Kandji](#with-kandji)
- [With JAMF](#with-jamf)
- [With Jumpcloud](#with-jumpcloud)

## With Kandi

### Prerequisites
- Access to Kandji for device management.
- Git installed on macOS devices.
- `smimesign` utility.
- Access to Okta for identity and access management.

### Handling of Device Trust Certificates

#### Certificate Profile Configuration

- Kandji allows you to configure and deploy certificate profiles to Apple devices. This feature is used for services requiring a valid certificate trust chain or apps that support certificate-based authentication​​.
- Kandji supports PKCS #1-formatted certificate files (.cer, .crt, .der) containing only the certificate, and PKCS #12-formatted files (.p12, .pfx) that include both the certificate and its corresponding private key​​.
- For PKCS #12-formatted certificates, Kandji provides options for naming the certificate, setting a password, uploading the certificate file, allowing apps to access the private key, and preventing the private key from being extracted from the keychain​​.

#### Okta Device Trust Integration
- Kandji's Okta Device Trust (ODT) integration combines device management with Okta's app management capabilities. This integration is built on Okta Identity Engine (OIE) and streamlines the setup and configuration of ODT by automatically deploying ODT configurations to devices​​.
- The integration ensures that Kandji-managed Apple devices are recognized before users can access Okta-protected apps, enabling password-less authentication experiences like Okta FastPass​​.
- Once ODT is set up, enabled, and scoped to your blueprints in Kandji, settings payloads are automatically configured and delivered to Apple devices. This includes a unique Okta SCEP certificate per device used in the device registration process and configurations for macOS, iOS, and iPadOS devices to integrate with Okta Verify​

#### TO DO

- [ ] Integrate Kandji's certificate management features with your Git commit signing process, with use of S/MIME certificates.
- [ ] Leverage the Okta Device Trust integration to manage access to Okta-protected resources, ensuring devices are managed by Kandji and meets trust criteria.
- [ ] Develop or modify tools to work with Kandji's PKCS #12-formatted certificates, fetching the latest key ID for signing at the time of commit.

### Setting Up Kandji
Kandji is used for deploying PKCS #12-formatted S/MIME certificates to Apple devices.

#### Steps:
1. Configure and deploy a certificate profile in Kandji.
2. Ensure PKCS #12-formatted certificates are deployed to macOS devices.

### Integrating `smimesign`
`smimesign` is used for signing Git commits with S/MIME certificates.

#### Steps:
1. Install `smimesign` on macOS devices.
2. Configure Git to use `smimesign` for commit signing.
3. Integrate a script for retrieving the current S/MIME certificate from the macOS Keychain.

### Okta Integration
Okta is used to ensure that only compliant devices have access to Git repositories.

#### Steps:
1. Integrate Okta Device Trust with Kandji.
2. Control repository access through Okta, ensuring compliance.

### Scripts for Automation
Scripts automate the retrieval and use of S/MIME certificates for signing commits.

#### Key Scripts:
- `setup_smimesign.sh`: This script will install smimesign and configure Git to use it for commit signing.
- `fetch_certificate.sh`: This script will interact with the macOS Keychain (where Kandji deploys certificates) to fetch the current S/MIME certificate for signing commits.
- `sign_commit.sh`: A wrapper script for Git commits, ensuring that each commit is signed with the appropriate certificate.

#### Usage Instructions

1. Make these scripts executable: `chmod +x setup_smimesign.sh fetch_certificate.sh sign_commit.sh`
2. Run `./setup_smimesign.sh` to set up smimesign.
3. Use `./sign_commit.sh` "Your commit message" to make a signed commit.


## With JAMF

### Prerequisites
- Access to JAMF for device management.
- Git installed on macOS devices.
- `smimesign` utility.
- Access to Okta for identity and access management.


### 1. Signing Commits with Device Trust Certificates
- **Setup of `smimesign` and `smimesign-figma`**:
    - Install `smimesign`, an S/MIME signing utility for Git, on the devices managed by JAMF Pro.
    - Modify or create a version of `smimesign` (referred to as `smimesign-figma`) that is specifically tailored to your organization's requirements, possibly to handle unique aspects of your certificate setup or integration needs.
    - Ensure that this custom utility can interact correctly with the S/MIME certificates deployed on the devices.
- **Deployment of S/MIME Certificates via JAMF Pro**:
    - Use JAMF Pro to deploy S/MIME certificates, issued by your private CA, to the Apple devices. These certificates are essential for signing commits.
    - Configure the certificate profiles correctly to ensure that the certificates are installed in the appropriate locations on the devices (e.g., system vs. user keychain on macOS).
- **Wrapper Script for Dynamic Key Fetching**:
    - Develop a wrapper script that facilitates the dynamic fetching of the key ID from the S/MIME certificates for signing commits.
    - This script should interface with the macOS Keychain (or appropriate certificate store) to retrieve the current certificate or key ID when a commit is made.
### 2. Verifying Signatures with AWS Lambda and GitHub Apps
- **AWS Lambda Function Setup**:
    - Create an AWS Lambda function that is triggered by GitHub webhook events for new commits.
    - Program this function to extract and verify the S/MIME signatures from the commits, ensuring they are signed with certificates issued by your private CA.
- **Integration with GitHub Apps**:
    - Set up a GitHub App that integrates with your Lambda function. This App will facilitate the communication between GitHub and the AWS environment.
    - Ensure the GitHub App has the necessary permissions to access commit data and report status back to GitHub.
- **Webhook Integration**:
    - Configure webhooks in your GitHub repositories to trigger the Lambda function upon new commit events.
    - These webhooks should send the necessary data (like commit details and signatures) to the Lambda function for processing.
### 3. Verifying Bot-authored Commits
- **Allowlist for Bot Commits**:
    - Create and maintain an allowlist of trusted bots (like Dependabot).
    - Implement logic in your verification process (either in the Lambda function or an additional script) to identify and handle commits made by these bots.


### JAMF Scripts for Automation




## With Jumpcloud
### Table of Contents
- [Jumpcloud Prerequisites](#jumpcloud-prerequisites)
- [Setting Up Jumpcloud](#setting-up-jumpcloud)
- [Integrating `smimesign`](#integrating-smimesign)
- [Jumpcloud Device Trust](#jumpcloud-device-trust)
- [Scripts for Automation](#jumpcloud-scripts-for-automation)


### Jumpcloud Prerequisites
- Access to Kandji for device management.
- Git installed on macOS devices.
- `smimesign` utility.
- Access to Okta for identity and access management.

### Handling of Device Trust Certificates

#### Certificate Profile Configuration


1. **Certificate Bundle Components**: The Device Trust Certificate Bundle includes a Root Certificate, an Intermediate Certificate, a Leaf Certificate, and a Private Key. The Root Certificate is self-signed, and the Leaf Certificate contains a unique identifier. The Private Key is created by the agent to generate the certificate signing request​[](https://jumpcloud.com/support/manage-device-trust-certificates)​.
2. **Storage Locations**:
    - On macOS, certificates are stored in a new jumpcloud-device-trust-keychain in the user’s Library/Keychains folder.
    - On Windows, the root certificate is installed in the system cert store, and the intermediate and Device Trust certificates are in the user’s stores.
    - On Linux, certificates are stored in the user’s NSS database​[](https://jumpcloud.com/support/manage-device-trust-certificates)​.
3. **Distribution of Certificates**: Global Device Certificates are distributed from the Conditional Policies Settings page in the JumpCloud Admin Portal, where you can enable Global Certificate Distribution​[](https://jumpcloud.com/support/manage-device-trust-certificates)​.
4. **Certificate Lifespan and Renewal**: These certificates have a time-to-live of 30 days and are renewed every two weeks by the user agent​[](https://jumpcloud.com/support/manage-device-trust-certificates#:~:text=Note%3A%0A%0AGlobal%20Device%20Certificates%20have%20a,weeks%20by%20the%20user%20agent)​.
5. **User Interaction**: Users may receive prompts to select Device Trust certificates when accessing the JumpCloud User Portal or using SSO-enabled applications. They are advised to select the JumpCloud Device Trust Certificate in these situations​[](https://jumpcloud.com/support/manage-device-trust-certificates)​.


#### Jumpcloud Device Trust Integration

1. **Authentication via Certificate Presentation**: When a user tries to access resources such as the User Portal or applications, the JumpCloud system requires the client (user’s device) to present a certificate. This process is integral to the Device Trust framework.
2. **Certificate-Based Device Trust**: The presence and validity of the certificate confirm the trustworthiness of the device. If the device presents the correct certificate, it is considered trusted, and access to the requested resources is granted.
3. **Seamless User Experience**: This setup facilitates a more streamlined access experience, saving time for users and allowing seamless access to applications.
4. **Integration with Other Systems**: Device Trust can be integrated with other systems like SSO-enabled applications, enhancing overall security and compliance.
5. **Device Management and Compliance**: The integration plays a key role in ensuring that devices meet specific security and compliance standards, which are crucial for maintaining the integrity of an organization's IT infrastructure.

### Setting Up Jumpcloud

### Integrating `smimesign`

### Jumpcloud Device Trust

### Jumpcloud Scripts for Automation


# References
- https://api-docs.kandji.io/


