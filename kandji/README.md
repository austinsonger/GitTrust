


### Table of Contents
- [Prerequisites](#prerequisites)
- [Setting Up Kandji](#setting-up-kandji)
- [Integrating `smimesign`](#integrating-smimesign)
- [Okta Integration](#okta-integration)
- [Scripts for Automation](#scripts-for-automation)

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