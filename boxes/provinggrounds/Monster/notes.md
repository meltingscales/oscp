A foothold on the target system will be gained by leveraging a weak password to access the CMS Admin panel. From there, the CMS backup system will be accessed, revealing crackable password hashes that lead to low-privilege access. Privileges will then be elevated to the Administrator account by manipulating writable XAMPP configuration files. This lab focuses on exploiting weak authentication and privilege escalation methods.

Summary

This lab demonstrates leveraging a weak password to access Monstra CMS, extracting password hashes from its backup system, and cracking them to gain RDP access. Privilege escalation is achieved by exploiting a writable xampp-control.ini file to inject a reverse shell payload, triggered upon interaction with the XAMPP Control Panel by an administrator. This lab emphasizes web application exploitation, credential cracking, and local privilege escalation through misconfigured services.

Learning Objectives

**After completion of this lab, learners will be able to:**

- Enumerate web services to discover Monstra CMS and access the admin panel using a weak password.
- Extract and analyze a backup file to retrieve user password hashes.
- Crack the hashes to obtain valid credentials and log in via RDP.
- Craft and deploy a reverse shell payload to replace the xampp-control.ini configuration path.
- Trigger the payload by interacting with the XAMPP Control Panel and escalate privileges to Administrator.

alright. easy lab. let's get crackin



