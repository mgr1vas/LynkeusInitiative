#!/usr/bin/env python3

# main.py
# Lynkeus Initiative
# Main entry point — interactive CLI menu
# Run this file to access all modules

import sys
import os

# Add project root to path so all imports resolve correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from output.colors import GREEN, RED, YELLOW, CYAN, DIM, BOLD, RESET
from output.display import print_banner_main


def menu():
    # Prints the main module selection menu
    print ("")
    print (CYAN + "=" * 55 + RESET)
    print (BOLD + "  LYNKEUS INITIATIVE — MAIN MENU" + RESET)
    print (CYAN + "=" * 55 + RESET)
    print ("")
    print (BOLD + "  CORE" + RESET)
    print ("  [1]  Port Scanner + Banner Grabber")
    print ("")
    print (BOLD + "  CREDENTIALS" + RESET)
    print ("  [2]  SSH Brute Forcer")
    print ("  [3]  FTP Brute Forcer")
    print ("  [4]  HTTP Basic Auth Brute Forcer")
    print ("")
    print (BOLD + "  NETWORK" + RESET)
    print ("  [5]  ARP Scanner — Live Host Discovery")
    print ("  [6]  DNS Spoofer")
    print ("  [7]  Packet Crafter")
    print ("")
    print (BOLD + "  STEALTH" + RESET)
    print ("  [8]  Stealth Scanner")
    print ("  [9]  TTL Spoofer")
    print ("  [10] User Agent Rotator")
    print ("")
    print (BOLD + "  DENIAL OF SERVICE" + RESET)
    print ("  [12] SYN Flood")
    print ("")
    print (BOLD + "  OTHER" + RESET)
    print ("  [11] Run All Modules (test_all.py)")
    print ("  [0]  Exit")
    print ("")
    print (CYAN + "=" * 55 + RESET)


def get_input(prompt, default=None):

    # Helper to get user input with an optional default value

    if default is not None:
        value = input("  " + prompt + " [" + str(default) + "]: ").strip()
        return value if value else str(default)
    else:
        value = input("  " + prompt + ": ").strip()
        return value


def get_usernames():

    # Helper to collect a list of usernames from the user

    raw = get_input("Usernames (comma separated, e.g. admin,root,user)")
    return [u.strip() for u in raw.split(",") if u.strip()]


def run_port_scanner():

    # Module 1 — Core Port Scanner

    from core.scanner import run_scan
    from utils.resolver import resolve_target
    from utils.ports import parse_ports
    from output.display import print_banner, print_summary
    from reports.json_report import save_report

    print ("")
    print (CYAN + "  PORT SCANNER" + RESET)
    print (CYAN + "  " + "-" * 40 + RESET)

    target  = get_input("Target IP or hostname")
    ports   = get_input("Ports", "1-1024")
    timeout = float(get_input("Timeout (seconds)", "1.0"))
    workers = int(get_input("Threads", "100"))
    output  = get_input("Save report to JSON? (filename or leave blank)", "")

    ip        = resolve_target(target)
    port_list = parse_ports(ports)

    print_banner(target, ip, len(port_list))
    results = run_scan(ip, port_list, timeout, workers)
    print_summary(len(results), len(port_list))

    if output:
        save_report(target, ip, results, output)


def run_ssh_brute():

    # Module 2 — SSH Brute Forcer

    from modules.credentials.ssh_brute import run_ssh_brute

    print ("")
    print (CYAN + "  SSH BRUTE FORCER" + RESET)
    print (CYAN + "  " + "-" * 40 + RESET)

    host      = get_input("Target IP or hostname")
    port      = int(get_input("SSH port", "22"))
    usernames = get_usernames()
    wordlist  = get_input("Path to wordlist")
    threads   = int(get_input("Threads", "5"))
    delay     = float(get_input("Delay between attempts (seconds)", "0.5"))
    timeout   = float(get_input("Timeout (seconds)", "3.0"))
    stealth   = get_input("Stealth mode? hides failed attempts (y/n)", "n").lower() == "y"

    run_ssh_brute(host, port, usernames, wordlist, threads, delay, timeout, stealth)


def run_ftp_brute():

    # Module 3 — FTP Brute Forcer

    from modules.credentials.ftp_brute import run_ftp_brute

    print ("")
    print (CYAN + "  FTP BRUTE FORCER" + RESET)
    print (CYAN + "  " + "-" * 40 + RESET)

    host      = get_input("Target IP or hostname")
    port      = int(get_input("FTP port", "21"))
    usernames = get_usernames()
    wordlist  = get_input("Path to wordlist")
    threads   = int(get_input("Threads", "5"))
    delay     = float(get_input("Delay between attempts (seconds)", "0.5"))
    timeout   = float(get_input("Timeout (seconds)", "3.0"))
    stealth   = get_input("Stealth mode? (y/n)", "n").lower() == "y"

    run_ftp_brute(host, port, usernames, wordlist, threads, delay, timeout, stealth)


