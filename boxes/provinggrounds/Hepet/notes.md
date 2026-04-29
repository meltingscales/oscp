In this lab, you will exploit the target by uncovering important information in emails accessed through leaked credentials. You will utilize this information to send a spreadsheet containing a malicious macro, granting you a low-privileged shell. Finally, you will escalate your privileges by exploiting a misconfigured service.

Summary

This lab demonstrates leveraging leaked credentials to access an email server and send a malicious spreadsheet containing a LibreOffice macro payload. Learners will use the payload to establish a reverse shell and escalate privileges by exploiting a writable service binary for the Veyon Service, ultimately achieving SYSTEM-level access. This lab emphasizes email server exploitation, social engineering, and privilege escalation through service misconfigurations.

Learning Objectives

**After completion of this lab, learners will be able to:**

- Enumerate services to identify the email server and associated credentials.
- Access emails to uncover sensitive details about spreadsheet processing.
- Craft a LibreOffice macro payload and send it via email to exploit the target system.
- Replace the writable binary for the Veyon Service with a malicious payload.
- Reboot the target machine to execute the malicious binary and gain SYSTEM access.