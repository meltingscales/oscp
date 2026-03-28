This lab demonstrates exploiting an SQL injection vulnerability in a Ruby on Rails web application to achieve remote code execution. Learners will then escalate privileges by exploiting an insecure folder permissions vulnerability in BarracudaDrive v6.5, replacing an executable to gain SYSTEM-level access after a reboot. This lab emphasizes exploiting SQL injection, web shell deployment, and service misconfigurations.

**After completion of this lab, learners will be able to:**

- Enumerate services to identify the SQL injection vulnerability in the Ruby on Rails application.
- Use the vulnerability to write a PHP web shell to the web root directory.
- Achieve remote code execution and deploy a reverse shell payload.
- Exploit insecure folder permissions in BarracudaDrive to replace an executable.
- Reboot the target to execute the malicious payload and gain SYSTEM privileges.


```
???(kali?kali)-[~]
??$ nmap -sS -sV MEDJED 
Starting Nmap 7.98 ( https://nmap.org ) at 2026-03-27 21:48 +0000
Nmap scan report for MEDJED (192.168.57.127)
Host is up (0.00045s latency).
Not shown: 995 closed tcp ports (reset)
PORT     STATE SERVICE       VERSION
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
3306/tcp open  mysql         MariaDB 10.3.24 or later (unauthorized)
8000/tcp open  http-alt      BarracudaServer.com (Windows)
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port8000-TCP:V=7.98%I=7%D=3/27%Time=69C6FB39%P=x86_64-pc-linux-gnu%r(Ge
SF:nericLines,72,"HTTP/1\.1\x20200\x20OK\r\nDate:\x20Fri,\x2027\x20Mar\x20
SF:2026\x2021:48:41\x20GMT\r\nServer:\x20BarracudaServer\.com\x20\(Windows
SF:\)\r\nConnection:\x20Close\r\n\r\n")%r(GetRequest,72,"HTTP/1\.1\x20200\
SF:x20OK\r\nDate:\x20Fri,\x2027\x20Mar\x202026\x2021:48:41\x20GMT\r\nServe
SF:r:\x20BarracudaServer\.com\x20\(Windows\)\r\nConnection:\x20Close\r\n\r
SF:\n")%r(FourOhFourRequest,72,"HTTP/1\.1\x20200\x20OK\r\nDate:\x20Fri,\x2
SF:027\x20Mar\x202026\x2021:48:46\x20GMT\r\nServer:\x20BarracudaServer\.co
SF:m\x20\(Windows\)\r\nConnection:\x20Close\r\n\r\n")%r(Socks5,72,"HTTP/1\
SF:.1\x20200\x20OK\r\nDate:\x20Fri,\x2027\x20Mar\x202026\x2021:48:46\x20GM
SF:T\r\nServer:\x20BarracudaServer\.com\x20\(Windows\)\r\nConnection:\x20C
SF:lose\r\n\r\n")%r(HTTPOptions,72,"HTTP/1\.1\x20200\x20OK\r\nDate:\x20Fri
SF:,\x2027\x20Mar\x202026\x2021:48:51\x20GMT\r\nServer:\x20BarracudaServer
SF:\.com\x20\(Windows\)\r\nConnection:\x20Close\r\n\r\n")%r(RTSPRequest,72
SF:,"HTTP/1\.1\x20200\x20OK\r\nDate:\x20Fri,\x2027\x20Mar\x202026\x2021:48
SF::51\x20GMT\r\nServer:\x20BarracudaServer\.com\x20\(Windows\)\r\nConnect
SF:ion:\x20Close\r\n\r\n")%r(SIPOptions,13C,"HTTP/1\.1\x20400\x20Bad\x20Re
SF:quest\r\nDate:\x20Fri,\x2027\x20Mar\x202026\x2021:49:53\x20GMT\r\nServe
SF:r:\x20BarracudaServer\.com\x20\(Windows\)\r\nConnection:\x20Close\r\nCo

```


http://medjed:8000/Config-Wizard/wizard/SetAdmin.lsp

neat. `admin1@gmail.com:admin1:admin1`

sqlmap set cookie. try on this guy.

```
sqlmap "http://medjed:8000/private/manage/PageManager.lsp?parent=0" --cookie="z9ZAqJtI=f632bdbd69c6fc89"

```

nope. lets actually do it a bit smarter.

what version of `BarracudaServer.com` is running?

BarracudaDrive 6.5

exploit-db time.

https://www.exploit-db.com/exploits/48789

we will revisit this later. this is not sqli.

okay, so my nmap was insufficient. there are 30XXX ports with http services. I need to start there.

```
nmap -sC -sV -o nmap.txt -p- MEDJED

cat nmap.txt
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds?
3306/tcp  open  mysql         MariaDB 10.3.24 or later (unauthorized)
5040/tcp  open  unknown
8000/tcp  open  http-alt      BarracudaServer.com (Windows)
30021/tcp open  ftp           FileZilla ftpd 0.9.41 beta
| ftp-syst:
|_  SYST: UNIX emulated by FileZilla
|_ftp-bounce: bounce working!
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| -r--r--r-- 1 ftp ftp            536 Nov 03  2020 .gitignore
33033/tcp open  unknown
| fingerprint-strings:
|   GenericLines:
|     HTTP/1.1 400 Bad Request
|   GetRequest, HTTPOptions:
|     HTTP/1.0 403 Forbidden
44330/tcp open  ssl/unknown
| ssl-cert: Subject: commonName=server demo 1024 bits/organizationName=Real Time Logic/stateOrProvinceNam>
| Not valid before: 2009-08-27T14:40:47
|_Not valid after:  2019-08-25T14:40:47
|_ssl-date: 2026-03-27T22:19:38+00:00; 0s from scanner time.
45332/tcp open  http          Apache httpd 2.4.46 ((Win64) OpenSSL/1.1.1g PHP/7.3.23)
|_http-server-header: Apache/2.4.46 (Win64) OpenSSL/1.1.1g PHP/7.3.23
| http-methods:
|_  Potentially risky methods: TRACE
|_http-title: Quiz App
45443/tcp open  http          Apache httpd 2.4.46 ((Win64) OpenSSL/1.1.1g PHP/7.3.23)
|_http-server-header: Apache/2.4.46 (Win64) OpenSSL/1.1.1g PHP/7.3.23
| http-methods:
|_  Potentially risky methods: TRACE
|_http-title: Quiz App

```


http://medjed:45332/ runs a quiz app. burp will tell us if it's sql injectable.

nope. let's try `45443`. also nope. quiz app is a rabbit hole.

`44330` runs "server demo". not useful.

okay.

https://medium.com/@vivek-kumar/offensive-security-proving-grounds-walk-through-medjed-7570cbbea087


I think we need to poke around on FTP.


```
ftp anonymous@MEDJED -p 30021
```

we can also go to `MEDJED:8000/fs`

```
http://medjed:8000/fs/C/Users/Jerren/Desktop/local.txt

pwned local flag.

http://medjed:8000/fs/C/Users/Administrator/Desktop/proof.txt

pwned root flag, lmao
```

well, that was an early pwn. but let's keep going.

```

http://medjed:33033/
# i can't use the hostname, i must use the IP.

http://192.168.52.127:33033/

```

users:

```

evren eagan
impossible is just an option
evren.eagan@company.com

joe webb
Hold the vision, trust the process
joe.webb@company.com

Jerren Valon
Only the paranoid survive.
jerren.devops@company.com

```

let's try `jerren.devops:paranoid` and load burpsuite to see if we can sql inject.

