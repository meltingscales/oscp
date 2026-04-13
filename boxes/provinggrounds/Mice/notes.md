In this lab, the RemoteMouse 3.008 exploit will be used on port 1978 for remote code execution, capturing a reverse shell with Netcat. After decoding the FileZilla password, we will log in via Remote Desktop and open a Command Prompt as an administrator. This lab focuses on exploiting service vulnerabilities and privilege escalation methods.

Summary

This lab demonstrates exploiting RemoteMouse 3.008 to achieve remote code execution via a modified exploit that delivers a reverse shell. Learners will escalate privileges by extracting and decoding credentials from FileZilla's configuration files, gaining RDP access as a user. Finally, they will exploit the RemoteMouse application's admin privileges to spawn a Command Prompt as Administrator. This lab emphasizes RCE, credential exploitation, and leveraging application misconfigurations for privilege escalation.

Learning Objectives

**After completion of this lab, learners will be able to:**

- Perform a full port scan to identify services and vulnerabilities on the target.
- Exploit RemoteMouse 3.008 to achieve remote code execution and a reverse shell.
- Enumerate FileZilla configuration files to extract encoded user credentials.
- Decode the extracted credentials and log in via RDP.
- Use RemoteMouse's privileged settings to spawn a Command Prompt with Administrator access.


alright. easy lab, I got lucky. lets get crackin.