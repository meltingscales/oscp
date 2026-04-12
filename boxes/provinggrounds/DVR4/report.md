# Report - DVR4
- Author: Henry Post
- Target: DVR4
- Target IP: 192.168.52.179
- Date: 04/12/2026
# Executive Summary

The target was enumerated by `nmap` to have an HTTP server open as well as SSH.

The HTTP server is running `Argus Surveillance DVR 4.0.0.0`, which was vulnerable to a Directory Traversal vulnerability. This was used to download private SSH keys, and get a non-SYSTEM shell. 

We log in via SSH as the user `Viewer`.

In addition to private SSH keys, we download `C:\ProgramData\PY_Software\Argus Surveillance DVR\DVRParams.ini`, which contained the Administrator user's password.

We decode this encoded password using `CVE-2022-25012`, as Argus doesn't use strong encryption for the password, just a static cipher.

We use the recovered password to run a reverse shell as the Administrator user and get SYSTEM level access.
# Recommendations

Do not leave Argus' login page unprotected. Use strong authentication.

Update Argus immediately to patch the Directory Traversal vulnerability.

Do not allow the `Viewer` user to use `runas` to escalate privileges.
# Recon

# Non-SYSTEM access

# SYSTEM access