# Report - Sizzle - HTB

- Author: Henry Post
- Target: Sizzle (HTB)
- Target IP: 10.129.54.76
- Attacker IP: 10.10.14.145
- Date: 03/01/2026

## Executive Summary



### Recommendations

 

## Resources

- a
- b
- c

## Recon

We first get the ports, then run a service scan.

```sh
ports=$(nmap -p- --min-rate=1000 -T4 10.129.54.76 | grep ^[0-9] | cut -d '/' -f 1 | tr '\n' ',' | sed s/,$//) 
# 21,53,80,135,139,389,443,445,464,593,636,3268,3269,5985,5986,9389,47001,49664,49665,49668,49670,49672,49686,49687,49691,49694,49709,49729,49747


nmap -p$ports -sC -sV 10.129.54.76
<<EOF
- 21/ftp
- 53/dns
- 80/http
- 135/msrpc
- 139/netbios-ssn
- 389/ldap
- 443/https
- kerberos
- a bunch more ldap ports
- 9389/mc-nmf (.net message framing)
- more RPC
EOF
```

Okay. Using a guide because apparently sizzle is insanely difficult.

http://10.129.54.76 - Neat gif of some bacon. :P

```sh

gobuster dir -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -t 100 -u http://10.129.54.76/

# Nothing interesting.
```

Let's try FTP.

According to the guide,

> Anonymous login was allowed on FTP but it had no contents.

```sh
ftp 10.129.54.76
# No files
```

## Non-root access

.
## Root access

.
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
