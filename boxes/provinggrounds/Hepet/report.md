# Report - Hepet

- Author: Henry Post
- Target: Hepet
- Target IP: 192.168.54.140
- Date: 04/28/2026

## Executive Summary



### Recommendations


## Resources


## Recon

I ran an nmap scan that enumerated their ports:

    nmap -sS -sV hepet


| port     | service      | notes |
| -------- | ------------ | ----- |
| 25/tcp   | smtp         |       |
| 79/tcp   | finger       |       |
| 106/tcp  | pop3pw       |       |
| 110/tcp  | pop3         |       |
| 135/tcp  | msrpc        |       |
| 139/tcp  | netbios-ssn  |       |
| 143/tcp  | imap         |       |
| 443/tcp  | https        |       |
| 445/tcp  | microsoft-ds |       |
| 8000/tcp | http         |       |
Let's try https://hepet.

A website shows up.

```txt
The Team

Meet us at our HQ
Paris

Ela Arwel

System Administrator
New York

Charlotte D.

Security & Pentester
San Francisco

Magnus U.

Designer
Paris

Agnes T.

Public Relations
New York

Jonas K.

SicMundusCreatusEst
San Francisco

Martha U.

Writter

```

I feel like `JonasK:SicMundusCreatusEst` might be a cred.

But I'm not sure how to login to SMTP.

```sh
echo 'SicMundusCreatusEst' > passwords.txt
hydra -l jonask -P passwords.txt hepet smtp -V
```

Before I use `cewl`, let's use gobuster. Don't want to go down a rabbit hole.

```sh
gobuster dir -k -u https://hepet -w /usr/share/wordlists/dirb/common.txt
```

https://hepet/team/ is the only result. Just JPGs.


```sh
cewl --lowercase https://hepet | grep -v CeWL > wordlists.txt

hydra -l jonask -P wordlists.txt hepet smtp -V # nope
hydra -l JonasK -P wordlists.txt hepet smtp -V # nope
```

What if we need to attack a different service?

Asking `z.ai`....
https://chat.z.ai/s/7468ec2e-ab05-4bfb-985a-5fd6fb0da286

Okay. Let's try `exiftool` on all the jpgs.

```sh

wget --no-check-certificate https://hepet/team/agnes.jpeg
wget --no-check-certificate https://hepet/team/charlotte.jpeg
wget --no-check-certificate https://hepet/team/ela_arwel.jpeg
wget --no-check-certificate https://hepet/team/jonas.jpeg
wget --no-check-certificate https://hepet/team/magnus.jpeg
wget --no-check-certificate https://hepet/team/martha.jpeg

exiftool *.jpeg
# not too interesting...

strings jonas.jpeg
```

I think this is a waste of time.

https://banua.medium.com/proving-grounds-hepet-oscp-prep-2025-practice-17-3bdc3ad86495

Okay. This writeup seems to help me out. I will return to this after temple.

Try firstname only for creds, then try `telnet hepet 143`.

```
agnes
charlotte
ela
jonas
magnus
martha
```


## Non-root access



## Root access




