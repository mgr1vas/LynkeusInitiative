# ARP Scanning

## What it is
ARP scanning is the fastest and most reliable method for discovering every live device on a local network. It works at Layer 2 of the network model, below IP, directly at the hardware level, which means firewalls and host-based security tools almost never block it.

## What ARP is
ARP stands for Address Resolution Protocol. Every device on a local network has two addresses, an IP address (like 192.168.1.10) and a MAC address (like 00:1A:2B:3C:4D:5E). IP addresses are logical and can change. MAC addresses are burned into the hardware of the network card and are unique to every device ever made.

ARP is the protocol devices use to ask the question: "Who on this network has IP address 192.168.1.10? Tell me your MAC address so I can talk to you directly."

## How ARP scanning works
Lynkeus sends a broadcast ARP request to every IP address in the target subnet simultaneously, essentially shouting "Is anyone home?" to every possible address. Every live device that hears the request replies with its MAC address. Devices that are offline or do not exist simply do not respond.

## What Lynkeus reports
For each live host discovered:
- **IP address** — the logical network address of the device
- **MAC address** — the hardware address of the device's network card
- **Vendor** — the manufacturer identified from the first three bytes of the MAC address

The vendor lookup is what makes ARP scanning particularly useful. The first three bytes of every MAC address (called the OUI — Organizationally Unique Identifier) identify the manufacturer. This is how you know that `00:50:56` is a VMware VM, `b8:27:eb` is a Raspberry Pi, or `00:1a:2b` is a Cisco device.

## Why it matters in pentesting
Before you can attack anything you need to know what exists. ARP scanning gives you a complete map of every live host on the local network in seconds, something that takes much longer with IP-based scanning. In a home lab it tells you exactly which VMs are online and what their addresses are.

## Why it matters in blue teaming
Rogue device detection is built on ARP scanning. If you baseline your network, you can run periodic ARP scans and alert on any new MAC address that was not there before. That is how you detect an unauthorized device connecting to your network.

## Key terms
- **ARP** — Address Resolution Protocol, maps IP addresses to MAC addresses
- **MAC address** — hardware address, 6 bytes written as XX:XX:XX:XX:XX:XX
- **OUI** — first 3 bytes of a MAC, identifies the manufacturer
- **Broadcast** — a message sent to all devices on the network at once
- **Subnet** — a range of IP addresses on the same local network, written in CIDR notation like 192.168.1.0/24