# Report - ClamAV

- Author: Henry Post
- Target: ClamAV
- Target IP: 192.168.52.42
- Attacker IP: 192.168.49.52
- Date: 06/07/2026

## Executive Summary

This machine, `hackme`, was enumerated by `nmap` to have ports 22 and 8000 open.

Port 8000 was running a `ladon` web service, which had default credentials of `admin:admin`.

To get non-root access, I used `CVE-2025-1234` on `exploit-db.com`.

From there, I identified a binary with elevated capabilities and used it to pivot to root.

### Recommendations

1. Update Ladon to the latest non-vulnerable version.
2. Do not use default credentials of `admin:admin`.
  3. Use strong credentials.
4. Do not use `setuid` binary permissions on Python or other binaries. Instead, remove the `setuid` permission from binaries that do not need it.

## Resources

- resource1
- github link
- medium link
- exploit-db link

## Recon

I ran an nmap scan that enumerated their ports:

    nmap -sS -sV clamav

```txt

???(kali?kali)-[~]
??$ nmap -sS -sV -p- clamav
Starting Nmap 7.98 ( https://nmap.org ) at 2026-06-07 20:29 +0000
Nmap scan report for clamav (192.168.52.42)
Host is up (0.00028s latency).
Not shown: 65528 closed tcp ports (reset)
PORT      STATE SERVICE     VERSION
22/tcp    open  ssh         OpenSSH 3.8.1p1 Debian 8.sarge.6 (protocol 2.0)
25/tcp    open  smtp        Sendmail 8.13.4/8.13.4/Debian-3sarge3
80/tcp    open  http        Apache httpd 1.3.33 ((Debian GNU/Linux))
139/tcp   open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
199/tcp   open  smux        Linux SNMP multiplexer
445/tcp   open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
60000/tcp open  ssh         OpenSSH 3.8.1p1 Debian 8.sarge.6 (protocol 2.0)
Service Info: Host: localhost.localdomain; OSs: Linux, Unix; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 42.14 seconds
```

Let's check HTTP.

We get an HTML response with this text:

```txt
01101001 01100110 01111001 01101111 01110101 01100100 01101111 01101110 01110100 01110000 01110111 01101110 01101101 01100101 01110101 01110010 01100001 01101110 00110000 0011 0000 01100010 
```

`Ph33r` as title, and message is `ifyoudontpwnmeuran00b`. Cute.

For SSH, we can't SSH until we fix our kex algo.

```txt
???(kali?kali)-[~]
??$ ssh clamav -p 60000
Unable to negotiate with 192.168.52.42 port 60000: no matching key exchange method found. Their offer: diffie-hellman-group-exchange-sha1,diffie-hellman-group1-sha1
                                                                                                          
???(kali?kali)-[~]
??$ ssh clamav -p 22   
Unable to negotiate with 192.168.52.42 port 22: no matching key exchange method found. Their offer: diffie-hellman-group-exchange-sha1,diffie-hellman-group1-sha1

```

Let's try dirb on `http://clamav`.

Nothing interesting.

Claude says:

1. SMTP: SendMail is ancient, do user enumeration via VRFY/EXPN, and check for SendMail exploits. `nc clamav 25; VRFY root; EXPN root;`
2. SMB: Run `enum4linux -a clamav` and `smbclient -L //clamav -N`.
3. SNMP: Can leak system info, try `snmpwalk -v1 -c public clamav` or `snmp-check clamav`.
4. HTTP: Can try `nikto -h http://clamav` or `gobuster`.

We can always use `searchsploit sendmail`. Keep in mind it's `Sendmail 8.13.4`.

Let's start with SMTP.

```sh
nc clamav 25
HELO test

VRFY root

EXPN root
```

It gives us some interesting output.

```txt
                                                                                                          
???(kali?kali)-[~]
??$ nc clamav 25           
220 localhost.localdomain ESMTP Sendmail 8.13.4/8.13.4/Debian-3sarge3; Sun, 7 Jun 2026 20:41:37 -0400; (No UCE/UBE) logging access from: [192.168.49.52](FAIL)-[192.168.49.52]
VRFY root
503 5.0.0 I demand that you introduce yourself first
EXPN root
503 5.0.0 I demand that you introduce yourself first
HELO test
250 localhost.localdomain Hello [192.168.49.52], pleased to meet you
VRFY root
250 2.1.5 <root@localhost.localdomain>
EXPN root
250 2.1.5 root <root@localhost.localdomain>
VRFY www-data
250 2.1.5 www-data <www-data@localhost.localdomain>
VRFY nobody
250 2.1.5 <nobody@localhost.localdomain>

```

Let's try `smtp-user-enum`...

