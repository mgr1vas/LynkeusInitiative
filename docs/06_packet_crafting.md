# Packet Crafting

## What it is
Packet crafting is the process of manually building network packets from scratch, with full control over every field, source IP, destination IP, flags, TTL, payload, and more. Instead of letting the operating system handle how packets are formed, you build them yourself and inject them directly into the network.

## Why it matters
Every network communication you have ever done, browsing a website, sending an email, running a port scan, produces packets that your OS builds automatically using standard rules. Packet crafting breaks those rules. You can send packets that no normal application would ever produce, which is exactly what makes it useful for security testing.

## What Scapy is
Lynkeus uses Scapy, a Python library that gives you complete control over every layer of a network packet. With Scapy you can build, send, receive, and analyse packets at the raw level. It is the standard tool for packet crafting in security research.

## The three packet types Lynkeus crafts
**TCP SYN packets**
A SYN packet is the first step of a TCP handshake, the knock on the door. Sending a raw SYN and watching what comes back tells you:
- SYN-ACK reply means the port is open
- RST-ACK reply means the port is closed
- No reply means the port is filtered

This is the same technique nmap uses internally when you run a SYN scan.

**ICMP packets**
ICMP (Internet Control Message Protocol) is the protocol behind the ping command. Lynkeus can send ICMP packets with custom payloads, arbitrary data embedded inside the ping. This is used to test whether your IDS or SIEM detects unusual ICMP traffic, which is a common indicator of ICMP tunneling (a technique attackers use to smuggle data out of a network hidden inside ping packets).

**UDP packets**
UDP (User Datagram Protocol) is a connectionless protocol — it sends packets without establishing a connection first. Lynkeus can send UDP packets with custom payloads to any port, useful for testing UDP-based services and firewall rules.

## Reading the responses
| Response | Meaning |
|----------|---------|
| SYN-ACK (flags = SA) | Port is open, service is listening |
| RST-ACK (flags = RA) | Port is closed |
| No response | Port is filtered by a firewall |
| ICMP unreachable | Port is administratively blocked |

## Why it matters in pentesting
Packet crafting lets you test exactly how a target responds to unusual or malformed traffic. You can probe firewall rules, test IDS signatures, simulate attack traffic, and understand at a fundamental level what is happening on the wire during any network interaction.

## Why it matters in blue teaming
If you know how crafted packets look, you can write detection rules for them. Seeing a SYN packet with a source port of 12345 and no follow-up handshake is a classic port scan signature. Seeing oversized ICMP payloads is a classic tunnel detection signature. Building the offensive tool teaches you exactly what to look for on the defensive side.

## Key terms
- **Packet** — a unit of data sent across a network, containing headers and a payload
- **TCP** — Transmission Control Protocol, connection-based, reliable
- **UDP** — User Datagram Protocol, connectionless, fast
- **ICMP** — Internet Control Message Protocol, used for diagnostics like ping
- **SYN** — synchronise flag, initiates a TCP connection
- **RST** — reset flag, forcibly closes or rejects a connection
- **Payload** — the data carried inside a packet, after the headers
- **Scapy** — Python library for building and sending raw packets
