# Lynkeus
![Image](assets/lynkeus_logo.png)

### *See through every wall.*

> In Greek mythology, Lynkeus was the Argonaut gifted with superhuman vision —  
> able to see through walls, into the earth, and across any obstacle.  
> This tool carries his name.

---

## What it does

Lynkeus is a modular port scanner and banner grabber written from scratch in Python.  
It maps open ports on a target, identifies running services, and captures banner information — giving you a clear picture of what's exposed.

Built for home lab and educational use. Run only against machines you own.

---

## Features

- Fast concurrent TCP port scanning
- Service banner grabbing (SSH version, HTTP headers, etc.)
- Identifies well-known services — SSH, RDP, SMB, MySQL, FTP, and more
- Clean coloured terminal output with ASCII header
- Optional structured JSON report export

---

## Folder structure

```
lynkeus/
├── main.py                  # Entry point — run this
├── README.md
├── .gitignore
├── core/
│   ├── scanner.py           # Thread pool + scan orchestration
│   └── probe.py             # TCP probe + banner grab logic
├── utils/
│   ├── resolver.py          # Hostname → IP resolution
│   ├── ports.py             # Port argument parser
│   └── port_names.py        # Port number → service name map
├── output/
│   ├── colors.py            # ANSI colour constants
│   └── display.py           # ASCII banner + all print functions
└── reports/
    └── json_report.py       # JSON report writer
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

No external libraries — pure Python 3 standard library only.

```bash
python3 --version   # Python 3.6+ required
```

---

## Disclaimer

Lynkeus is built for educational use in your own home lab only.  
Do not scan systems you do not own or have explicit written permission to test.
