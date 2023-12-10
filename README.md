# SecureGit-KandjiTrust (SGKT): Enhanced S/MIME Commit Signing with Device Authentication

## Overview
S/MIME signing for Git commits in an environment where devices are managed by Kandji and access control is managed by Okta. It ensures that only compliant devices can make signed commits to Git repositories.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Setting Up Kandji](#setting-up-kandji)
- [Integrating `smimesign`](#integrating-smimesign)
- [Okta Integration](#okta-integration)
- [Scripts for Automation](#scripts-for-automation)

## Prerequisites
- Access to Kandji for device management.
- Git installed on macOS devices.
- `smimesign` utility.
- Access to Okta for identity and access management.

## Setting Up Kandji
Kandji is used for deploying PKCS #12-formatted S/MIME certificates to Apple devices.

### Steps:
1. Configure and deploy a certificate profile in Kandji.
2. Ensure PKCS #12-formatted certificates are deployed to macOS devices.

## Integrating `smimesign`
`smimesign` is used for signing Git commits with S/MIME certificates.

### Steps:
1. Install `smimesign` on macOS devices.
2. Configure Git to use `smimesign` for commit signing.
3. Integrate a script for retrieving the current S/MIME certificate from the macOS Keychain.

## Okta Integration
Okta is used to ensure that only compliant devices have access to Git repositories.

### Steps:
1. Integrate Okta Device Trust with Kandji.
2. Control repository access through Okta, ensuring compliance.

## Scripts for Automation
Scripts automate the retrieval and use of S/MIME certificates for signing commits.

### Key Scripts:
- `fetch_certificate.sh`: Retrieves the current S/MIME certificate from the Keychain.
- `sign_commit.sh`: Wrapper script for Git commits using the fetched certificate.


