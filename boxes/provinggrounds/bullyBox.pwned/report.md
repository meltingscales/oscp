# Report - bullyBox

- Author: Henry Post
- Target: bullyBox
- Target IP: 192.168.60.27
- Date: 04/11/2026

# Executive Summary

The victim was enumerated by `nmap` to have a web service, "BoxBilling", running at port 80.

An open `.git/` directory was found and dumped with `git-dumper`. 

The dumped files had a `bb-config.php` file with credentials that let us login as admin on the BoxBilling site.

The BoxBilling site had an admin panel that was used to upload a PHP reverse shell and get non-root access.

Then, because the user `yuki` was a sudoer, we ran `sudo bash` to get root access.

# Recommendations

# Recon

# Non-root access

After logging in as the admin user in BoxBilling, we can upload a reverse shell PHP file, execute it, and get a reverse shell.

# Root access

Because the user `xxx` is a sudoer, we simply run `sudo bash`.

