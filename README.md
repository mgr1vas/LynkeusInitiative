# Lynkeus
![Image](assets/lynkeus_logo.png)

> *"Οὐδὲν λανθάνει με."*
> Nothing escapes me.
 
---
 
## Eyes on Target
 
A modular offensive security framework built from scratch in Python. Every module is self-contained, every line is written by hand, and every capability is one you understand completely, not one you borrowed from a tool you cannot explain.
 
The Lynkeus Initiative is not a finished product. It is a living framework. New modules are added as skills grow. The framework grows with the operator.
 
**This is not a script kiddie toolkit. This is an initiative.**
 
> Built for home lab and educational use only. Run against machines you own.
 
---
 
## Getting Started
 
```bash
# Clone the repository
git clone https://github.com/yourname/lynkeus.git
cd lynkeus
 
# Install dependencies
pip install -r requirements.txt
 
# Launch Lynkeus
python3 main.py
```
 
That is it. Everything runs from the interactive menu — no imports, no flags to memorise, no terminal one-liners.
 
---
 
## Interactive Menu
 
When you run `python3 main.py` you are greeted with the full module menu:
 
```
  LYNKEUS INITIATIVE — MAIN MENU
 
  CORE
  [1]  Port Scanner + Banner Grabber
 
  CREDENTIALS
  [2]  SSH Brute Forcer
  [3]  FTP Brute Forcer
  [4]  HTTP Basic Auth Brute Forcer
 
  NETWORK
  [5]  ARP Scanner — Live Host Discovery
  [6]  DNS Spoofer
  [7]  Packet Crafter
 
  STEALTH
  [8]  Stealth Scanner
  [9]  TTL Spoofer
  [10] User Agent Rotator
 
  OTHER
  [11] Run All Modules
  [0]  Exit
```
 
Select a number, answer the prompts, and the module runs. No setup beyond the initial install.
 
---
 
## Modules
 
### [1] Port Scanner + Banner Grabber
Maps every open port on a target, identifies the running service, and grabs the service banner. The banner reveals software names and version numbers, turning an open port into a named, versioned target.
 
Supports single ports, ranges, and comma-separated lists. Scans run concurrently across a configurable thread pool. Results can be saved to a JSON report.
 
### [2] SSH Brute Forcer
Attempts to authenticate to an SSH service using a username list and a password wordlist. Runs attempts concurrently with configurable threading, delay between attempts, and stealth mode that hides failed attempts from output. Stops immediately when valid credentials are found.
 
### [3] FTP Brute Forcer
Attacks FTP services with credential wordlists. Always checks anonymous login first before running the wordlist — many poorly configured servers still allow anonymous access with no password.
 
### [4] HTTP Basic Auth Brute Forcer
Tests credentials against HTTP basic authentication protected pages. Sends base64-encoded credentials with each request and checks the response code. Works on both HTTP and HTTPS targets.
 
### [5] ARP Scanner
Discovers every live host on a local subnet by sending ARP broadcast requests. Reports each host's IP address, MAC address, and vendor name identified from the MAC prefix. The fastest and most reliable way to map a local network.
 
### [6] DNS Spoofer
Intercepts DNS queries on the network and returns forged responses, redirecting victims to a controlled IP address. Supports targeting specific domains, multiple domains simultaneously, or wildcard mode to intercept all DNS traffic. Requires network positioning or ARP spoofing to be in place first.
 
### [7] Packet Crafter
Builds and sends raw network packets using Scapy with full control over every field. Supports TCP SYN packets (test port state and firewall response), ICMP packets with custom payloads (test IDS detection of unusual ping traffic), and UDP packets to any port.
 
### [8] Stealth Scanner
A port scanner built to avoid IDS detection. Randomises the order ports are scanned (breaking sequential scan signatures) and adds configurable random jitter between each probe (breaking timing-based detection). Configurable thread count keeps traffic volume low.
 
### [9] TTL Spoofer
Manipulates the TTL value in outgoing packets to impersonate a different operating system. Defenders and security tools use TTL values to passively fingerprint OS types. Lynkeus can make your traffic look like Windows, Linux, macOS, Cisco, or use a fully randomised TTL per packet to make fingerprinting impossible.
 
### [10] User Agent Rotator
Cycles through a pool of real, current browser user agent strings for HTTP requests. Prevents web servers and WAFs from identifying your tool by its User-Agent header. Pool includes Chrome, Firefox, Edge, Safari, and mobile browsers across Windows, Linux, macOS, and Android.
 
---
 
## Folder Structure
 
```
LynkeusInitiative/
├── main.py                        
├── README.md
├── requirements.txt
├── testCommands.md
├── .gitignore
├── LICENSE
├── READMECommands.md
├── ROADMAP.md
├── core/
│   ├── scanner.py                 
│   └── probe.py                   
├── utils/
│   ├── resolver.py               
│   ├── ports.py                   
│   └── port_names.py              
├── output/
│   ├── colors.py                  
│   └── display.py               
├── reports/
│   └── json_report.py            
├── modules/
│   ├── credentials/
│   │   ├── ssh_brute.py           
│   │   ├── ftp_brute.py         
│   │   └── http_brute.py          
│   ├── network/
│   │   ├── arp_scan.py           
│   │   ├── dns_spoof.py           
│   │   └── packet_craft.py        
│   └── stealth/
│       ├── stealth_scan.py        
│       ├── user_agent.py          
│       └── ttl_spoof.py          
└── docs/
    ├── 01_port_scanning.md
    ├── 02_banner_grabbing.md
    ├── 03_brute_forcing.md
    ├── 04_arp_scanning.md
    ├── 05_dns_spoofing.md
    ├── 06_packet_crafting.md
    ├── 07_stealth_scanning.md
    ├── 08_ttl_spoofing.md
    └── 09_user_agent_rotation.md
```
 
---
 
## Requirements
 
```bash
# Python 3.6 or higher required
python3 --version
 
# Install all dependencies
pip install -r requirements.txt
```
 
| Library | Used by |
|---------|---------|
| `paramiko` | SSH brute forcer |
| `scapy` | ARP scanner, DNS spoofer, packet crafter, TTL spoofer |
 
The core port scanner, HTTP brute forcer, FTP brute forcer, and user agent rotator use only the Python standard library — no external dependencies.
 
---
 
## Continuous Development
 
The Lynkeus Initiative is a living framework. Every module in this project was built to be understood, not just used. If a capability exists here, the person who built it can explain every line of it.
 
Planned additions include a reverse shell generator, subdomain enumerator, HTTP directory brute forcer, CVE lookup integration, HTML report generator, and a full automated recon pipeline. See `ROADMAP.md` for the full plan.
 
*The mission is never complete. Lynkeus never stops looking.*
 
---
 
## Disclaimer
 
The Lynkeus Initiative is built for educational use in your own home lab only.
Do not use against systems you do not own or have explicit written permission to test.
