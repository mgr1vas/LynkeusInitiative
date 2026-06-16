#!/usr/bin/env python3

# test_all.py
# Lynkeus Initiative
# Automated Framework Integrity Check

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from output.colors import GREEN, RED, YELLOW, CYAN, RESET

def run_integrity_check():
    print(CYAN + "\n  === LYNKEUS CORE INTEGRITY TEST ===" + RESET)
    print("  Validating internal module pathways...\n")

    # Mapping target components to ensure baseline operational imports
    modules_to_test = {
        "Core Port Scanner": "core.scanner",
        "SSH Brute Forcer": "modules.credentials.ssh_brute",
        "FTP Brute Forcer": "modules.credentials.ftp_brute",
        "HTTP Brute Forcer": "modules.credentials.http_brute",
        "ARP Network Scanner": "modules.network.arp_scan",
        "DNS Spoofer Engine": "modules.network.dns_spoof",
        "Packet Crafter Logic": "modules.network.packet_craft",
        "Stealth Timing Scan": "modules.stealth.stealth_scan",
        "TTL Profile Spoofer": "modules.stealth.ttl_spoof",
        "User Agent Pool": "modules.stealth.user_agent",
        "SYN Flood Logic": "modules.dos.syn_flood",
        "Volumetric Flooder": "modules.dos.udp_icmp_flood",
        "Slowloris Engine": "modules.dos.slowloris"
    }

    passed_tests = 0
    failed_tests = 0

    for name, path in modules_to_test.items():
        print(f"  [*] Testing import mapping: {name:<25} ", end="")
        try:
            # Dynamically check module initialization paths
            __import__(path)
            print("[" + GREEN + " SUCCESS " + RESET + "]")
            passed_tests += 1
        except Exception as e:
            print("[" + RED + " FAILED " + RESET + "]")
            print(YELLOW + f"      └─ Reason: {e}" + RESET)
            failed_tests += 1

    print(CYAN + "\n" + "=" * 45 + RESET)
    print(f"  Integrity scan finished. Status:")
    print(f"  Passed components : {GREEN}{passed_tests}{RESET}")
    print(f"  Failed components : {RED if failed_tests > 0 else GREEN}{failed_tests}{RESET}")
    print(CYAN + "=" * 45 + RESET + "\n")

if __name__ == "__main__":
    run_integrity_check()
