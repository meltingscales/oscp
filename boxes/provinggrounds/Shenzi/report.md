# Report - Shenzi

- Author: Henry Post
- Target: Shenzi
- Target IP: 192.168.59.55
- Date: 04/20/2026
## Executive Summary

### Recommendations

### Resources

- https://medium.com/@ryanchamruiyang/proving-grounds-shenzi-walkthrough-b-70304399b645

## Recon

```
???(kali?kali)-[~]
??$ nmap -sS -sV shenzi
Starting Nmap 7.98 ( https://nmap.org ) at 2026-04-20 16:47 +0000
Nmap scan report for shenzi (192.168.59.55)
Host is up (0.00040s latency).
Not shown: 993 closed tcp ports (reset)
PORT     STATE SERVICE       VERSION
21/tcp   open  ftp           FileZilla ftpd 0.9.41 beta
80/tcp   open  http          Apache httpd 2.4.43 ((Win64) OpenSSL/1.1.1g PHP/7.4.6)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
443/tcp  open  ssl/http      Apache httpd 2.4.43 ((Win64) OpenSSL/1.1.1g PHP/7.4.6)
445/tcp  open  microsoft-ds?
3306/tcp open  mysql         MariaDB 10.3.24 or later (unauthorized)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 30.33 seconds
```

`nmap` shows we have FTP, HTTP, SMB, and MySQL.
## Non-root access

Let's start with SMB enumeration.

```sh
netexec smb 192.168.59.55 -u '' -p '' --users --shares
# no dice, we need credentials...
```

Let's try FTP.

```sh
wget -r ftp://Anonymous:potato123@shenzi
# no anonymous login.
```

Let's try web.

- http://shenzi/dashboard/ - XAMPP dashboard
- http://shenzi/dashboard/phpinfo.php - phpinfo
- `C:\Users\shenzi` - user folder
- http://shenzi/phpmyadmin/ - access forbidden from non-localhost

Going to consult a guide...

https://medium.com/@ryanchamruiyang/proving-grounds-shenzi-walkthrough-b-70304399b645

Okay, so apparently SMBClient is our next route.

```sh
smbclient -L ///**192.168.59.55//
# failed

smbclient -N "//192.168.59.55/Shenzi**"
# failed
```

https://medium.com/@Dpsypher/proving-ground-practice-shenzi-10e684479eb9

Another guide.

```sh
enum4linux 192.168.59.55
# failed

smbclient -N -L \\\\192.168.59.55\\
# success:
<<EOF
        Sharename       Type      Comment
        ---------       ----      -------
        IPC$            IPC       Remote IPC
        Shenzi          Disk      
Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to 192.168.59.55 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
Unable to connect with SMB1 -- no workgroup available
EOF

# Apparently "Shenzi" is a disk on SMB.

smbclient \\\\192.168.59.55\\Shenzi
```

We download these files.

![](Pasted%20image%2020260420120438.png)

We find the WordPress admin password.

5) WordPress:
   User: admin
   Password: FeltHeadwallWight357

We can use this to get a PHP reverse shell.

- http://shenzi/shenzi/ - wp page
- http://shenzi/shenzi/wp-admin - wp-admin login


## Root access

TBD

## Proof

### Local proof

- `ip a`/`ifconfig`
- `whoami`
- `hostname`
- `date`
- `cat local.txt`
(IMG_PLACEHOLDER)

### Root proof

- `ip a`/`ifconfig`
- `whoami`
- `hostname`
- `date`
- `cat proof.txt`
(IMG_PLACEHOLDER)
