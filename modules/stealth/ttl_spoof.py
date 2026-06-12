#!/usr/bin/env python3

# modules/stealth/ttl_spoof.py
# Lynkeus Initiative — TTL Manipulator
# Adjusts TTL values on outgoing packets
# Confuses traceroute detection and hop-count analysis
# Lab use only — run against machines you own

import random

#  Attempt to import scapy 
try:
    from scapy.all import IP, TCP, send, sr1, conf
    conf.verb = 0
except ImportError:
    print ("[!] scapy is not installed. Run: pip install scapy")
    exit(1)

from output.colors import GREEN, YELLOW, CYAN, DIM, BOLD, RESET


#  Common TTL values used by different operating systems 
OS_TTL_PROFILES = {
    "windows":    128,
    "linux":       64,
    "macos":       64,
    "cisco":      255,
    "freebsd":     64,
    "random":    None,
}


def get_ttl(profile):
    """
    # Returns a TTL value based on the selected OS profile
    # 'random' returns a random value between 50 and 200
    # This makes your packets look like they came from different systems
    """

    if profile == "random":
        return random.randint(50, 200)

    return OS_TTL_PROFILES.get(profile, 64)


def send_spoofed_syn(target_ip, target_port, ttl_profile, count, timeout):
    """
    # Sends TCP SYN packets with a spoofed TTL value
    # Useful for confusing passive OS fingerprinting on the target
    """

    ttl = get_ttl(ttl_profile)

    print ("")
    print (CYAN + "=" * 55 + RESET)
    print (BOLD + "  TTL MANIPULATOR" + RESET)
    print (CYAN + "=" * 55 + RESET)
    print ("  Target  : " + BOLD + target_ip + ":" + str(target_port) + RESET)
    print ("  Profile : " + ttl_profile)
    print ("  TTL     : " + (str(ttl) if ttl_profile != "random" else "randomised per packet"))
    print ("  Count   : " + str(count))
    print (CYAN + "-" * 55 + RESET)
    print ("")

    for i in range(count):

        #  Randomise TTL per packet if random mode 
        if ttl_profile == "random":
            ttl = get_ttl("random")

        #  Build SYN packet with spoofed TTL 
        packet   = IP(dst=target_ip, ttl=ttl) / TCP(dport=target_port, flags="S")
        response = sr1(packet, timeout=timeout, verbose=0)

        if response:
            resp_ttl   = response[IP].ttl
            resp_flags = response[TCP].flags if response.haslayer(TCP) else "?"
            print (GREEN + "  [+] Response — TTL sent: " + str(ttl) + "  TTL received: " + str(resp_ttl) + "  Flags: " + str(resp_flags) + RESET)
        else:
            print (DIM + "  [~] No response for packet " + str(i + 1) + RESET)

    print ("")
    print (CYAN + "=" * 55 + RESET)
    print ("")
