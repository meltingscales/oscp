# Report - Wheels
Author: Henry Post
Target: WHEELS
Target IP: 192.168.66.202
Date: 03/25/2026
# Executive Summary

This machine, Wheels, was enumerated by `nmap` to have HTTP and SSH open.

Port `80` was running an HTTP server, which was used to extract SSH credentials by using XPATH injection.

These credentials were used to gain non-root access.

A SUID binary at `/opt/get-list`was exploited using path traversal to read the hashed password file at `/etc/shadow`. 

We then cracked the `root` user's password with `hashcat` and got root level access.

## Recommendations

# Recon

# Non-root access

# Root access