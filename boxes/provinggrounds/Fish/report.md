# Report - Fish

Author: Henry Post
Target: Fish
Target IP: 192.168.56.168
Date: 03/14/2026

## Executive Summary

This machine, `Fish`, was enumerated by nmap to have `rdp` port `3389` and GlassFish ports `8080,4848` open.

GlassFish was vulnerable to `CVE-2017-1000028`, a directory traversal vulnerability. This was exploited to gain RDP credentials from SynaMan.

The RDP credentials were used to login as `arthur`, and the user flag was taken.

From there, a reverse shell listener was created on the attacker, a malicious DLL was sent to the victim, and `CVE-2019-18194`, a DLL loading vulnerability involving TotalAV, was exploited to get SYSTEM access and take the root flag.

## Recommendations

Do not expose unnecessary services.

Update GlassFish to the latest patched version.

Update TotalAV to the latest non-vulnerable version.

## Recon

An `nmap` scan shows a few open ports - RDP and GlassFish.

    nmap -sS -sV 192.168.56.168

![](Pasted%20image%2020260314204439.png)

## Non-root access

I searched through `exploit-db.com` for an exploit targeting GlassFish, and found one - CVE-2017-1000028. There was also a related Metasploit module.

![](Pasted%20image%2020260314210129.png)

	search CVE-2017-1000028
	use 0

![](Pasted%20image%2020260314210249.png)

I do some googling, and find out that SynaMan stores its credentials file at `C:\SynaMan\config\AppConfig.xml`.

We need to set these options:

- `set FILEPATH /SynaMan/config/AppConfig.xml`
- `set RHOSTS 192.168.56.168`
- `set RPORT 4848`

![](Pasted%20image%2020260314232652.png)

We steal a credential from that file - `arthur:KingOfAtlantis`.

![](Pasted%20image%2020260314233138.png)

We then use `rdesktop` and get RDP access.

    rdesktop -u arthur -p KingOfAtlantis 192.168.56.168:3389


![](Pasted%20image%2020260314233756.png)

We got the user flag.

## SYSTEM access