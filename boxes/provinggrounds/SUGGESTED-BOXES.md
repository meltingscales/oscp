# Suggested Boxes

## Finish What You've Started First

**Interface** — Very close. Found `/api/users`, have a user list, know it's a password-spray problem.
Try spraying `admin` as the password against all users — creds are typically trivially simple on these boxes.

**Hepet** — Full walkthrough in notes but no progress logged. Windows box: LibreOffice macro → Veyon Service binary replacement.

**Hokkaido** — RDP as `molly.smith`, member of WSUS Administrators. SharpWSUS blocked by Defender.
Try WSUS abuse via PowerShell API directly (no binary needed), or investigate `Server Operators` group angle.

---

## New Boxes

| Box | OS | Why |
|-----|-----|-----|
| **ClamAV** | Linux | Classic buffer overflow in ClamAV milter — good BOF practice |
| **Bratarina** | Linux | SMTP exploit, quick and clean win |
| **Hetemit** | Linux | Python-based service exploit, good enumeration practice |
| **Kevin** | Windows | Beginner-friendly, HP Power Manager exploit — builds Windows confidence |
| **Access** | AD/Windows | Classic OSCP box — telnet + .mdb credential harvesting + runas |
| **Nibbles** | Linux | NibbleBlog RCE, good web app exploitation practice |

## Priority Order

1. Interface (20 min, basically there)
2. Hepet (have the notes, just execute)
3. Bratarina / Kevin (quick wins to keep momentum)
4. Access (AD practice without Hokkaido's complexity)
5. ClamAV (if you want BOF practice)
