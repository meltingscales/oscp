# Windows Pentesting Assessment - February 2026

## Your Gaps

**What you've demonstrated:**
- Basic SMB enumeration (`smbclient`, `smbmap`, `nxc`)
- GPP password decryption (`gpp-decrypt`)
- Basic Kerberoasting (on Active)
- Webshells and reverse shells

**What's missing from your notes:**
- BloodHound/SharpHound (AD visualization - this is massive for OSCP)
- Token impersonation attacks (you mention SeImpersonate but haven't done it)
- Windows service exploitation (unquoted paths, weak permissions)
- Any real pivoting practice

---

## Priority Focus List

### 1. Finish these boxes ASAP (in order)
From tjnull's list, prioritize:

| Box                   | Why                                                 |
| --------------------- | --------------------------------------------------- |
| **Forest** [FAIL/OLD] | AS-REP Roasting + DCSync - fundamental AD attacks   |
| **Sauna**             | Similar to Forest, reinforces the pattern           |
| **Bastion**           | VHD mount + SAM dump - common Windows foothold      |
| **Devel**             | Classic IIS + SeImpersonate (do the potato privesc) |
| **Jeeves**            | Jenkins exploitation + JuicyPotato                  |

### 2. Skills to drill before exam

**Token Impersonation (you will see this):**
```
whoami /priv
# If you see SeImpersonatePrivilege or SeAssignPrimaryTokenPrivilege:
# → PrintSpoofer, GodPotato, JuicyPotato, RoguePotato
```

**BloodHound (learn this NOW):**
```powershell
# On victim
.\SharpHound.exe -c All
# On Kali
bloodhound &
# Upload .zip, look for "Shortest Path to Domain Admin"
```

**impacket suite (memorize these):**
```bash
impacket-GetNPUsers domain.local/ -usersfile users.txt -no-pass  # AS-REP Roast
impacket-GetUserSPNs domain.local/user:pass -request              # Kerberoast
impacket-secretsdump domain.local/user:pass@DC_IP                 # Dump hashes
impacket-psexec domain.local/admin:pass@TARGET                    # Shell
impacket-wmiexec domain.local/admin@TARGET -hashes LMHASH:NTHASH  # PTH
```

### 3. Your TECHNIQUES.md is empty - fix that

You need checklists for:
- Windows initial enumeration
- Windows privesc (WinPEAS output → what to check)
- AD attack paths
- File transfer methods (certutil, powershell, smb, etc.)

---

## Blunt Assessment

Your Active notes show you needed heavy AI assistance for basic steps. That's fine for learning, but you need to internalize the pattern so you can do it blind:

1. Enumerate → find GPP creds / null sessions / Kerberos users
2. Spray creds → get domain user
3. BloodHound → find path to DA
4. Execute attack chain (Kerberoast/AS-REP/DCSync)

Your note to yourself is correct: **practice Medium boxes blind, cheat on 2-3 first to learn the pattern, then do them without guides.**

Do Forest and Sauna this week. They'll cement the AD methodology you started on Active.

---

## Homework Checklist

- [ ] Complete **Forest** (HTB Easy) - focus on AS-REP Roasting
- [ ] Complete **Sauna** (HTB Easy) - reinforce AD patterns
- [ ] Complete **Bastion** (HTB Easy) - VHD/SAM extraction
- [ ] Complete **Devel** (HTB Easy) - IIS + SeImpersonate potato
- [ ] Complete **Jeeves** (HTB Medium) - Jenkins + JuicyPotato
- [ ] Install and learn **BloodHound** - run against GOAD lab
- [ ] Fill out **TECHNIQUES.md** with Windows enumeration checklist
- [ ] Practice **impacket** commands until muscle memory
- [ ] Do one box completely blind (no hints, no AI) - time yourself
