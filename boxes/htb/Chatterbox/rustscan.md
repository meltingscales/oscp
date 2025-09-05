                                                                                                                                        
┌──(root㉿kali)-[/home/kali/Downloads]
└─# rustscan -a $ip
.----. .-. .-. .----..---.  .----. .---.   .--.  .-. .-.
| {}  }| { } |{ {__ {_   _}{ {__  /  ___} / {} \ |  `| |
| .-. \| {_} |.-._} } | |  .-._} }\     }/  /\  \| |\  |
`-' `-'`-----'`----'  `-'  `----'  `---' `-'  `-'`-' `-'
The Modern Day Port Scanner.
________________________________________
: http://discord.skerritt.blog         :
: https://github.com/RustScan/RustScan :
 --------------------------------------
Open ports, closed hearts.

[~] The config file is expected to be at "/root/.rustscan.toml"
[!] File limit is lower than default batch size. Consider upping with --ulimit. May cause harm to sensitive servers
[!] Your file limit is very small, which negatively impacts RustScan's speed. Use the Docker image, or up the Ulimit with '--ulimit 5000'. 
Open 10.10.10.74:135
Open 10.10.10.74:139
Open 10.10.10.74:445
Open 10.10.10.74:9255
Open 10.10.10.74:9256
Open 10.10.10.74:49152
Open 10.10.10.74:49153
Open 10.10.10.74:49155
Open 10.10.10.74:49154
Open 10.10.10.74:49156
Open 10.10.10.74:49157
[~] Starting Script(s)
[~] Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-05 15:31 EDT
Initiating Ping Scan at 15:31
Scanning 10.10.10.74 [4 ports]
Completed Ping Scan at 15:31, 0.12s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 15:31
Completed Parallel DNS resolution of 1 host. at 15:31, 0.00s elapsed
DNS resolution of 1 IPs took 0.00s. Mode: Async [#: 1, OK: 0, NX: 1, DR: 0, SF: 0, TR: 1, CN: 0]
Initiating SYN Stealth Scan at 15:31
Scanning 10.10.10.74 [11 ports]
Discovered open port 139/tcp on 10.10.10.74
Discovered open port 445/tcp on 10.10.10.74
Discovered open port 135/tcp on 10.10.10.74
Discovered open port 49155/tcp on 10.10.10.74
Discovered open port 49153/tcp on 10.10.10.74
Discovered open port 49152/tcp on 10.10.10.74
Discovered open port 49156/tcp on 10.10.10.74
Discovered open port 49157/tcp on 10.10.10.74
Discovered open port 49154/tcp on 10.10.10.74
Discovered open port 9255/tcp on 10.10.10.74
Discovered open port 9256/tcp on 10.10.10.74
Completed SYN Stealth Scan at 15:31, 0.22s elapsed (11 total ports)
Nmap scan report for 10.10.10.74
Host is up, received echo-reply ttl 127 (0.095s latency).
Scanned at 2025-09-05 15:31:33 EDT for 0s

PORT      STATE SERVICE      REASON
135/tcp   open  msrpc        syn-ack ttl 127
139/tcp   open  netbios-ssn  syn-ack ttl 127
445/tcp   open  microsoft-ds syn-ack ttl 127
9255/tcp  open  mon          syn-ack ttl 127
9256/tcp  open  unknown      syn-ack ttl 127
49152/tcp open  unknown      syn-ack ttl 127
49153/tcp open  unknown      syn-ack ttl 127
49154/tcp open  unknown      syn-ack ttl 127
49155/tcp open  unknown      syn-ack ttl 127
49156/tcp open  unknown      syn-ack ttl 127
49157/tcp open  unknown      syn-ack ttl 127

Read data files from: /usr/share/nmap
Nmap done: 1 IP address (1 host up) scanned in 0.51 seconds
           Raw packets sent: 15 (636B) | Rcvd: 44 (1.792KB)

                                                                                                                                        
┌──(root㉿kali)-[/home/kali/Downloads]
└─# 
