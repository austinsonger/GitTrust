# GitTrust (GT): Enhanced S/MIME Commit Signing with Device Authentication
> Inspired By: [FIGMA](https://www.figma.com/blog/how-we-enforce-device-trust-on-code-changes/)
--------
To proactively mitigate the risk of malicious code reaching production, GitTrust ensures that code changes merged into GitHub release branches come from trusted, company-managed devices. It does this by S/MIME signing for Git commits in an environment where devices are managed by MDM and access control is managed by Okta. It ensures that only compliant devices can make signed commits to Git repositories.

**PROJECT-WIDE TO-DO**
- [ ] Issue X.509 Okta Device Trust certificates to MacBooks from an Amazon Private Certificate Authority (CA) (The certificates will be distributed through MDM, renew every 30 days, and attest that a laptop meets Endpoint Security Baseline criteria at the time they’re issued.)
  - Enforce [NISTGOV Baselines via macOS Security Compliance Project](https://github.com/usnistgov/macos_security/tree/main/baselines)

**MDM**
- [With Kandji](/kandji/README.md)
- [With JAMF](/jamf/README.md)
- [With Jumpcloud](/jumpcloud/README.md)


# Signing Commits with Device Trust Certificates

![](/images/Signing%20Commits%20with%20Device%20Trust%20Certificates.png)

# Verifying Signatures with AWS Lambda and GitHub Apps
![](/images/Verifying%20Signatures%20with%20AWS%20Lambda%20and%20GitHub%20.png)


# Verifying Bot-authored Commits
![](/images/Verifying%20Bot-authored%20Commits.png)



