## Recon

I ran a script scan with `sudo nmap -sVC $TARGET --script vuln` against the target to enumerate it.

![](Pasted%20image%2020260301120720.png)

CVE-2009-3103 shows up. Let's search msfconsole.

## Exploit

The first exploit, `windows/smb/ms09_050_smb2_negotiate_func_index`, is the one we will use.

![](Pasted%20image%2020260301140801.png)

It is possible due to the nature of heap corruption exploits, that this exploit is non-deterministic. It may take multiple tries to pop a shell.

I am switching to the in-browser Kali from `portal.offsec.com`.

![](Pasted%20image%2020260301142353.png)

It works! The exploit required running from within the OffSec-provided Kali instance, as it has the correct VPN routing to the victim.

Useful commands:
- getuid
- pwd
- localtime

I will now steal the flag.

![](Pasted%20image%2020260301143144.png)

## Recommendations

Update Windows immediately to Windows 11 or higher. Do not use outdated services. It is highly likely that other vulnerabilities exist that could lead to full system compromise.