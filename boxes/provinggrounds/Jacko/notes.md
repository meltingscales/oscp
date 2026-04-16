This lab demonstrates exploiting a misconfigured H2 database with default credentials to achieve remote code execution, followed by privilege escalation via a DLL hijacking vulnerability in Fujitsu's PaperStream IP application. Learners will utilize SQL queries to execute commands and leverage an unpatched DLL search path vulnerability to obtain a SYSTEM shell.

**After completion of this lab, learners will be able to:**

- Enumerate services to identify the H2 database on port 8082 and authenticate using default credentials.
- Use SQL queries to achieve command execution and deploy a reverse shell payload.
- Enumerate the target system for interesting applications and discover PaperStream IP.
- Craft a malicious DLL and use the discovered vulnerability to execute arbitrary code.
- Confirm SYSTEM-level access on the target machine and extract critical information.