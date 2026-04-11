# Report - bullyBox

- Author: Henry Post
- Target: bullyBox
- Target IP: 192.168.60.27
- Date: 04/11/2026

# Executive Summary

The victim was enumerated by `nmap` to have a web service, "BoxBilling", running at port 80.

An open `.git/` directory was found and dumped with `git-dumper`. 

The dumped files had a `bb-config.php` file with credentials that let us login as admin on the BoxBilling site.

The BoxBilling site had an admin panel that was used to upload a PHP reverse shell and get non-root access.

Then, because the user `yuki` was a sudoer, we ran `sudo bash` to get root access.

# Recommendations

Do not leave `.git/` folders unsecured. Remove access or require authentication.

Remove file upload features from BoxBilling.

Do not hardcode credentials.

Do not leave users like `yuki` as sudoers. Restrict `sudo` access.

# Recon


We set up the `/etc/hosts` file.
```bash
sudo sh -c "echo '192.168.60.27 BULLYBOX' >> /etc/hosts"
sudo sh -c "echo '192.168.60.27 BULLYBOX.local' >> /etc/hosts"
```
We run an `nmap` scan.

```c
???(kali?kali)-[~]
??$ nmap bullybox.local
Starting Nmap 7.98 ( https://nmap.org ) at 2026-04-11 20:44 +0000
Nmap scan report for bullybox.local (192.168.60.27)
Host is up (0.00035s latency).
rDNS record for 192.168.60.27: BULLYBOX
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
```

![](Pasted%20image%2020260411154516.png)

We notice that HTTP is open.

We run `dirb` on the victim.

```
???(kali?kali)-[~]
??$ dirb http://bullybox.local

-----------------
DIRB v2.22    
By The Dark Raver
-----------------

START_TIME: Sat Apr 11 20:46:05 2026
URL_BASE: http://bullybox.local/
WORDLIST_FILES: /usr/share/dirb/wordlists/common.txt

-----------------

GENERATED WORDS: 4612                                                          

---- Scanning URL: http://bullybox.local/ ----
+ http://bullybox.local/.git/HEAD (CODE:200|SIZE:23) 
```

We notice `.git/` is open.

We install `git-dumper` with `pipx`, and run it.

```sh
pipx install git-dumper

git-dumper http://bullybox.local/.git git-loot

cd git-loot/

ls bb-config.php
```


![](Pasted%20image%2020260411154820.png)

We get `bb-config.php`, which has credentials we later use.

![](Pasted%20image%2020260411154906.png)

`admin:Playing-Unstylish7-Provided` is the credential.

# Non-root access

After logging in as the admin user in BoxBilling, we can upload a reverse shell PHP file, execute it, and get a reverse shell.

We get a reverse shell from `nc` listener.

![](Pasted%20image%2020260411154417.png)



# Root access

Because the user `xxx` is a sudoer, we simply run `sudo bash`.

