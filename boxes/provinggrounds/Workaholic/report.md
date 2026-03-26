# Report - Workaholic

Author: Henry Post
Target: WORKAHOLIC
Target IP: 192.168.61.229

# Executive Summary

This machine, Workaholic, was enumerated by nmap to have FTP, HTTP, and SSH open.

The HTTP server was running WordPress which was vulnerable to CVE-2024-9796. This CVE was used to dump a list of users and password hashes on WordPress.

The hashes were cracked, and we found a user, `ted`, that had an FTP login.

From FTP, we downloaded `wp-config.php` which had more credentials in it.

We used `hydra` to enumerate SSH and found that `charlie` had a login on SSH.

We got the user flag from SSH, and used `find / -perm -u=s -type f 2>/dev/null | grep -v snap` to find binaries with SUID set, meaning they can run as root.

We found `/var/www/html/wordpress/blog/wp-monitor` as a SUID binary, ran `strings` on it to discover it loaded shared objects from a specific directory, and used C shared object injection to get root.

## Recommendations

Upgrade WordPress plugins vulnerable to CVE-2024-9796 immediately.

Close unnecessary ports like FTP or SSH if they do not need to be open.

Consider using private-public key auth for SSH instead of passwords.

Do not allow FTP users to access sensitive files.

Do not set SUID on binaries that do not need it.

Do not load shared objects if you can avoid it.

## References

- <https://github.com/meltingscales/CVE-2024-9796>

# Recon

We ran `nmap -sS -sV WORKAHOLIC`.



# Non-root access

# Root access
