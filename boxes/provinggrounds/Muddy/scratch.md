
# Muddy

In this lab, we'll exploit an XXE (XML External Entity Expansion) vulnerability to access credentials for a WebDAV service. By using WebDAV, we'll upload a reverse shell to establish a foothold on the target. Finally, we'll leverage a cron job PATH to elevate our access to root.

This lab demonstrates exploiting an XML External Entity (XXE) vulnerability in the Ladon framework to leak sensitive information, including WebDAV credentials. Learners will use the credentials to upload a reverse shell, gaining a foothold on the target. Privilege escalation is achieved by exploiting a writable directory in the cron job PATH to execute commands as root. This lab emphasizes XXE exploitation, web application abuse, and cron-based privilege escalation techniques.

## Learning Objectives

**After completion of this lab, learners will be able to:**

- Enumerate open ports and services, identifying the Ladon framework and WebDAV.
- Exploit the XXE vulnerability to leak sensitive information, including WebDAV credentials.
- Use the credentials to upload and trigger a reverse shell via WebDAV.
- Analyze the system's PATH and create a malicious binary in a writable directory for cron exploitation.
- Gain root access by leveraging the cron job to execute the malicious payload.



```
???(kali?kali)-[~]
??$ nmap -sS -sV $TARGET                             tun0:Down | TARGET:192.168.52.161 | 03-02-26 2:39:05
Starting Nmap 7.98 ( https://nmap.org ) at 2026-03-02 02:39 +0000
Nmap scan report for 192.168.52.161
Host is up (0.00050s latency).
Not shown: 993 closed tcp ports (reset)
PORT     STATE SERVICE       VERSION
22/tcp   open  ssh           OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
25/tcp   open  smtp          Exim smtpd
80/tcp   open  http          Apache httpd 2.4.38 ((Debian))
111/tcp  open  rpcbind       2-4 (RPC #100000)
443/tcp  open  https?
808/tcp  open  ccproxy-http?
8888/tcp open  http          WSGIServer 0.1 (Python 2.7.16)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.02 seconds

```

http://muddy.ugc:8888/muddy/