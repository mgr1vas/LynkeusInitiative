# Brute Forcing

## What it is
Brute forcing is the method of systematically trying every possible combination of credentials until the correct one is found. In practice, this almost never means trying every possible character combination, it means trying passwords from a wordlist, a pre-built list of real passwords leaked from past data breaches.

## How it works
Lynkeus takes a list of usernames and a wordlist file, then attempts to authenticate to the target service with every username and password combination. The moment a valid pair is found, the attack stops and reports the result.

## The three services Lynkeus targets
**SSH (port 22)**
SSH is the primary way administrators remotely access Linux servers. A successful SSH brute force gives you a shell on the target machine — full command line access.

**FTP (port 21)**
FTP is used to transfer files. Lynkeus always checks anonymous login first (no password required) before running the wordlist. Many poorly configured servers still allow anonymous access.

**HTTP Basic Auth**
Some web pages and admin panels are protected by HTTP basic authentication — a simple username and password prompt built into the HTTP protocol. Lynkeus sends requests with base64-encoded credentials and checks whether the server responds with 200 (success) or 401 (unauthorized).

## Key concepts
- **Wordlist** — a text file with one password per line, built from real leaked passwords
- **rockyou.txt** — the most famous wordlist, containing 14 million real passwords from the 2009 RockYou breach
- **SecLists** — a GitHub repository with hundreds of wordlists for different purposes
- **Threading** — running multiple attempts simultaneously to speed up the attack
- **Delay** — a pause between attempts to avoid triggering account lockout or IDS alerts
- **Stealth mode** — hides failed attempts from terminal output to reduce noise

## Parameters explained
| Parameter | What it controls |
|-----------|-----------------|
| `threads` | How many attempts run at the same time — higher is faster but noisier |
| `delay` | Seconds to wait between attempts — higher is slower but harder to detect |
| `timeout` | How long to wait for a server response before giving up |
| `stealth` | When True, only successful logins are printed |

## Why it matters
Weak passwords are still the most common vulnerability in real environments. Brute forcing teaches you how attackers think about credential attacks and why password policies, account lockouts, and MFA exist on the defensive side.