#!/usr/bin/env python3

# ─────────────────────────────────────────────
# modules/network/arp_scan.py
# Lynkeus Initiative — ARP Scanner
# Discovers all live hosts on the local subnet
# Maps IP addresses to MAC addresses
# Lab use only — run on your own network
# ─────────────────────────────────────────────

import socket
import struct
import time

# ── Attempt to import scapy — required for ARP ───────────────────
try:
    from scapy.all import ARP, Ether, srp, conf
    conf.verb = 0
except ImportError:
    print ("[!] scapy is not installed. Run: pip install scapy")
    exit(1)

from output.colors import GREEN, YELLOW, CYAN, DIM, BOLD, RESET


# ── Known vendor prefixes (first 3 bytes of MAC) ─────────────────
VENDOR_MAP = {
    "00:50:56": "VMware",
    "00:0c:29": "VMware",
    "08:00:27": "VirtualBox",
    "52:54:00": "QEMU/KVM",
    "00:1a:2b": "Cisco",
    "b8:27:eb": "Raspberry Pi",
    "dc:a6:32": "Raspberry Pi",
    "00:e0:4c": "Realtek",
}


def lookup_vendor(mac):
    """
    # Returns a vendor name based on the first 3 octets of the MAC
    # Returns 'Unknown' if the prefix is not in the local map
    """

    prefix = mac[:8].lower()

    for key, vendor in VENDOR_MAP.items():
        if prefix == key.lower():
            return vendor

    return "Unknown"


def run_arp_scan(subnet, timeout):
    """
    # Sends ARP requests across the entire subnet
    # Collects all responses and builds a host table
    # subnet format: '192.168.1.0/24'
    """

    print ("")
    print (CYAN + "=" * 55 + RESET)
    print (BOLD + "  ARP SCANNER — LIVE HOST DISCOVERY" + RESET)
    print (CYAN + "=" * 55 + RESET)
    print ("  Subnet  : " + BOLD + subnet + RESET)
    print ("  Timeout : " + str(timeout) + "s")
    print (CYAN + "-" * 55 + RESET)
    print ("")

    # ── Build ARP request packet ──────────────────────────────────
    arp     = ARP(pdst=subnet)
    ether   = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet  = ether / arp

    # ── Send packet and collect replies ──────────────────────────
    answered, _ = srp(packet, timeout=timeout, retry=1)

    hosts = []

    for sent, received in answered:
        vendor = lookup_vendor(received.hwsrc)

        host = {
            "ip":     received.psrc,
            "mac":    received.hwsrc,
            "vendor": vendor,
        }

        hosts.append(host)

        # ── Print each discovered host ────────────────────────────
        ip_col     = BOLD + received.psrc.ljust(18) + RESET
        mac_col    = YELLOW + received.hwsrc.ljust(20) + RESET
        vendor_col = DIM + vendor + RESET

        print ("  " + GREEN + "LIVE" + RESET + "  " + ip_col + mac_col + vendor_col)

    # ── Summary ───────────────────────────────────────────────────
    print ("")
    print (CYAN + "-" * 55 + RESET)
    print ("  " + BOLD + str(len(hosts)) + " live host(s)" + RESET + " discovered on " + subnet)
    print (CYAN + "=" * 55 + RESET)
    print ("")

    return hosts