```sh
smtp-user-enum -M VRFY -U /usr/share/wordlists/metasploit/unix_users.txt -t clamav
<<EOF
######## Scan started at Sun Jun  7 20:43:18 2026 #########
clamav: backup exists
clamav: bin exists
clamav: daemon exists
clamav: ftp exists
clamav: games exists
clamav: gnats exists
clamav: irc exists
clamav: list exists
clamav: lp exists
clamav: mail exists
clamav: man exists
clamav: news exists
clamav: nobody exists
clamav: postmaster exists
clamav: proxy exists
clamav: root exists
clamav: ROOT exists
clamav: sshd exists
clamav: sync exists
clamav: sys exists
clamav: uucp exists
clamav: webmaster exists
clamav: www exists
clamav: www-data exists
######## Scan completed at Sun Jun  7 20:43:18 2026 #########
24 results.
EOF
```

Neat. Some users exist.

Let's move on to SMB.

2. SMB: Run `enum4linux -a clamav` and `smbclient -L //clamav -N`.

```txt
(see adjacent doc), enum4linux.md
```

```txt
???(kali?kali)-[~]
??$ smbclient -L //clamav -N                                                          

        Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        IPC$            IPC       IPC Service (0xbabe server (Samba 3.0.14a-Debian) brave pig)
        ADMIN$          IPC       IPC Service (0xbabe server (Samba 3.0.14a-Debian) brave pig)
Reconnecting with SMB1 for workgroup listing.

        Server               Comment
        ---------            -------
        0XBABE               0xbabe server (Samba 3.0.14a-Debian) brave pig

        Workgroup            Master
        ---------            -------
        WORKGROUP            0XBABE

```

On to #3...

3. SNMP: Can leak system info, try `snmpwalk -v1 -c public clamav` or `snmp-check clamav`.

```sh
snmpwalk -v1 -c public clamav

<<EOF
iso.3.6.1.2.1.1.1.0 = STRING: "Linux 0xbabe.local 2.6.8-4-386 #1 Wed Feb 20 06:15:54 UTC 2008 i686"
iso.3.6.1.2.1.1.2.0 = OID: iso.3.6.1.4.1.8072.3.2.10
iso.3.6.1.2.1.1.3.0 = Timeticks: (130263) 0:21:42.63
iso.3.6.1.2.1.1.4.0 = STRING: "Root <root@localhost> (configure /etc/snmp/snmpd.local.conf)"
iso.3.6.1.2.1.1.5.0 = STRING: "0xbabe.local"
iso.3.6.1.2.1.1.6.0 = STRING: "Unknown (configure /etc/snmp/snmpd.local.conf)"
iso.3.6.1.2.1.1.8.0 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.2.1 = OID: iso.3.6.1.2.1.31
iso.3.6.1.2.1.1.9.1.2.2 = OID: iso.3.6.1.6.3.1
iso.3.6.1.2.1.1.9.1.2.3 = OID: iso.3.6.1.2.1.49
iso.3.6.1.2.1.1.9.1.2.4 = OID: iso.3.6.1.2.1.4
iso.3.6.1.2.1.1.9.1.2.5 = OID: iso.3.6.1.2.1.50
iso.3.6.1.2.1.1.9.1.2.6 = OID: iso.3.6.1.6.3.16.2.2.1
iso.3.6.1.2.1.1.9.1.2.7 = OID: iso.3.6.1.6.3.10.3.1.1
iso.3.6.1.2.1.1.9.1.2.8 = OID: iso.3.6.1.6.3.11.3.1.1
iso.3.6.1.2.1.1.9.1.2.9 = OID: iso.3.6.1.6.3.15.2.1.1
iso.3.6.1.2.1.1.9.1.3.1 = STRING: "The MIB module to describe generic objects for network interface sub-layers"
iso.3.6.1.2.1.1.9.1.3.2 = STRING: "The MIB module for SNMPv2 entities"
iso.3.6.1.2.1.1.9.1.3.3 = STRING: "The MIB module for managing TCP implementations"
iso.3.6.1.2.1.1.9.1.3.4 = STRING: "The MIB module for managing IP and ICMP implementations"
iso.3.6.1.2.1.1.9.1.3.5 = STRING: "The MIB module for managing UDP implementations"
iso.3.6.1.2.1.1.9.1.3.6 = STRING: "View-based Access Control Model for SNMP."
iso.3.6.1.2.1.1.9.1.3.7 = STRING: "The SNMP Management Architecture MIB."
iso.3.6.1.2.1.1.9.1.3.8 = STRING: "The MIB for Message Processing and Dispatching."
iso.3.6.1.2.1.1.9.1.3.9 = STRING: "The management information definitions for the SNMP User-based Security Model."
EOF
```

Now to try `snmp-check`.

```sh
snmp-check 192.168.52.42

<<EOF

processes:
 
  3776                  runnable              clamd                 /usr/local/sbin/clamd                      
  3778                  runnable              clamav-milter         /usr/local/sbin/clamav-milter  --black-hole-mode -l -o -q /var/run/clamav/clamav-milter.ctl

EOF
```

Cool. Let's use `searchsploit sendmail`. Keep in mind it's `Sendmail 8.13.4`.

Let's try this one:

