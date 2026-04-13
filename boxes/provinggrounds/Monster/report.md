# Report - Monster

# Executive Summary

# Recommendations

# Resources

# Recon

```sh
sudo nano /etc/hosts

nmap -sV -sC -T4 -oA initial MONSTER
```

We notice that ports 80, 443, and 3389 (RDP) are open. It looks like port 80 and 443 serve the same content.

```txt
???(kali?kali)-[~]
??$ nmap -sV -sC -T4 -oA initial MONSTER
Starting Nmap 7.98 ( https://nmap.org ) at 2026-04-13 21:47 +0000
Nmap scan report for MONSTER (192.168.62.180)
Host is up (0.00039s latency).
Not shown: 994 closed tcp ports (reset)
PORT     STATE SERVICE       VERSION
80/tcp   open  http          Apache httpd 2.4.41 ((Win64) OpenSSL/1.1.1c PHP/7.3.10)
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Apache/2.4.41 (Win64) OpenSSL/1.1.1c PHP/7.3.10
|_http-title: Mike Wazowski
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
443/tcp  open  ssl/http      Apache httpd 2.4.41 ((Win64) OpenSSL/1.1.1c PHP/7.3.10)
|_ssl-date: TLS randomness does not represent time
| tls-alpn: 
|_  http/1.1
|_http-title: Mike Wazowski
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Apache/2.4.41 (Win64) OpenSSL/1.1.1c PHP/7.3.10
| ssl-cert: Subject: commonName=localhost
| Not valid before: 2009-11-10T23:48:47
|_Not valid after:  2019-11-08T23:48:47
445/tcp  open  microsoft-ds?
3389/tcp open  ms-wbt-server Microsoft Terminal Services
| rdp-ntlm-info: 
|   Target_Name: MIKE-PC
|   NetBIOS_Domain_Name: MIKE-PC
|   NetBIOS_Computer_Name: MIKE-PC
|   DNS_Domain_Name: Mike-PC
|   DNS_Computer_Name: Mike-PC
|   Product_Version: 10.0.19041
|_  System_Time: 2026-04-13T21:48:13+00:00
|_ssl-date: 2026-04-13T21:48:21+00:00; 0s from scanner time.
| ssl-cert: Subject: commonName=Mike-PC
| Not valid before: 2026-04-12T21:45:32
|_Not valid after:  2026-10-12T21:45:32
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2026-04-13T21:48:16
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 22.92 seconds
```

![](Pasted%20image%2020260413165148.png)

We get some useful data from this.

```txt
Name Mike Wazowski
Age 23 Years
Experience 4 Years
Country USA
Location Alpha Centauri
e-mail wazowski@offsec.pg
Phone + 1410 1411 1418
Freelance Available
```

We also run `dirb https://monster`.

https://monster/blog/admin/



# Non-root access

# Root access