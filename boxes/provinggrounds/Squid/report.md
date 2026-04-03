# Report - Squid
Author: Henry Post
Target: SQUID
Target IP: 192.168.53.189
Date: 04/03/2026

# Executive Summary

This machine, Squid, was enumerated by `nmap` to have a Squid proxy at port 3182 open.

When connecting over the proxy, a PHPMyAdmin instance was running.

Default credentials were used to login to PHPMyAdmin.

From there, a PHP reverse shell and uploader tool were created on the victim using MySQL code to write to files.

Non-SYSTEM access was obtained, and `GodPotato.exe`, a tool which escalates privileges, along with `FullPowers.exe` were used to obtain SYSTEM level access.

## Recommendations

# Recon

# Non-SYSTEM access

# SYSTEM access
