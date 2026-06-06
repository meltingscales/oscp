# Report - Interface

- Author: Henry Post
- Target: Interface
- Target IP: 192.168.52.106
- Attacker IP: 192.168.49.52
- Date: 06/06/2026

## Executive Summary


### Recommendations


## Resources



## Recon

```sh
sudo nano /etc/hosts

nmap -sS -sV -p- interface

<<EOF
Starting Nmap 7.98 ( https://nmap.org ) at 2026-06-06 20:05 +0000
Nmap scan report for interface (192.168.52.106)
Host is up (0.00039s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
80/tcp open  http    Node.js Express framework
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.21 seconds
EOF
```

Port 22 and 80.

On port 80, there's a login screen.

![](Pasted%20image%2020260606150746.png)

When we inspect the POST request, it's formatted like this:

http://interface/login
payload `{"username":"xxx","password":"xxx"}` as JSON POST body.

We also notice that there's `/api/users`.

```sh
wget http://interface/api/users
mv users users.json

jq -r '.[]' users.json > users.txt
```

Now, how should we brute-force this?

A failed login to `/login` gives 401 Unauthorized.

Let's try our own custom fuzzer...

```sh
sudo gunzip /usr/share/wordlists/rockyou.txt.gz

wget https://raw.githubusercontent.com/meltingscales/oscp/refs/heads/main/boxes/provinggrounds/Interface/brute.py

head -n 1000 /usr/share/wordlists/rockyou.txt > rockyou1000.txt

python brute.py --passwords rockyou1000.txt
```


## Non-root access




## Root access

