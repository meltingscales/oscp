
???(kali?kali)-[~]
??$ enum4linux -a clamav
Starting enum4linux v0.9.1 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Sun Jun  7 20:44:35 2026

 =========================================( Target Information )=========================================
                                                                                                          
Target ........... clamav                                                                                 
RID Range ........ 500-550,1000-1050
Username ......... ''
Password ......... ''
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none


 ===============================( Enumerating Workgroup/Domain on clamav )===============================
                                                                                                          
                                                                                                          
[+] Got domain/workgroup name: WORKGROUP                                                                  
                                                                                                          
                                                                                                          
 ===================================( Nbtstat Information for clamav )===================================
                                                                                                          
Looking up status of 192.168.52.42                                                                        
        0XBABE          <00> -         B <ACTIVE>  Workstation Service
        0XBABE          <03> -         B <ACTIVE>  Messenger Service
        0XBABE          <20> -         B <ACTIVE>  File Server Service
        ..__MSBROWSE__. <01> - <GROUP> B <ACTIVE>  Master Browser
        WORKGROUP       <00> - <GROUP> B <ACTIVE>  Domain/Workgroup Name
        WORKGROUP       <1d> -         B <ACTIVE>  Master Browser
        WORKGROUP       <1e> - <GROUP> B <ACTIVE>  Browser Service Elections

        MAC Address = 00-00-00-00-00-00



 ==========================================( Users on clamav )==========================================
                                                                                                          
index: 0x1 RID: 0x3f2 acb: 0x00000011 Account: games    Name: games     Desc: (null)                      
index: 0x2 RID: 0x1f5 acb: 0x00000011 Account: nobody   Name: nobody    Desc: (null)
index: 0x3 RID: 0x402 acb: 0x00000011 Account: proxy    Name: proxy     Desc: (null)
index: 0x4 RID: 0x42a acb: 0x00000011 Account: www-data Name: www-data  Desc: (null)
index: 0x5 RID: 0x3e8 acb: 0x00000011 Account: root     Name: root      Desc: (null)
index: 0x6 RID: 0x3fa acb: 0x00000011 Account: news     Name: news      Desc: (null)
index: 0x7 RID: 0x3ec acb: 0x00000011 Account: bin      Name: bin       Desc: (null)
index: 0x8 RID: 0x3f8 acb: 0x00000011 Account: mail     Name: mail      Desc: (null)
index: 0x9 RID: 0x3ea acb: 0x00000011 Account: daemon   Name: daemon    Desc: (null)
index: 0xa RID: 0xbb8 acb: 0x00000011 Account: ryu      Name: ryu,,,    Desc: (null)
index: 0xb RID: 0x3f4 acb: 0x00000011 Account: man      Name: man       Desc: (null)
index: 0xc RID: 0x3f6 acb: 0x00000011 Account: lp       Name: lp        Desc: (null)
index: 0xd RID: 0x4b4 acb: 0x00000011 Account: Debian-exim      Name: (null)    Desc: (null)
index: 0xe RID: 0x43a acb: 0x00000011 Account: gnats    Name: Gnats Bug-Reporting System (admin)        Desc: (null)
index: 0xf RID: 0x42c acb: 0x00000011 Account: backup   Name: backup    Desc: (null)
index: 0x10 RID: 0x3ee acb: 0x00000011 Account: sys     Name: sys       Desc: (null)
index: 0x11 RID: 0x434 acb: 0x00000011 Account: list    Name: Mailing List Manager      Desc: (null)
index: 0x12 RID: 0x436 acb: 0x00000011 Account: irc     Name: ircd      Desc: (null)
index: 0x13 RID: 0x3f0 acb: 0x00000011 Account: sync    Name: sync      Desc: (null)
index: 0x14 RID: 0x3fc acb: 0x00000011 Account: uucp    Name: uucp      Desc: (null)

user:[games] rid:[0x3f2]
user:[nobody] rid:[0x1f5]
user:[proxy] rid:[0x402]
user:[www-data] rid:[0x42a]
user:[root] rid:[0x3e8]
user:[news] rid:[0x3fa]
user:[bin] rid:[0x3ec]
user:[mail] rid:[0x3f8]
user:[daemon] rid:[0x3ea]
user:[ryu] rid:[0xbb8]
user:[man] rid:[0x3f4]
user:[lp] rid:[0x3f6]
user:[Debian-exim] rid:[0x4b4]
user:[gnats] rid:[0x43a]
user:[backup] rid:[0x42c]
user:[sys] rid:[0x3ee]
user:[list] rid:[0x434]
user:[irc] rid:[0x436]
user:[sync] rid:[0x3f0]
user:[uucp] rid:[0x3fc]



 ====================================( Share Enumeration on clamav )====================================
                                                                                                          
                                                                                                          
        Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        IPC$            IPC       IPC Service (0xbabe server (Samba 3.0.14a-Debian) brave pig)
        ADMIN$          IPC       IPC Service (0xbabe server (Samba 3.0.14a-Debian) brave pig)
Reconnecting with SMB1 for workgroup listing.

        Server               Comment
        ---------            -------
        0XBABE               0xbabe server (Samba 3.0.14a-Debian) brave pig

        Workgroup            Master
        ---------            -------
        WORKGROUP            0XBABE

[+] Attempting to map shares on clamav                                                                    

 ===============================( Password Policy Information for clamav )===============================
                                                                                                          
Password:                                                                                                 


[+] Attaching to clamav using a NULL share

[+] Trying protocol 139/SMB...

