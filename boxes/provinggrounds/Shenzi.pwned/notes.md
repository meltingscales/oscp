You will discover exposed credentials on an open SMB file share, enabling you to upload a PHP reverse shell to this lab for initial access. Following this, you will exploit an insecure registry configuration to install .msi packages with elevated privileges. This exercise enhances your skills in credential exploitation and privilege escalation through misconfigurations.

**After completion of this lab, learners will be able to:**

- Enumerate open SMB shares and retrieve sensitive information, such as credentials, from accessible files.
- Use discovered credentials to gain access to a Wordpress administration panel.
- Upload a PHP reverse shell through the Wordpress theme editor to achieve initial access.
- Enumerate registry settings to identify the AlwaysInstallElevated misconfiguration.
- Create and deploy a malicious MSI package to escalate privileges to SYSTEM.