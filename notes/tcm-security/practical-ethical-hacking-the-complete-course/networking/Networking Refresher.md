
lmao i am skipping ALL of this, we r good on networking :)

![](udp-joke-meme.png)

..........WOW!!!! packets. ports. wowie!!


## common ports and protocols

...just since I don't memorize all of these,

- tcp
	- 21/ftp
	- 22/ssh
	- 23/telnet
	- 53/dns
	- 80/http
	- 443/https
	- 110/pop3
	- 139+445/smb
	- 143/imap
- udp
	- 53/dns
	- 67,68/dhcp
	- 69/tftp
	- 161/snmp

smtp, pop3, imap are all mail related (mailpup...good album)

dns is...yeeee haw!!! 🤠
(literally just turns a domain into IP)

SMB is a...tasty tasty source of vulnerabilities. binary protocol that windows uses to be extremely vulnerable. yum!!!!!!
"Samba" "Server Message Block"


## OSI Model

layer cake!!!
https://ahicha.bandcamp.com/album/sugar-sweet-symphony


PDNTSPA
Please Do Not Throw Sausage Pizza Away
1 Physical - copper
2 Data - switching+MAC
3 Network - IP+routing
4 Transport - TCP/UDP
5 Session - session mgmt (idk lol)
6 Presentation - WMV, JPEG, MOV
7 Application - HTTP, SMTP, FTP, SSH

or, diagnostic stack/six sigma/whatever:

1. "Is the cable plugged in?"
2. Is the blinking light on the back green?
3. What's your IP?
4. Are packets being received?
5. ???
6. Profit?
7. Are there error logs????


## subnetting :)

```
~/Git/dotfiles master  
❯ ip a show enp10s0  
3: enp10s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000  
   link/ether [[MAC]] brd ff:ff:ff:ff:ff:ff  
   altname enx22274d05238c  
   inet 192.168.0.[[REDACTED]]/24 brd 192.168.0.255 scope global dynamic noprefixroute enp10s0  
      valid_lft 5857sec preferred_lft 5857sec  
   inet6 [[REDACTED]]/64 scope link noprefixroute    
      valid_lft forever preferred_lft forever
```

my desktop's wireless card.

`192.168.0.x/24` is the subnet in CIDR notation.
we can derive a "netmask" from it.

```py
from ipaddress import IPv4Network

def cidr_to_netmask(cidr):
    network = IPv4Network(cidr)
    return str(network.netmask)
```

```bash
~/Git/oscp/notes/tcm-security/practical-ethical-hacking-the-complete-course/networking main*
❯ python cidrToNetmask.py
255.255.255.0

```

