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
- [ ] Full exam sim: 48hr timer, no AI, write report as you go

## Scoring Math
- AD chain (40pts) + 2 standalones (40pts) = 80 → pass
- If AD fails, need 3.5 standalones (70pts) → harder path
