# Lynkeus
![Image](assets/lynkeus_logo.png)

### *See through every wall.*

> In Greek mythology, Lynkeus was the Argonaut gifted with superhuman vision, 
> able to see through walls, into the earth, and across any obstacle.  
> This tool carries his name.

---

## Capabilities

The Lynkeus Initiative is not a finished product, it is a living framework.
New modules are added as skills grow. Every capability in this project was built to be understood, not just used. If a tool exists here, the person who put it here can explain every line of it.
Planned additions include post-exploitation modules, a unified CLI, SIEM integration, automated reporting, and a full recon-to-report pipeline. The framework grows with the operator.
The mission is never complete. Lynkeus never stops looking.

---

## Features

- Fast concurrent TCP port scanning
- Service banner grabbing (SSH version, HTTP headers, etc.)
- Identifies well-known services — SSH, RDP, SMB, MySQL, FTP, and more
- Clean coloured terminal output with ASCII header
- Optional structured JSON report export

---

## Folder Structure

```
LynkeusInitiative/
├── main.py
├── README.md
├── .gitignore
├── requirements.txt
├── core/
│   ├── __init__.py
│   ├── scanner.py
│   └── probe.py
├── utils/
│   ├── __init__.py
│   ├── resolver.py
│   ├── ports.py
│   └── port_names.py
├── output/
│   ├── __init__.py
│   ├── colors.py
│   └── display.py
├── reports/
│   ├── __init__.py
│   └── json_report.py
└── modules/
    ├── __init__.py
    ├── credentials/
    │   ├── __init__.py
    │   ├── ssh_brute.py
    │   ├── ftp_brute.py
    │   └── http_brute.py
    ├── network/
    │   ├── __init__.py
    │   ├── arp_scan.py
    │   ├── dns_spoof.py
    │   └── packet_craft.py
    └── stealth/
        ├── __init__.py
        ├── stealth_scan.py
        ├── user_agent.py
        └── ttl_spoof.py   
```

---

## Usage

```bash
# Basic scan — ports 1 to 1024
python3 main.py 192.168.1.1

# Scan specific ports
python3 main.py 192.168.1.1 -p 22,80,443,3306,3389

# Full scan with more threads and a saved report
python3 main.py 192.168.1.1 -p 1-65535 -w 200 -o results.json

# Scan by hostname
python3 main.py scanme.nmap.org -p 1-1024
```

### Flags

| Flag | Default | Description |
|------|---------|-------------|
| `-p` | `1-1024` | Ports to scan: `80`, `1-1024`, `22,80,443` |
| `-t` | `1.0` | Timeout per connection in seconds |
| `-w` | `100` | Number of concurrent threads |
| `-o` | None | Save output to a JSON file |

---

## Requirements

No external libraries, pure Python 3 standard library only. **FOR NOW**

```bash
python3 --version   # Python 3.6+ required
```
## Disclaimer

Lynkeus is built for educational use in your own home lab only.  
Do not scan systems you do not own or have explicit written permission to test.
