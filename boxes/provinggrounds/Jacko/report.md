# Report - Jacko
- Author: Henry Post
- Target: Jacko
- Target IP: 192.168.53.66
- Date: 04/15/2026
# Executive Summary

# Recommendations

# Resources

# Recon

We run `nmap` on our target.

```
???(kali?kali)-[~]
??$ nmap -sS -sV jacko
Starting Nmap 7.98 ( https://nmap.org ) at 2026-04-16 00:34 +0000
Nmap scan report for jacko (192.168.53.66)
Host is up (0.00049s latency).
Not shown: 995 closed tcp ports (reset)
PORT     STATE SERVICE       VERSION
80/tcp   open  http          Microsoft IIS httpd 10.0
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
8082/tcp open  http          H2 database http console
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 17.16 seconds
```

We notice that `80/HTTP` and `H2/8080` are open.

# Non-SYSTEM access

# SYSTEM access