```txt
Sendmail with clamav-milter < 0.91.2 - Remote Command Execution         | multiple/remote/4761.pl
```

```sh
searchsploit --path 4761
# /usr/share/exploitdb/exploits/multiple/remote/4761.pl

cp /usr/share/exploitdb/exploits/multiple/remote/4761.pl ./

# in separate terminal...
nc -nvlp 31337

perl 4761.pl clamav
```

This one fails.

Here's the full list:

```txt
???(kali?kali)-[~]
??$ searchsploit sendmail   
------------------------------------------------------------------------ ---------------------------------
 Exploit Title                                                          |  Path
------------------------------------------------------------------------ ---------------------------------
Berkeley Sendmail 5.58 - Debug                                          | linux/remote/19028.txt
BSD 2 / CND 1 / Sendmail 8.x / FreeBSD 2.1.x / HP-UX 10.x / AIX 4 / Red | multiple/local/19556.sh
Caldera OpenLinux 2.2 / Debian 2.1/2.2 / RedHat 6.0 - Vixie Cron MAILTO | linux/local/19474.txt
ClamAV Milter 0.92.2 - Blackhole-Mode (Sendmail) Code Execution (Metasp | multiple/remote/9913.rb
Eric Allman Sendmail 8.8.x - Socket Hijack                              | linux/local/19602.c
Eric Allman Sendmail 8.9.1/8.9.3 - ETRN Denial of Service               | linux/dos/19701.sh
Indexu 5.0/5.3 - 'Sendmail.php' Multiple Cross-Site Scripting Vulnerabi | php/webapps/29481.txt
Linux Kernel 2.0 Sendmail - Denial of Service                           | linux/dos/19282.c
Linux Kernel 2.2.x 2.4.0-test1 (SGI ProPack 1.2/1.3) - Sendmail 8.10.1  | linux/local/20001.sh
Linux Kernel 2.2.x 2.4.0-test1 (SGI ProPack 1.2/1.3) - Sendmail Capabil | linux/local/20000.c
Metainfo Sendmail 2.0/2.5 / MetaIP 3.1 - Upload / Execute Read Scripts  | multiple/remote/19084.txt
Morris Worm - sendmail Debug Mode Shell Escape (Metasploit)             | unix/remote/45789.rb
ObieWebsite Mini Web Shop 2 - 'Sendmail.php?PATH_INFO' Cross-Site Scrip | php/webapps/29957.txt
PHP 4.x/5.0/5.1 with Sendmail Mail Function - 'additional_param' Arbitr | php/local/27334.txt
PHPMailer < 5.2.19 - Sendmail Argument Injection (Metasploit)           | multiple/webapps/41688.rb
Sendmail 8.11.6 - Address Prescan Memory Corruption                     | unix/local/22442.c
Sendmail 8.11.x (Linux/i386) - Local Privilege Escalation               | linux/local/411.c
Sendmail 8.11/8.12 Debugger - Arbitrary Code Execution (1)              | linux/local/21060.c
Sendmail 8.11/8.12 Debugger - Arbitrary Code Execution (2)              | linux/local/21061.c
Sendmail 8.11/8.12 Debugger - Arbitrary Code Execution (3)              | linux/local/21062.txt
Sendmail 8.11/8.12 Debugger - Arbitrary Code Execution (4)              | linux/local/21063.txt
Sendmail 8.12.6 - Compromised Source Backdoor                           | unix/remote/21919.sh
Sendmail 8.12.8 (BSD) - 'Prescan()' Remote Command Execution            | linux/remote/24.c
Sendmail 8.12.9 - 'Prescan()' Variant Remote Buffer Overrun             | linux/remote/23154.c
Sendmail 8.12.x - 'X-header' Remote Heap Buffer Overflow (PoC)          | linux/dos/32995.txt
Sendmail 8.12.x - Header Processing Buffer Overflow (1)                 | unix/remote/22313.c
Sendmail 8.12.x - Header Processing Buffer Overflow (2)                 | unix/remote/22314.c
Sendmail 8.12.x - SMRSH Double Pipe Access Validation                   | unix/local/21884.txt
Sendmail 8.13.5 - Remote Signal Handling (PoC)                          | linux/dos/2051.py
Sendmail 8.6.9 IDENT - Remote Command Execution                         | unix/remote/20599.sh
Sendmail 8.9.2 - Headers Prescan Denial of Service                      | irix/dos/23167.c
Sendmail 8.9.x/8.10.x/8.11.x/8.12.x - File Locking Denial of Service (1 | linux/dos/21476.c
Sendmail 8.9.x/8.10.x/8.11.x/8.12.x - File Locking Denial of Service (2 | linux/dos/21477.c
Sendmail with clamav-milter < 0.91.2 - Remote Command Execution         | multiple/remote/4761.pl
WEBgais 1.0 - websendmail Remote Command Execution                      | cgi/remote/20483.txt
------------------------------------------------------------------------ ---------------------------------
Shellcodes: No Results

```


## Non-root access


## Root access


