# Report - Exghost

Author: Henry Post
Target: Exghost
Target IP: 192.168.53.183
Attacker IP: 192.168.49.53
Date: 03/12/2026

## Executive Summary

This machine, Exghost, was enumerated by `nmap` to have ports `21` (ftp) and `80` (http) open.

The FTP password was brute-forced and found to be `user:system`. 

On the FTP drive, a WireShark packet capture file showed that a PHP website was hosting `ExifTool` version `12.23`, which was vulnerable to `CVE-2021-22204`. This vulnerability gave us local user access.

From non-root access, we discovered that `/usr/lib/policykit-1/` existed, and realizing that the `/usr/lib/policykit-1/polkit-agent-helper-1` file was last updated on May 26, 2021, this meant that polkit is vulnerable to `CVE-2021-4034` aka "PwnKit", which is a privilege escalation vulnerability.

`CVE-2021-4034` "PwnKit" was used to pivot to root access.

## Recon

We see that port 21 and port 80 are open.

    nmap -sS -sV 192.168.53.183

![](Pasted%20image%2020260312225417.png)

## FTP Access

Let's start with a brute force attack.

