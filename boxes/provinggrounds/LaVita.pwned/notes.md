The lab will leverage enumeration techniques, including web enumeration, to uncover potential vulnerabilities. You will also exploit CVE-2021-3129 and demonstrate how to abuse SUDO permissions for unauthorized access. This lab focuses on understanding and exploiting vulnerabilities to enhance security awareness.

Summary

This lab challenges learners to exploit a misconfigured APP_DEBUG setting in a Laravel 8.4.0 application. Using CVE-2021-3129, an unauthenticated Remote Code Execution (RCE) vulnerability in Laravel's Ignition component, attackers can execute arbitrary code, gain reverse shells, and escalate privileges to root through misconfigurations.

Learning Objectives

**After completion of this lab, learners will be able to:**

- Enumerate services on the target machine and identify Laravel running on port 80.
- Exploit the APP_DEBUG misconfiguration to trigger the CVE-2021-3129 RCE.
- Obtain an initial shell as the www-data user by leveraging the Laravel exploit script.
- Identify privilege escalation opportunities, including artisan commands and file permissions.
- Escalate to root access by exploiting sudo privileges for composer and achieve full system control.