# Testing Commands

### Main Scanner - main.py
# Basic scan
`python3 main.py 192.168.1.1`

# Specific ports
`python3 main.py 192.168.1.1 -p 22,80,443,3306,3389`

# Full range with more threads
`python3 main.py 192.168.1.1 -p 1-65535 -w 200`

# Save report
`python3 main.py 192.168.1.1 -p 1-1024 -o results.json`

# Slow and careful
`python3 main.py 192.168.1.1 -p 1-1024 -t 3.0 -w 20`

# Hostname target
`python3 main.py scanme.nmap.org -p 1-1024`

---

### SSH Brute Forcer - ssh_brute.py
from modules.credentials.ssh_brute import run_ssh_brute
# Basic test
`run_ssh_brute("192.168.1.10", 22, ["admin"], "wordlist.txt", 5, 0.5, 3.0, False)`

# Multiple usernames
`run_ssh_brute("192.168.1.10", 22, ["admin", "root", "user"], "rockyou.txt", 5, 0.5, 3.0, False)`

# Stealth mode — hides failed attempts
`run_ssh_brute("192.168.1.10", 22, ["admin"], "wordlist.txt", 2, 2.0, 3.0, True)`

# Custom SSH port
`run_ssh_brute("192.168.1.10", 2222, ["admin"], "wordlist.txt", 5, 0.5, 3.0, False)`

---

### FTP Brute Forcer - ftp_brute.py
`from modules.credentials.ftp_brute import run_ftp_brute`
# Basic test — always checks anonymous first
`run_ftp_brute("192.168.1.10", 21, ["admin"], "wordlist.txt", 5, 0.5, 3.0, False)`

# Multiple usernames
`run_ftp_brute("192.168.1.10", 21, ["admin", "ftp", "user"], "rockyou.txt", 5, 0.5, 3.0, False)`

# Stealth mode
`run_ftp_brute("192.168.1.10", 21, ["admin"], "wordlist.txt", 2, 2.0, 3.0, True)`

---

HTTP Brute Forcer - http_brute.py
from modules.credentials.http_brute import run_http_brute
# Basic test
`run_http_brute("http://192.168.1.10/admin", ["admin"], "wordlist.txt", 5, 0.5, 3.0, False)`

# HTTPS target
`run_http_brute("https://192.168.1.10/login", ["admin", "root"], "rockyou.txt", 5, 0.5, 3.0, False)`

# Stealth mode
`run_http_brute("http://192.168.1.10/admin", ["admin"], "wordlist.txt", 2, 2.0, 3.0, True)`

---

ARP Scanner - arp_scan.py
`from modules.network.arp_scan import run_arp_scan`
# Scan full /24 subnet
`run_arp_scan("192.168.1.0/24", 2)`

# Scan /16 — larger range, increase timeout
`run_arp_scan("10.0.0.0/16", 5)`

# Tight subnet — your lab only
`run_arp_scan("192.168.56.0/24", 2)`

---

DNS Spoofer - dns_spoof.py
from modules.network.dns_spoof import run_dns_spoof

# Spoof a single domain
`run_dns_spoof({"example.com": "192.168.1.100"}, "192.168.1.100", "eth0", 0)`

# Spoof multiple domains
```bash
run_dns_spoof(
    {"google.com": "192.168.1.100", "facebook.com": "192.168.1.100"},
    "192.168.1.100", "eth0", 0
)
```
# Wildcard — spoof ALL DNS queries
`run_dns_spoof({"*": "192.168.1.100"}, "192.168.1.100", "eth0", 0)`

# Stop after 10 spoofed packets
`run_dns_spoof({"example.com": "192.168.1.100"}, "192.168.1.100", "eth0", 10)`

# Different interface (WiFi)
`run_dns_spoof({"example.com": "192.168.1.100"}, "192.168.1.100", "wlan0", 0)`

---

Packet Crafter - packet_crafter.py
`from modules.network.packet_craft import send_syn, send_icmp, send_udp`
# Send SYN to port 80
`send_syn("192.168.1.10", 80, 12345, 3, 2.0)`

# Send SYN to port 22 — see if SSH responds
`send_syn("192.168.1.10", 22, 54321, 1, 2.0)`

# Send ICMP with custom payload
`send_icmp("192.168.1.10", "LYNKEUS", 4, 2.0)`

# Send ICMP with hidden data — test IDS detection
`send_icmp("192.168.1.10", "A" * 100, 3, 2.0)`

# Send UDP to DNS port
`send_udp("192.168.1.10", 53, "HELLO", 2, 2.0)`

---

Stealth Scanner - stealth_scan.py
`from modules.stealth.stealth_scan import run_stealth_scan`
# Low and slow — hardest to detect
`run_stealth_scan("192.168.1.10", range(1, 1025), 1.0, 5, 1.0, 5.0)`

# Medium stealth
`run_stealth_scan("192.168.1.10", range(1, 1025), 1.0, 10, 0.5, 2.0)`

# Specific ports — stealthier
`run_stealth_scan("192.168.1.10", [22, 80, 443, 3306, 3389], 1.0, 3, 2.0, 8.0)`

# Faster but still randomised
`run_stealth_scan("192.168.1.10", range(1, 1025), 1.0, 20, 0.1, 0.5)`

---

User Agent Rotator - user_agent.py
`from modules.stealth.user_agent import get_random_agent, get_all_agents, get_agent_count`
# Get a random agent for an HTTP request
`print (get_random_agent())`

# See how many are available
`print (get_agent_count())`

# Loop through all of them
```bash
for agent in get_all_agents():
    print (agent)
```

---

TTL Spoofer - ttl_spoof.py
`from modules.stealth.ttl_spoof import send_spoofed_syn`
# Impersonate a Windows machine
`send_spoofed_syn("192.168.1.10", 80, "windows", 3, 2.0)`

# Impersonate Linux
`send_spoofed_syn("192.168.1.10", 80, "linux", 3, 2.0)`

# Fully randomised TTL per packet
`send_spoofed_syn("192.168.1.10", 80, "random", 5, 2.0)`

# Test against SSH port as a Cisco device
`send_spoofed_syn("192.168.1.10", 22, "cisco", 2, 2.0)`
