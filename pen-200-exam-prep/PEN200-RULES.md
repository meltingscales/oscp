# OSCP / PEN-200 Exam Rules — Quick Reference

The OSCP is deliberately an **open-book** exam. OffSec encourages using Google,
your notes, and other tools; the proctor won't disqualify you for that. The
hard lines are automated tooling and getting help from other people.

> Policies get revised. Confirm against the official OSCP Exam Guide at
> help.offsec.com before your exam date.

---

## Reference material — allowed

- Cheat sheets and GitHub repos (PayloadsAllTheThings, HackTricks, etc.)
- Printed reports / write-ups of previously-pwned boxes
- Your own notes (Obsidian, CherryTree, OneNote, etc.)
- Google / general web searching

**Caveat:** Exam machines are *not* reused public HTB/PG boxes. Old write-ups
are useful for methodology and payload reference, not as answer keys.

**Hard line — no human help:** You may use Discord to *search* for information,
but you may never seek or receive assistance from another person. Reading a
public write-up is fine; asking someone "how do I root box 2" is an instant fail.

---

## Environment

- **Kali VM** is the expected setup — bring your own attacking machine and
  connect over OffSec's VPN.
- Load all tools and notes into the VM *before* exam day; don't rely on
  internet-dependent workflows.

---

## Tool restrictions

### Allowed freely
Nmap (+ NSE), Nikto, Burp Free/Community, DirBuster, gobuster, hydra,
LinPEAS / WinPEAS, netcat, custom Python/Bash scripts, and similar
non-automated tools against any target.

### Metasploit — restricted, not banned
- Usable on **one target machine only** (auxiliary, exploit, and post modules,
  or the Meterpreter payload).
- Once used on a machine, it is **locked to that machine**.
- **Cannot be used for pivoting** (that would touch a second target).

### Prohibited entirely
- Mass vulnerability scanners: Nessus, OpenVAS, Nexpose
- Automated exploitation tools: SQLmap, db_autopwn, browser_autopwn
  - *Gotcha:* SQLmap is allowed on some other OffSec exams, but **not** OSCP.
- Commercial tools: Burp Pro, Metasploit Pro
- Any tool performing similar automated functions — you're responsible for
  knowing what your tools do under the hood.
- **AI / LLMs / chatbots** — banned the entire time, **including the reporting
  phase**. A static cheat sheet you wrote beforehand is fine; querying a
  chatbot live is not.

---

## Breaks

The exam is ~24 hours — take breaks, eat, sleep, caffeinate.

- Inform your proctor via the proctoring chat before you leave and when you
  return (no need to wait for acknowledgment).
- Leave the proctoring session active while on break; the VPN stays connected
  so you can leave processes running.
- Use the "pause webcam" option for longer breaks.
- The proctor is a silent **visual-only** observer (no audio) — eat and drink
  freely.

---

## Two things to memorize cold

1. **Metasploit one-machine rule** (and it locks to that machine).
2. **Proof-file contents must be shown in a shell with `cat` from their
   original location** — obtaining them any other way = zero points for that
   machine.
