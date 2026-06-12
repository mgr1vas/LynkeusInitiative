#!/usr/bin/env python3

# modules/network/packet_craft.py
# Lynkeus Initiative — Packet Crafter
# Build and send custom raw packets using Scapy
# Useful for testing IDS rules and firewall responses
# Lab use only — run against machines you own

# Attempt to import scapy 
try:
    from scapy.all import IP, TCP, UDP, ICMP, Raw, send, sr1, conf
    conf.verb = 0
except ImportError:
    print ("[!] scapy is not installed. Run: pip install scapy")
    exit(1)

from output.colors import GREEN, RED, YELLOW, CYAN, DIM, BOLD, RESET


def send_syn(target_ip, target_port, source_port, count, timeout):
    """
    # Sends a raw TCP SYN packet to the target
    # Useful for testing how a host responds to half-open connections
    # This is what a basic port scanner does at the network level
    """

    print ("")
    print (CYAN + "=" * 55 + RESET)
    print (BOLD + "  PACKET CRAFTER — TCP SYN" + RESET)
    print (CYAN + "=" * 55 + RESET)
    print ("  Target  : " + BOLD + target_ip + ":" + str(target_port) + RESET)
    print ("  Count   : " + str(count))
    print (CYAN + "-" * 55 + RESET)
    print ("")

    for i in range(count):

        #  Build SYN packet 
        packet = IP(dst=target_ip) / TCP(sport=source_port, dport=target_port, flags="S")

        # Send and wait for response 
        response = sr1(packet, timeout=timeout, verbose=0)

        if response:
            tcp_flags = response[TCP].flags if response.haslayer(TCP) else "?"

            if tcp_flags == "SA":
                #  SYN-ACK = port open 
                print (GREEN + "  [+] SYN-ACK received — port " + str(target_port) + " is OPEN" + RESET)

            elif tcp_flags == "RA":
                #  RST-ACK = port closed 
                print (RED + "  [-] RST-ACK received — port " + str(target_port) + " is CLOSED" + RESET)

            else:
                print (YELLOW + "  [?] Unexpected flags: " + str(tcp_flags) + RESET)

        else:
            print (DIM + "  [~] No response — port may be filtered" + RESET)

    print ("")
    print (CYAN + "=" * 55 + RESET)
    print ("")


def send_icmp(target_ip, payload, count, timeout):
    """
    # Sends ICMP echo requests with a custom payload
    # Useful for testing ICMP tunnel detection rules in your SIEM
    """

    print ("")
    print (CYAN + "=" * 55 + RESET)
    print (BOLD + "  PACKET CRAFTER — ICMP PING" + RESET)
    print (CYAN + "=" * 55 + RESET)
    print ("  Target  : " + BOLD + target_ip + RESET)
    print ("  Payload : " + payload)
    print ("  Count   : " + str(count))
    print (CYAN + "-" * 55 + RESET)
    print ("")

    for i in range(count):

        # Build ICMP packet with custom payload 
        packet   = IP(dst=target_ip) / ICMP() / Raw(load=payload.encode())
        response = sr1(packet, timeout=timeout, verbose=0)

        if response:
            print (GREEN + "  [+] Reply from " + response[IP].src + " — TTL: " + str(response[IP].ttl) + RESET)
        else:
            print (DIM + "  [~] No reply" + RESET)

    print ("")
    print (CYAN + "=" * 55 + RESET)
    print ("")


def send_udp(target_ip, target_port, payload, count, timeout):
    """
    # Sends UDP packets with a custom payload to the target
    # Useful for testing UDP service responses and firewall rules
    """

    print ("")
    print (CYAN + "=" * 55 + RESET)
    print (BOLD + "  PACKET CRAFTER — UDP" + RESET)
    print (CYAN + "=" * 55 + RESET)
    print ("  Target  : " + BOLD + target_ip + ":" + str(target_port) + RESET)
    print ("  Payload : " + payload)
    print ("  Count   : " + str(count))
    print (CYAN + "-" * 55 + RESET)
    print ("")

    for i in range(count):

        # Build UDP packet 
        packet   = IP(dst=target_ip) / UDP(dport=target_port) / Raw(load=payload.encode())
        response = sr1(packet, timeout=timeout, verbose=0)

        if response:
            print (GREEN + "  [+] Response received from " + response[IP].src + RESET)
        else:
            print (DIM + "  [~] No response" + RESET)

    print ("")
    print (CYAN + "=" * 55 + RESET)
    print ("")
