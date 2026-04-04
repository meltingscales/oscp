This lab involves exploiting Sonatype Nexus 3.21.0-05 for authenticated remote code execution and using the SMBGhost vulnerability to escalate privileges. Learners will craft payloads to gain initial access and leverage an unpatched SMB service to obtain a SYSTEM shell. The lab highlights web application vulnerabilities and critical privilege escalation techniques.

ok lets get crackin

```
???(kali?kali)-[~]
??$ nmap -sV -sC -T4 -oA initial 192.168.60.61
Starting Nmap 7.98 ( https://nmap.org ) at 2026-04-04 21:13 +0000
Nmap scan report for 192.168.60.61
Host is up (0.00088s latency).
Not shown: 994 closed tcp ports (reset)
PORT     STATE SERVICE       VERSION
21/tcp   open  ftp           Microsoft ftpd
| ftp-syst: 
|_  SYST: Windows_NT
80/tcp   open  http          Microsoft IIS httpd 10.0
|_http-server-header: Microsoft-IIS/10.0
|_http-cors: HEAD GET POST PUT DELETE TRACE OPTIONS CONNECT PATCH
|_http-title: BaGet
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
8081/tcp open  http          Jetty 9.4.18.v20190429
|_http-server-header: Nexus/3.21.0-05 (OSS)
| http-robots.txt: 2 disallowed entries 
|_/repository/ /service/
|_http-title: Nexus Repository Manager
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2026-04-04T21:13:28
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 28.62 seconds

```

okay. FTP, SonaType on port `8081`. let's search exploit-db for ...what version is it running, I wonder.

```
Sonatype
Sonatype Nexus Repository Manager OSS 3.21.0-05
```

rce auth'd
https://www.exploit-db.com/exploits/49385

cool. now we just need to log in first to get RCE.

- Use default credentials to access the application and execute commands to deploy a reverse shell.

ok.

`admin:admin123`

nope.

let's uh.

 `/opt/sonatype-work/nexus3/admin.password`

try to steal this.

path traversal
https://www.exploit-db.com/exploits/52101

ok. a bit stuck. 8/30 boxes in, let's use a guide.

https://banua.medium.com/proving-grounds-billyboss-oscp-prep-2025-practice-10-8bbf7ed4dc0f

okay, so he uses a wordlist.

```sh
cewl --lowercase http://BILLYBOSS:8081/ | grep -v CeWL > wordlists.txt

hydra -I -f -L wordlists.txt -P wordlists.txt “http-post-form://BILLYBOSS:8081/service/rapture/session:username=^USER64^&password=^PASS64^:F=403”
```