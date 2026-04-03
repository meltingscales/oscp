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

We use FoxyProxy to access `http://192.168.53.189:8080`. It shows a PHPMyAdmin control panel.

![](Pasted%20image%2020260403144140.png)

We try `root:<BLANK>` as credentials for PHPMyAdmin, and we get in.

![](Pasted%20image%2020260403144156.png)

![](Pasted%20image%2020260403144208.png)

We also go to `phpinfo` page and see the document root is `C:\wamp\www\`.

![](Pasted%20image%2020260403144351.png)

We then go to "SQL" panel in PHPMyAdmin, where we set up an upload utility and a reverse shell.

```



```
# Non-SYSTEM access

# SYSTEM access
