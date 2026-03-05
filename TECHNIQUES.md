(i can program)

## recon

- nmap -sS -sV $TARGET

## brute-force

- ffuf
- /usr/share/wordlists/seclists/Passwords/Default-Credentials/default-passwords.txt
## reverse shell

- /usr/share/webshells

## smb

- smbclient
- crackmapexec
  - netexec

## shell stabilization

python3 -c "import pty; pty.spawn('/bin/bash');"