[+] Found domain(s):

        [+] 0XBABE
        [+] Builtin

[+] Password Info for Domain: 0XBABE

        [+] Minimum password length: 5
        [+] Password history length: None
        [+] Maximum password age: Not Set
        [+] Password Complexity Flags: 000000

                [+] Domain Refuse Password Change: 0
                [+] Domain Password Store Cleartext: 0
                [+] Domain Password Lockout Admins: 0
                [+] Domain Password No Clear Change: 0
                [+] Domain Password No Anon Change: 0
                [+] Domain Password Complex: 0

        [+] Minimum password age: None
        [+] Reset Account Lockout Counter: 30 minutes 
        [+] Locked Account Duration: 30 minutes 
        [+] Account Lockout Threshold: None
        [+] Forced Log off Time: Not Set


 [+] Getting builtin groups:                                                                               
                                                                                                          
group:[System Operators] rid:[0x225]                                                                      
group:[Replicators] rid:[0x228]
group:[Guests] rid:[0x222]
group:[Power Users] rid:[0x223]
group:[Print Operators] rid:[0x226]
group:[Administrators] rid:[0x220]
group:[Account Operators] rid:[0x224]
group:[Backup Operators] rid:[0x227]
group:[Users] rid:[0x221]

 
 
 =====================( Users on clamav via RID cycling (RIDS: 500-550,1000-1050) )=====================
                                                                                                          
                                                                                                          
[I] Found new SID:                                                                                        
S-1-5-21-1974239401-1762029558-4115558683                                                                 

[+] Enumerating users using SID S-1-5-21-1974239401-1762029558-4115558683 and logon username '', password ''                                                                                                        
                                                                                                          
S-1-5-21-1974239401-1762029558-4115558683-500 0XBABE\Administrator (Local User)                           
S-1-5-21-1974239401-1762029558-4115558683-501 0XBABE\nobody (Local User)
S-1-5-21-1974239401-1762029558-4115558683-512 0XBABE\Domain Admins (Domain Group)
S-1-5-21-1974239401-1762029558-4115558683-513 0XBABE\Domain Users (Domain Group)
S-1-5-21-1974239401-1762029558-4115558683-514 0XBABE\Domain Guests (Domain Group)
S-1-5-21-1974239401-1762029558-4115558683-1000 0XBABE\root (Local User)
S-1-5-21-1974239401-1762029558-4115558683-1001 0XBABE\root (Domain Group)
S-1-5-21-1974239401-1762029558-4115558683-1002 0XBABE\daemon (Local User)
S-1-5-21-1974239401-1762029558-4115558683-1003 0XBABE\daemon (Domain Group)
S-1-5-21-1974239401-1762029558-4115558683-1004 0XBABE\bin (Local User)
S-1-5-21-1974239401-1762029558-4115558683-1005 0XBABE\bin (Domain Group)
S-1-5-21-1974239401-1762029558-4115558683-1006 0XBABE\sys (Local User)
S-1-5-21-1974239401-1762029558-4115558683-1007 0XBABE\sys (Domain Group)
S-1-5-21-1974239401-1762029558-4115558683-1008 0XBABE\sync (Local User)
S-1-5-21-1974239401-1762029558-4115558683-1009 0XBABE\adm (Domain Group)
S-1-5-21-1974239401-1762029558-4115558683-1010 0XBABE\games (Local User)
S-1-5-21-1974239401-1762029558-4115558683-1011 0XBABE\tty (Domain Group)
S-1-5-21-1974239401-1762029558-4115558683-1012 0XBABE\man (Local User)
S-1-5-21-1974239401-1762029558-4115558683-1013 0XBABE\disk (Domain Group)
S-1-5-21-1974239401-1762029558-4115558683-1014 0XBABE\lp (Local User)
S-1-5-21-1974239401-1762029558-4115558683-1015 0XBABE\lp (Domain Group)
S-1-5-21-1974239401-1762029558-4115558683-1016 0XBABE\mail (Local User)
S-1-5-21-1974239401-1762029558-4115558683-1017 0XBABE\mail (Domain Group)
S-1-5-21-1974239401-1762029558-4115558683-1018 0XBABE\news (Local User)
S-1-5-21-1974239401-1762029558-4115558683-1019 0XBABE\news (Domain Group)
S-1-5-21-1974239401-1762029558-4115558683-1020 0XBABE\uucp (Local User)
S-1-5-21-1974239401-1762029558-4115558683-1021 0XBABE\uucp (Domain Group)
S-1-5-21-1974239401-1762029558-4115558683-1025 0XBABE\man (Domain Group)
S-1-5-21-1974239401-1762029558-4115558683-1026 0XBABE\proxy (Local User)
S-1-5-21-1974239401-1762029558-4115558683-1027 0XBABE\proxy (Domain Group)
S-1-5-21-1974239401-1762029558-4115558683-1031 0XBABE\kmem (Domain Group)
S-1-5-21-1974239401-1762029558-4115558683-1041 0XBABE\dialout (Domain Group)
S-1-5-21-1974239401-1762029558-4115558683-1043 0XBABE\fax (Domain Group)
S-1-5-21-1974239401-1762029558-4115558683-1045 0XBABE\voice (Domain Group)
S-1-5-21-1974239401-1762029558-4115558683-1049 0XBABE\cdrom (Domain Group)

 ==================================( Getting printer info for clamav )==================================
                                                                                                          
No printers returned.                                                                                     


enum4linux complete on Sun Jun  7 20:44:42 2026
