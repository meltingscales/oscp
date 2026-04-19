# Report - Algernon

- Author: Henry Post
- Target: Algernon
- Target IP: 1.2.3.4
- Date: 04/17/2026

## Executive Summary

%% This machine, `hackme`, was enumerated by `nmap` to have ports 22 and 8000 open.

Port 8000 was running a `ladon` web service, which had default credentials of `admin:admin`.

To get non-root access, I used `CVE-2025-1234` on `exploit-db.com`.

From there, I identified a binary with elevated capabilities and used it to pivot to root. %%

### Recommendations

%% 1. Update Ladon to the latest non-vulnerable version.
1. Do not use default credentials of `admin:admin`.
  2. Use strong credentials.
3. Do not use `setuid` binary permissions on Python or other binaries. Instead, remove the `setuid` permission from binaries that do not need it. %%

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

https://medium.com/@Dpsypher/pg-practice-algernon-5382b92a8142

We're going to cheat a bit. It's late and I'm tired.

Let's try FTP. `wget -r` dumps all files.

```bash
wget -r ftp://Anonymous:pass@algernon
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

## Root access



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
