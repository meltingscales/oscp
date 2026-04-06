Author: Henry Post
Target: BILLYBOSS
Target IP: 1.2.3.4
Date: 04/06/2026

# Executive Summary

This machine, Billyboss, was enumerated by `nmap` to be running Sonatype Nexus on port `8081`.

The login to Nexus was brute-forced by using common words on the login page.

`CVE-2020-10199`, an authenticated Remote Code Execution vulnerability in Nexus, was used to gain a non-SYSTEM shell on the target.

The target was vulnerable to SMBGhost (`CVE-2020-0796`), but an exploit was not successful. We were not able to gain SYSTEM level access.
## Recommendations

Do not use weak passwords. Use strong passwords or key-based authentication.

Update Windows immediately and patch `CVE-2020-0796`.
# Recon

`nmap -sV -sC -T4 -oA initial BILLYBOSS` was used to discover Nexus' web service.



# Non-SYSTEM access

We use `CVE-2020-10199` in Nexus to get a non-SYSTEM shell as a local service.

We host a Python3 webserver to upload exploit files.

# SYSTEM access

We upload SMBGhost Local Privilege Escalation binary.

We execute it, but it does not work.

We upload `GodPotato.exe` and `FullPowers.exe`, but these also fail.