
### Table of Contents
- [Jumpcloud Prerequisites](#jumpcloud-prerequisites)
- [Setting Up Jumpcloud](#setting-up-jumpcloud)
- [Integrating `smimesign`](#integrating-smimesign)
- [Jumpcloud Device Trust](#jumpcloud-device-trust)
- [Scripts for Automation](#jumpcloud-scripts-for-automation)


### Jumpcloud Prerequisites
- Access to Jumpcloud for device management.
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
