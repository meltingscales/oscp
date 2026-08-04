# OSCP Readiness — Verdict (2026-06-23)

**Status: Not ready. ~3-4 weeks more needed.**

## Stats
- 24 pwned, 5 stuck (Cobweb, Hokkaido, Jacko, MedJed, Roquefort), 1 in-progress (Hepet)

## Critical Gaps

1. **AD independence** — Hokkaido required walkthrough + AI at every step. Exam AD chain = 40pts, no AI allowed. Biggest risk.
2. **Stuck boxes** — 17% stuck rate across multiple categories suggests methodology gaps.
3. **AI dependency** — must own the full AD attack chain mentally: enumerate → MSSQL impersonate → BloodHound → targetedKerberoast → ForceChangePassword → WSUS/RBCD.

## Strengths
- Solid enumeration habits
- Good Windows privesc toolchain (GodPotato, SeImpersonatePrivilege)
- Impacket / netexec / BloodHound familiarity
- Decent breadth (24 boxes)

## Before Booking Exam

- [ ] Redo Hokkaido from scratch — no guide, no AI, target < 4 hrs
- [ ] Understand what you missed on Jacko, Cobweb, MedJed (don't skip)
- [ ] Complete 2-3 more AD boxes (Vault, Heist, Hutch on PG)

## PG Practice AD Box Pool (pick 2-3 beyond Vault/Heist/Hutch)
- Access — intermediate, AD-like, good next step after Hutch
- Resourced — intermediate, resourced.local domain
- Nagoya — hard
- Nara — Windows DC, Kerberos/LDAP/DNS enum focus
- [ ] Full exam sim: 48hr timer, no AI, write report as you go

## Post-ADChain_01 — gap analysis (2026-07-15)

ADChain_01 covered: BloodHound collection/analysis, SMB/RDP/WinRM password spray, remote SAM dump (reg save + secretsdump), LSA/DCC2 (mscache2) hash dump + crack, lateral via local acct reuse, NTDS dump + PtH to DA.

Not yet touched, hit these next:
- **Kerberoasting** (SPN → TGS → crack) — box: `Forest` (HTB), `Support` (HTB), or `Cascade` (PG)
- **AS-REP Roasting** (no-preauth accounts) — box: `Sauna` (HTB) — good, does Kerberoast+ASREP+gMSA in one
- **ACL abuse** (GenericAll/WriteDACL/ForceChangePassword/AddMember via BloodHound edges) — box: `Resolute` (HTB), `Cascade` (PG)
- **Constrained/Unconstrained delegation + RBCD** — box: `Manager` (HTB), or PG `Access` (does have delegation angle)
- **DCSync abuse** (mimikatz/secretsdump `-just-dc` w/ replication rights, not just local admin) — box: `Reel` or `Sizzle` (HTB)
- **GPO abuse / SharpGPOAbuse** — box: `Sizzle` (HTB) or `Zephyr` (HTB, harder)
- **Certificate services (ESC1/ESC8 AD CS)** — not covered anywhere yet, exam-relevant — box: `Certified` (HTB), `Escape` (HTB)

Priority order given exam scope: Kerberoast/ASREP (Sauna) ✅ → ACL abuse (Resolute) ✅ → DCSync (Sizzle) ← in progress → Reel (DCSync, later) → delegation/RBCD (Manager) → AD CS (Certified) if time allows.

## Scoring Math
- AD chain (40pts) + 2 standalones (40pts) = 80 → pass
- If AD fails, need 3.5 standalones (70pts) → harder path
