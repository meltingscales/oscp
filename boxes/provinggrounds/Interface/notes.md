To breach this lab, you'll brute-force user credentials in a NodeJS web application to gain an initial foothold. Subsequently, you'll exploit an OS command injection vulnerability in the application to obtain a root shell. This lab enhances your skills in credential brute-forcing and exploiting command injection vulnerabilities for privilege escalation.

This lab demonstrates exploiting a NodeJS Express application by brute-forcing user credentials and leveraging an OS command injection vulnerability in the application's backup functionality. Learners will gain initial access by password-spraying valid credentials, impersonating the admin user, and exploiting the backup feature to achieve a reverse shell as root. The lab highlights web application enumeration, credential attacks, and command injection.

Learning Objectives

**After completion of this lab, learners will be able to:**

- Enumerate services to identify the NodeJS application and its endpoints.
- Extract user accounts and use a password-spraying technique to authenticate as a valid user.
- Elevate privileges by modifying JSON parameters to impersonate the admin user.
- Exploit the command injection vulnerability in the backup feature to execute arbitrary commands.
- Deploy a reverse shell payload to obtain a root shell on the target system.

		OKAY! I'm not going to use a guide. Wish me luck.

.


    nmap -sS -sV 192.168.51.106

port 22, port 80.


```
users.txt:
wendi
cole
mickey
iva
nickolas
cherie
gonzalo
olen
allen
ellen 
```

```
smallpasswords.txt:
password
admin
login
changeme
```


time to try to fuzz these.

http://192.168.51.106/login
payload `{"username":"xxx","password":"xxx"}`



```
ffuf -w /usr/share/seclists/Passwords/Common-Credentials/top-100-php-passwords.txt \
  -u http://example.com \
  -X POST \
  -d "username=admin&password=FUZZ" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -fr "incorrect"
```


```
ffuf -w names.txt:USER -w names.txt:PASS \
  -u http://192.168.51.106:80 \
  -X POST \
  -d '{"username":"USER","password":"PASS"}' \
  -H "Content-Type: application/json" \
  -fr "Unauthorized"
  
  # all fail, lets try a wordlist.
```


```
ffuf -w names.txt:USER -w /usr/share/wordlists/rockyou.txt:PASS \
  -u http://192.168.51.106:80 \
  -X POST \
  -d '{"username":"USER","password":"PASS"}' \
  -H "Content-Type: application/json" \
  -fr "Unauthorized"

# fail, took too long.
```


```
ffuf -w names.txt:USER -w /usr/share/wordlists/seclists/Passwords/Common-Credentials/darkweb2017_top-10000.txt:PASS \
  -u http://192.168.51.106:80/login \
  -X POST \
  -d '{"username":"USER","password":"PASS"}' \
  -H "Content-Type: application/json" \
  -fr "Unauthorized" \
  -fc 200

# tbd
```


OMG. I forgot to add `/login`. wow.

oh, also,
 there are loads more users! I should have started with Burp Suite.
see `/api/users`

```
jq -r '.[]' users.json > users.txt
```



```
echo "">/home/kali/Downloads/passwords.txt
echo "password">>/home/kali/Downloads/passwords.txt
echo "login">>/home/kali/Downloads/passwords.txt


ffuf -w /home/kali/Downloads/users.txt:USER -w /home/kali/Downloads/passwords.txt:PASS \
  -u http://192.168.51.106:80/login \
  -X POST \
  -d '{"username":"USER","password":"PASS"}' \
  -H "Content-Type: application/json" \
  -fr "Unauthorized" \
  -fc 200

# fail
```

```
ffuf -w /home/kali/Downloads/users.txt:USER \
  # -w /home/kali/Downloads/users.txt:PASS \
  -u http://192.168.51.106:80/login \
  -X POST \
  -d '{"username":"USER","password":"admin"}' \
  -H "Content-Type: application/json" \
  -fr "Unauthorized" \
  -fc 200

# fail
```

dang it. back from the gym. no new ideas. i will revisit this later.

"- Extract user accounts and use a password-spraying technique to authenticate as a valid user."

password spraying...as a valid user.

We must have to use the big json user list.

But what is the password? admin?

let's try something different...

`dirb`. something mentioned subdomains.

```
gobuster dns -d $TARGET -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt
```


okay. no subdomains.

next goal:

api/users
brute force with hydra and top 10 passwords.
