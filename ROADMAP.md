# Lynkeus Initiative — Roadmap

---

## What We Have Built

### Core
| File | What it does |
|------|-------------|
| `main.py` | Interactive CLI menu — run this to access everything |
| `core/scanner.py` | Concurrent TCP port scanner using thread pools |
| `core/probe.py` | TCP connection probe and service banner grabber |

### Utilities
| File | What it does |
|------|-------------|
| `utils/resolver.py` | Resolves hostnames to IP addresses |
| `utils/ports.py` | Parses port arguments into lists (80, 1-1024, 22,80,443) |
| `utils/port_names.py` | Maps port numbers to service names |

### Output
| File | What it does |
|------|-------------|
| `output/colors.py` | ANSI colour constants used across all modules |
| `output/display.py` | All terminal print functions — ASCII banner, results, summary |

### Reports
| File | What it does |
|------|-------------|
| `reports/json_report.py` | Saves scan results to a structured JSON file |

### Credential Attacks
| File | What it does |
|------|-------------|
| `modules/credentials/ssh_brute.py` | SSH brute forcer with threading, delay, stealth mode |
| `modules/credentials/ftp_brute.py` | FTP brute forcer with anonymous login check |
| `modules/credentials/http_brute.py` | HTTP basic auth brute forcer |

### Network Attacks
| File | What it does |
|------|-------------|
| `modules/network/arp_scan.py` | ARP scanner — finds every live host and MAC on the subnet |
| `modules/network/dns_spoof.py` | DNS spoofer — redirects DNS queries to a controlled IP |
| `modules/network/packet_craft.py` | Raw packet crafter — SYN, ICMP, UDP via Scapy |

### Stealth
| File | What it does |
|------|-------------|
| `modules/stealth/stealth_scan.py` | Port scanner with randomised order and jittered timing |
| `modules/stealth/user_agent.py` | HTTP user agent rotator — 10 real browser identities |
| `modules/stealth/ttl_spoof.py` | TTL manipulator — impersonate different OS fingerprints |

### Documentation
| File | What it covers |
|------|---------------|
| `docs/01_port_scanning.md` | What port scanning is and how it works |
| `docs/02_banner_grabbing.md` | What banners are and what they reveal |
| `docs/03_brute_forcing.md` | How brute forcing works and why wordlists matter |
| `docs/04_arp_scanning.md` | ARP protocol, host discovery, MAC vendor lookup |
| `docs/05_dns_spoofing.md` | How DNS spoofing works and how to detect it |
| `docs/06_packet_crafting.md` | Raw packet construction, Scapy, TCP/ICMP/UDP |
| `docs/07_stealth_scanning.md` | How IDS detects scans and how to evade detection |
| `docs/08_ttl_spoofing.md` | TTL values, OS fingerprinting, how spoofing works |
| `docs/09_user_agent_rotation.md` | HTTP headers, WAF evasion, bot detection |

---

## What to Build Next

### Short Term

**Reverse Shell Generator**
Generate one-liner reverse shells in Python, Bash, and PHP that connect back to your machine.
Teaches you exactly how malware establishes access and how defenders detect outbound connections.
```
modules/post/reverse_shell.py
```

**CSV Report Exporter**
Add a second report format alongside JSON — a clean CSV you can open in Excel or import into a SIEM directly.
```
reports/csv_report.py
```

**Subdomain Enumerator**
Given a domain, brute force subdomains using a wordlist and DNS queries. Classic OSINT recon step before any web application test.
```
modules/recon/subdomain_enum.py
```

**HTTP Directory Brute Forcer**
Given a URL, probe paths from a wordlist to find hidden admin panels, login pages, and exposed files.
```
modules/recon/dir_brute.py
```

---

### Medium tTrm — Grow the Framework

**CVE Lookup Integration**
After a port scan, cross-reference open ports and banner versions against the NVD (National Vulnerability Database) API. Show known CVEs for each detected service automatically.
```
modules/intel/cve_lookup.py
```

**WHOIS + Geolocation**
Given a target IP or domain, pull WHOIS registration data and geolocate the IP (country, city, ASN, ISP).
```
modules/recon/whois_lookup.py
```

**SSH Key Checker**
Instead of brute forcing passwords, test whether the target SSH server accepts commonly leaked private keys from public breach databases.
```
modules/credentials/ssh_key_check.py
```

**Privilege Escalation Suggester**
Scan a Linux target for common misconfiguration — SUID binaries, writable cron jobs, sudo rules, world-writable paths — and suggest escalation routes.
```
modules/post/privesc_check.py
```

**HTML Report Generator**
Generate a styled, readable HTML pentest report from scan results. Include open ports, banners, discovered hosts, and credential findings in one document.
```
reports/html_report.py
```

---

*The mission is never complete. Lynkeus never stops looking.*
