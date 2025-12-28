
## 1a. passive recon

- sat imgs
- drone recon
- building layout (gmaps, OGNSS, GLONASS, etc)

job info
- employee name
- job title
- phone #
- pictures
- badge photos
- desk photos
- computer photos

### web/host

target validation: 
- whois
- nslookup
- dnsrecon

subdomains
- googe-fu
- dig
- nmap
- sublist3r
- bluto
- crt.sh
- etc

fingerprinting
- nmap
- wappalyzer
- whatweb
- builtwith
- netcat/nc

data breaches
- ddosecrets
- HIBP
- breach-parse
- weleakinfo
- .onion etc
- i2p
- breachforums



## identifying our target.
(literally read bug bounty.)


## discovering email addresses
hunter.io
yeeeeeep......

domain search "tesla.com"

phonebook.cz

intelx.io

data is inherently useful
the messiness of humans means you can usually link data together to infer more valuable data (duh)

voilanorbert.com

connect.clearbit.com

tools.verifyemailaddress.io

email-checker.net

- you should abuse google "recover account" because it leaks emails


## breach-parse

./breach-parse.sh (kali)

github.com/hmaverickadams

(just a magnet download then sifts through data. p simple) nuff said
lmao this is so basic
just write your own in rust + claude
takes like. <4 minutes
why am i even watching this video


## deHashed - hunting breached credentials

lmao again, perhaps rent 4x gpu cluster, hashcat? orrr, thats only if u need to crack hash.

dehashed.com
just pay for it

hashes.org
or google it


## hunting subdomains part 1

sublist3r lol

crt.sh
### 2

owasp amass
rtfm
write rust software to validate or mass scan :3
distribute across vpns (hijack cloudflare, see old github) or just use swarm of aws ec2s/etc/botnet

## identifying website technologies

- builtwith.com
wappalyzer
whatweb

    whatweb <URL>

## burp suite

...gonna skip it, i think im good enuff

literally just capture requests and read text documents/fields, and read the folder structure and dig thru files to find hidden domains or internal server headers,

also fuzz endpoints/parameters
"dashboard" useful

buy it, could be useful >:3c




## google fu

actually screw this, lets hack!!!
