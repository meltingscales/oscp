# Suggested Boxes

## Finish What You've Started First

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

1. Hepet (have the notes, just execute)
2. Bratarina / Kevin (quick wins to keep momentum)
3. Access (AD practice without Hokkaido's complexity)
4. ClamAV (if you want BOF practice)
