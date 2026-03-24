# Report - Nickel
Author: Henry Post
Target: NICKEL
Target IP: 192.168.61.99
Date: 03/24/2026

## Executive Summary

This machine, Nickel, was enumerated by `nmap` to have FTP, HTTP, and SSH open.

Port `8089` was running an HTTP server, which leaked a command line process that contained a user credential, `ariah`. 

This `ariah` account was used to login via SSH.

From there, we found an endpoint at `127.0.0.0.1?cmd` that allowed us to execute commands under `SYSTEM` authority.

This was used to create a privileged account and get `SYSTEM` level access over RDP.

### Recommendations

Protect command line processes and do not disclose this over HTTP.

Disable command execution endpoints like those running on `NICKEL` as it enables command injection.

Do not use passwords for SSH, but use public-private keypairs.

Do not run services as `SYSTEM` level, but a lower privileged account.

## Recon

We run `nmap -sS -sV NICKEL`.

![](Pasted%20image%2020260324124302.png)

I notice ports 21 (ftp), and port 8089 (http) and port 22 (ssh) are open.


## Non-SYSTEM access

## SYSTEM access