# Report - QuackerJack

Author: Henry Post  
Target: QUACKERJACK  
Target IP: 192.168.52.67  
Date: 04/08/2026  
# Executive Summary

This machine, QuackerJack, was enumerated by `nmap` to have port `8081` open, running rConfig version `3.9.4`.

rConfig was vulnerable to two CVEs.

`CVE-2020-10220` was used to dump users and password hashes from the victim, and `CVE-2019-19509` was used to get a non-root reverse shell.

A SUID-set binary was found at `/usr/bin/find`, and this was used to pivot to a root shell.

# Recommendations

Update rConfig to the latest non-vulnerable version.

Do not set SUID bit on binaries that do not need it.

Use strong passwords for admin accounts.

# References

- https://gtfobins.org/gtfobins/find/
- https://www.exploit-db.com/exploits/47982
- https://md5.gromweb.com/?md5=dc40b85276a1f4d7cb35f154236aa1b2
- https://raw.githubusercontent.com/v1k1ngfr/exploits-rconfig/refs/heads/master/rconfig_CVE-2020-10220.py

# Recon

# Non-root access

# Root access