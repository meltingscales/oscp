# OSCP Report Improvements

## Critical Missing Items (OSCP Exam Requirements)

### 1. Proof screenshots are incomplete
The OSCP requires every proof screenshot to show **three things in the same screenshot**:
- `whoami` (showing root/SYSTEM)
- `hostname` or `ipconfig`/`ifconfig` (proving which machine)
- `cat proof.txt` / `type proof.txt`

None of the current reports explicitly capture all three. If the root-flag screenshots don't show all three, they'd be rejected.

### 2. No `local.txt` (low-priv flag)
OSCP awards partial points for getting a low-priv shell and grabbing `local.txt`. None of the reports mention capturing it. A screenshot of `local.txt` with a low-priv shell + IP is required.

### 3. Internal.pwned — no title or target IP
The report has no header, no machine name, no IP address documented anywhere. OSCP requires clearly identifying each target.

### 4. Internal.pwned — Metasploit usage undisclosed
OSCP allows Metasploit on **only one machine** per exam. The report should explicitly note this is the Metasploit machine so the grader knows it's intentional.

---

## Structural Issues

### 5. No executive summary
All three reports jump straight into technical steps. Each report should open with a 2–3 sentence summary: what the machine is, how you got in, and the impact.

### 6. CVE/vulnerability not named upfront
- **Internal**: CVE-2009-3103 is mentioned inline but not clearly called out
- **Levram**: CVE-2021-43857 is in the notes but **not in the report at all**
- **Muddy**: No CVE number cited for the XXE (should reference the Ladon exploit)

### 7. Commands not documented as text
Reports rely entirely on screenshots for commands. OSCP graders want to see the exact commands written out in the report, not just inferred from images. Add code blocks, e.g.:
```
sudo nmap -sVC 192.168.x.x --script vuln
```

### 8. Recommendations are thin
- **Internal**: "Update to Windows 11" is vague — name the specific patch (MS09-050).
- **Levram**: Missing "disable default credentials" as a systemic process recommendation.
- **Muddy**: Calls it "Guidance" instead of "Recommendations" — be consistent.

---

## Summary Table

| Issue | Internal | Levram | Muddy |
|---|---|---|---|
| Proof screenshot (whoami+IP+flag) | ? | ? | ? |
| local.txt captured | ❌ | ❌ | ❌ |
| Target IP documented | ❌ | ❌ | ❌ |
| Executive summary | ❌ | ❌ | ❌ |
| CVE named | partial | ❌ | ❌ |
| Commands as text | ❌ | ❌ | partial |
| Metasploit disclosure | ❌ | N/A | N/A |

The **Muddy** report is the strongest structurally (good section headers, multi-stage exploit chain explained well). **Internal** needs the most work.
