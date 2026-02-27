# Internal

## Recon

I ran a script scan with `sudo nmap -sVC 192.168.55.40 --script vuln` against the target to enumerate it.

The victim seemed to be running Windows Server 2008 R2.

This script let me know that this victim is vulnerable to CVE-2017-0143.

![](./nmap.png)

## Vulnerability

I searched `msfconsole` for a payload that matched CVE-2017-0143.

A few came up.

I used the msfconsole module called `TODO`.


## Recommendations

Upgrade to Windows 11 or higher.
