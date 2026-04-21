In this lab, you will exploit a remote file inclusion vulnerability in a web application. You will then escalate privileges by leveraging misconfigured permissions on an executable that operates under the system job scheduler. This exercise enhances your skills in vulnerability exploitation and privilege escalation techniques.

## Summary

This lab demonstrates exploiting a remote file inclusion vulnerability in a web application to execute arbitrary commands and deploy a reverse shell. Learners will escalate privileges by replacing a scheduled executable with a malicious payload, leveraging weak file permissions and an administrative task scheduler. The lab highlights web application vulnerabilities and improper file permission practices.

## Learning Objectives

**After completion of this lab, learners will be able to:**

- Enumerate open services and identify the web application vulnerable to remote file inclusion.
- Exploit the RFI vulnerability to execute arbitrary commands on the target system.
- Deploy a reverse shell payload to establish persistent access to the target.
- Identify misconfigured permissions on files executed by a scheduled task.
- Replace the scheduled executable with a malicious payload to achieve privilege escalation.