def run_http_brute():

    # Module 4 — HTTP Basic Auth Brute Forcer

    from modules.credentials.http_brute import run_http_brute

    print ("")
    print (CYAN + "  HTTP BRUTE FORCER" + RESET)
    print (CYAN + "  " + "-" * 40 + RESET)

    url       = get_input("Target URL (e.g. http://192.168.1.10/admin)")
    usernames = get_usernames()
    wordlist  = get_input("Path to wordlist")
    threads   = int(get_input("Threads", "5"))
    delay     = float(get_input("Delay between attempts (seconds)", "0.5"))
    timeout   = float(get_input("Timeout (seconds)", "3.0"))
    stealth   = get_input("Stealth mode? (y/n)", "n").lower() == "y"

    run_http_brute(url, usernames, wordlist, threads, delay, timeout, stealth)


def run_arp_scan():

    # Module 5 — ARP Scanner

    from modules.network.arp_scan import run_arp_scan

    print ("")
    print (CYAN + "  ARP SCANNER" + RESET)
    print (CYAN + "  " + "-" * 40 + RESET)

    subnet  = get_input("Subnet in CIDR notation (e.g. 192.168.1.0/24)")
    timeout = float(get_input("Timeout (seconds)", "2"))

    run_arp_scan(subnet, timeout)


def run_dns_spoof():

    # Module 6 — DNS Spoofer

    from modules.network.dns_spoof import run_dns_spoof

    print ("")
    print (CYAN + "  DNS SPOOFER" + RESET)
    print (CYAN + "  " + "-" * 40 + RESET)

    redirect_ip   = get_input("IP to redirect victims to")
    interface     = get_input("Network interface", "eth0")
    packet_limit  = int(get_input("Stop after how many spoofed packets? (0 = unlimited)", "0"))

    print ("")
    print (DIM + "  Enter domains to spoof. Type 'done' when finished." + RESET)
    print (DIM + "  Type * to spoof ALL domains (wildcard)." + RESET)
    print ("")

    targets = {}

    while True:
        domain = input("  Domain (or 'done'): ").strip()
        if domain.lower() == "done":
            break
        if domain:
            ip = get_input("Redirect " + domain + " to IP", redirect_ip)
            targets[domain] = ip

    if not targets:
        print (RED + "  [!] No domains entered. Returning to menu." + RESET)
        return

    run_dns_spoof(targets, redirect_ip, interface, packet_limit)


def run_packet_crafter():

    # Module 7 — Packet Crafter

    from modules.network.packet_craft import send_syn, send_icmp, send_udp

    print ("")
    print (CYAN + "  PACKET CRAFTER" + RESET)
    print (CYAN + "  " + "-" * 40 + RESET)
    print ("")
    print ("  [1]  TCP SYN")
    print ("  [2]  ICMP Ping")
    print ("  [3]  UDP")
    print ("")

    choice = get_input("Select packet type")

    if choice == "1":
        target_ip   = get_input("Target IP")
        target_port = int(get_input("Target port"))
        source_port = int(get_input("Source port", "12345"))
        count       = int(get_input("Number of packets", "3"))
        timeout     = float(get_input("Timeout (seconds)", "2.0"))
        send_syn(target_ip, target_port, source_port, count, timeout)

    elif choice == "2":
        target_ip = get_input("Target IP")
        payload   = get_input("Custom payload", "LYNKEUS")
        count     = int(get_input("Number of packets", "4"))
        timeout   = float(get_input("Timeout (seconds)", "2.0"))
        send_icmp(target_ip, payload, count, timeout)

    elif choice == "3":
        target_ip   = get_input("Target IP")
        target_port = int(get_input("Target port", "53"))
        payload     = get_input("Custom payload", "LYNKEUS")
        count       = int(get_input("Number of packets", "2"))
        timeout     = float(get_input("Timeout (seconds)", "2.0"))
        send_udp(target_ip, target_port, payload, count, timeout)

    else:
        print (RED + "  [!] Invalid choice." + RESET)


def run_stealth_scanner():

    # Module 8 — Stealth Scanner

    from modules.stealth.stealth_scan import run_stealth_scan
    from utils.ports import parse_ports

    print ("")
    print (CYAN + "  STEALTH SCANNER" + RESET)
    print (CYAN + "  " + "-" * 40 + RESET)

    ip        = get_input("Target IP")
    ports     = get_input("Ports", "1-1024")
    timeout   = float(get_input("Timeout (seconds)", "1.0"))
    workers   = int(get_input("Threads (keep low for stealth)", "5"))
    min_delay = float(get_input("Min jitter delay (seconds)", "0.5"))
    max_delay = float(get_input("Max jitter delay (seconds)", "2.0"))

    port_list = parse_ports(ports)

    run_stealth_scan(ip, port_list, timeout, workers, min_delay, max_delay)


