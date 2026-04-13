You are required to leverage enumeration techniques, including web enumeration, to uncover potential vulnerabilities. The lab involves exploiting CVE-2022-26134 and abusing cronjobs to gain unauthorized access. This lab focuses on understanding and exploiting vulnerabilities to enhance security awareness.

Summary

In this lab, learners exploit CVE-2022-26134, a critical Remote Code Execution (RCE) vulnerability in Atlassian Confluence (version 7.13.6). By leveraging OGNL injection, attackers gain initial access to the system, discover misconfigured cron jobs, and escalate privileges to root by manipulating executable scripts.

Learning Objectives

After completion of this lab, learners will be able to:

Perform enumeration to identify the vulnerable Confluence service on port 8090.
Use the Metasploit module to exploit the OGNL injection vulnerability and gain a shell.
Identify cron jobs running as root and check writable scripts.
Modify the cron-executed script to escalate privileges by adding SUID to /bin/bash.
Elevate to root and retrieve the final proof file.


alright. let's get crackin

