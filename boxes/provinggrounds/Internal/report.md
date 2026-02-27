# Internal

## Recon

I ran a script scan with `sudo nmap -sVC 192.168.55.40 --script vuln` against the target to enumerate it.

The victim seemed to be running Windows Server 2008 R2.

This script let me know that this victim is vulnerable to CVE-XXX.

![](./nmap.png)

## Vulnerability

I searched `msfconsole` for a payload that matched CVE-XXX.

A few came up.

I used the msfconsole module called `windows/smb/ms09_050_smb2_negotiate_func_index`.


## Recommendations

Upgrade to Windows 11 or higher.
