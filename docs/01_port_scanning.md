# Port Scanning

## What it is
Port scanning is the process of probing a target machine to find out which network ports are open, closed, or filtered. Every service running on a computer listens on a specific port number, SSH on 22, HTTP on 80, RDP on 3389. A port scanner systematically knocks on each door and records what answers.

## How it works
A TCP port scan works by attempting a full or partial connection to each port on the target. The three possible responses are:

- **Open** — the port accepted the connection. A service is running and listening
- **Closed** — the port rejected the connection with a RST (reset) packet. The host is alive but nothing is listening there
- **Filtered** — no response came back at all. A firewall is likely dropping the packets silently

## What Lynkeus does
Lynkeus uses a full TCP connect scan, it completes the three-way handshake (SYN, SYN-ACK, ACK) to confirm a port is open, then immediately closes the connection and attempts to grab the service banner.

## Why it matters in pentesting
Port scanning is always the first step in a real engagement. You cannot attack what you cannot see. Before exploiting anything, you need to know what services are exposed, what versions they are running, and what the attack surface looks like.

## Key terms

- **Port** — a numbered endpoint (0–65535) that a service listens on
- **TCP** — Transmission Control Protocol, the connection-based protocol most services use
- **SYN** — the first packet in a TCP handshake, sent to initiate a connection
- **SYN-ACK** — the server's reply confirming it is listening
- **RST** — a reset packet, meaning the port is closed
- **Banner** — the first message a service sends after a connection is made, often containing version info

## Ports to always check
| Port | Service |
|------|---------|
| 21 | FTP |
| 22 | SSH |
| 23 | Telnet |
| 80 | HTTP |
| 443 | HTTPS |
| 445 | SMB |
| 3306 | MySQL |
| 3389 | RDP |
| 5900 | VNC |