def run_ttl_spoof():

    # Module 9 — TTL Spoofer

    from modules.stealth.ttl_spoof import send_spoofed_syn

    print ("")
    print (CYAN + "  TTL SPOOFER" + RESET)
    print (CYAN + "  " + "-" * 40 + RESET)
    print ("")
    print (DIM + "  Profiles: windows | linux | macos | cisco | freebsd | random" + RESET)
    print ("")

    target_ip   = get_input("Target IP")
    target_port = int(get_input("Target port", "80"))
    profile     = get_input("OS profile", "random")
    count       = int(get_input("Number of packets", "3"))
    timeout     = float(get_input("Timeout (seconds)", "2.0"))

    send_spoofed_syn(target_ip, target_port, profile, count, timeout)


def run_user_agent():

    # Module 10 — User Agent Rotator

    from modules.stealth.user_agent import get_random_agent, get_all_agents, get_agent_count

    print ("")
    print (CYAN + "  USER AGENT ROTATOR" + RESET)
    print (CYAN + "  " + "-" * 40 + RESET)
    print ("")
    print ("  [1]  Get one random agent")
    print ("  [2]  Show all agents")
    print ("  [3]  Show agent count")
    print ("")

    choice = get_input("Select option")

    if choice == "1":
        print ("")
        print (GREEN + "  " + get_random_agent() + RESET)
        print ("")

    elif choice == "2":
        print ("")
        for agent in get_all_agents():
            print (GREEN + "  " + agent + RESET)
        print ("")

    elif choice == "3":
        print ("")
        print (GREEN + "  Agent pool size: " + str(get_agent_count()) + RESET)
        print ("")

    else:
        print (RED + "  [!] Invalid choice." + RESET)

def run_syn_flood_module():
    # Module 12 — SYN Flood
    from modules.dos.syn_flood import run_syn_flood

    print ("")
    print (CYAN + "  SYN FLOOD TOOL" + RESET)
    print (CYAN + "  " + "-" * 40 + RESET)

    target_ip   = get_input("Target IP")
    target_port = int(get_input("Target Port", "80"))
    duration    = int(get_input("Duration (seconds)", "10"))
    threads     = int(get_input("Threads", "10"))

    run_syn_flood(target_ip, target_port, duration, threads)

def run_test_all():

    # Module 11 — Run all modules via test_all.py

    print ("")
    print (YELLOW + "  [*] Launching test_all.py..." + RESET)
    print (DIM + "  Make sure you have edited the CONFIG section in test_all.py first." + RESET)
    print ("")
    os.system("python3 test_all.py")


# Module router — maps menu choices to functions
MODULES = {
    "1":  run_port_scanner,
    "2":  run_ssh_brute,
    "3":  run_ftp_brute,
    "4":  run_http_brute,
    "5":  run_arp_scan,
    "6":  run_dns_spoof,
    "7":  run_packet_crafter,
    "8":  run_stealth_scanner,
    "9":  run_ttl_spoof,
    "10": run_user_agent,
    "11": run_test_all,
}


def main():

    # Print ASCII header once at startup
    print_banner_main()

    while True:

        # Show the menu
        menu()

        choice = input("  Select module: ").strip()

        if choice == "0":
            print ("")
            print (CYAN + "  Lynkeus out." + RESET)
            print ("")
            sys.exit(0)

        elif choice in MODULES:
            try:
                MODULES[choice]()
            except KeyboardInterrupt:
                print ("")
                print (YELLOW + "  [!] Module interrupted. Returning to menu." + RESET)

        else:
            print ("")
            print (RED + "  [!] Invalid choice. Enter a number from the menu." + RESET)

        input("\n  Press Enter to return to menu...")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# main.py
# Lynkeus — See through every wall.
# Entry point — parses arguments and launches the scan

import argparse
from core.scanner import run_scan
from utils.resolver import resolve_target
from utils.ports import parse_ports
from output.display import print_banner, print_summary
from reports.json_report import save_report


def main():

    # Argument parser
    parser = argparse.ArgumentParser(
        prog="lynkeus",
        description="Lynkeus — Port Scanner + Banner Grabber | Lab use only"
    )

    parser.add_argument("target",           help="Target IP or hostname")
    parser.add_argument("-p", "--ports",    default="1-1024",
                        help="Ports: '80'  '1-1024'  '22,80,443'  (default: 1-1024)")
    parser.add_argument("-t", "--timeout",  type=float, default=1.0,
                        help="Connection timeout in seconds (default: 1.0)")
    parser.add_argument("-w", "--workers",  type=int,   default=100,
                        help="Concurrent threads (default: 100)")
    parser.add_argument("-o", "--output",   default=None,
                        help="Save results to a JSON file (optional)")

    args = parser.parse_args()

    # Resolve target hostname to IP
    ip = resolve_target(args.target)

    # Parse port range or list
    ports = parse_ports(args.ports)

    # Print Lynkeus scan header 
    print_banner(args.target, ip, len(ports))

    # Run the scan 
    open_ports = run_scan(ip, ports, args.timeout, args.workers)

    # Print summary
    print_summary(len(open_ports), len(ports))

    # Save JSON report if output flag was passed
    if args.output:
        save_report(args.target, ip, open_ports, args.output)


if __name__ == "__main__":
    main()
