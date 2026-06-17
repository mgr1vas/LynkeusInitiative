#!/usr/bin/env python3

# main.py
# Lynkeus Initiative
# Interactive Command-Driven Console Shell

import sys
import os
import cmd
import shlex

# Add project root to path so all imports resolve correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from output.colors import GREEN, RED, YELLOW, CYAN, DIM, BOLD, RESET
from output.display import print_banner_main
from utils.logger import log


class LynkeusShell(cmd.Cmd):
    prompt = BOLD + CYAN + "lynkeus > " + RESET
    intro = ""

    def emptyline(self):
        # Do nothing on empty input instead of repeating last command
        pass

    def default(self, line):
        print(RED + f"  [!] Unknown command: '{line}'. Type 'help' or '?' to see modules." + RESET)

    # Automatically intercept and log all command strings prior to execution
    def precmd(self, line):
        clean_line = line.strip()
        if clean_line and clean_line not in ["exit", "quit"]:
            log.info(f"Console command executed: '{clean_line}'")
        return line

    # Exit the console shell
    def do_exit(self, arg):
        print(CYAN + "\n  Lynkeus out.\n" + RESET)
        return True

    # Alias for exit
    def do_quit(self, arg):
        return self.do_exit(arg)

    # Scan ports and grab banners
    def do_scan(self, arg):
        args = shlex.split(arg)
        if len(args) < 1:
            print(YELLOW + "  Usage: scan <target> [ports] [threads] [timeout]" + RESET)
            return

        from core.scanner import run_scan
        from utils.resolver import resolve_target
        from utils.ports import parse_ports
        from output.display import print_banner, print_summary

        target = args[0]
        ports = args[1] if len(args) > 1 else "1-1024"
        workers = int(args[2]) if len(args) > 2 else 100
        timeout = float(args[3]) if len(args) > 3 else 1.0

        print(CYAN + "\n  PORT SCANNER" + RESET)
        print(CYAN + "  " + "-" * 40 + RESET)
        
        try:
            ip = resolve_target(target)
            port_list = parse_ports(ports)
            print_banner(target, ip, len(port_list))
            run_scan(ip, port_list, timeout, workers)
        except Exception as e:
            print(RED + f"  [!] Error: {e}" + RESET)

    # Helper to parse common credential testing arguments
    def _parse_brute_args(self, args):
        if len(args) < 3:
            return None
        host = args[0]
        usernames = [u.strip() for u in args[1].split(",") if u.strip()]
        wordlist = args[2]
        threads = int(args[3]) if len(args) > 3 else 5
        delay = float(args[4]) if len(args) > 4 else 0.5
        return host, usernames, wordlist, threads, delay

    # Test SSH credentials
    def do_sshbrute(self, arg):
        args = shlex.split(arg)
        parsed = self._parse_brute_args(args)
        if not parsed:
            print(YELLOW + "  Usage: sshbrute <target> <users> <wordlist> [threads] [delay]" + RESET)
            return
        
        from modules.credentials.ssh_brute import run_ssh_brute
        host, users, wordlist, threads, delay = parsed
        
        print(CYAN + "\n  SSH BRUTE FORCER" + RESET)
        print(CYAN + "  " + "-" * 40 + RESET)
        run_ssh_brute(host, 22, users, wordlist, threads, delay, 3.0, False)

    # Test FTP credentials
    def do_ftpbrute(self, arg):
        args = shlex.split(arg)
        parsed = self._parse_brute_args(args)
        if not parsed:
            print(YELLOW + "  Usage: ftpbrute <target> <users> <wordlist> [threads] [delay]" + RESET)
            return

        from modules.credentials.ftp_brute import run_ftp_brute
        host, users, wordlist, threads, delay = parsed

        print(CYAN + "\n  FTP BRUTE FORCER" + RESET)
        print(CYAN + "  " + "-" * 40 + RESET)
        run_ftp_brute(host, 21, users, wordlist, threads, delay, 3.0, False)

    # Test HTTP basic auth
    def do_httpbrute(self, arg):
        args = shlex.split(arg)
        if len(args) < 3:
            print(YELLOW + "  Usage: httpbrute <url> <users> <wordlist> [threads] [delay]" + RESET)
            return

        from modules.credentials.http_brute import run_http_brute
        url = args[0]
        usernames = [u.strip() for u in args[1].split(",") if u.strip()]
        wordlist = args[2]
        threads = int(args[3]) if len(args) > 3 else 5
        delay = float(args[4]) if len(args) > 4 else 0.5

        print(CYAN + "\n  HTTP BRUTE FORCER" + RESET)
        print(CYAN + "  " + "-" * 40 + RESET)
        run_http_brute(url, usernames, wordlist, threads, delay, 3.0, False)

    # Discover hosts via ARP
    def do_arpscan(self, arg):
        args = shlex.split(arg)
        if len(args) < 1:
            print(YELLOW + "  Usage: arpscan <subnet_cidr> [timeout]" + RESET)
            return

        from modules.network.arp_scan import run_arp_scan
        subnet = args[0]
        timeout = float(args[1]) if len(args) > 1 else 2.0

        print(CYAN + "\n  ARP SCANNER" + RESET)
        print(CYAN + "  " + "-" * 40 + RESET)
        run_arp_scan(subnet, timeout)

    # Spoof DNS responses
    def do_dnsspoof(self, arg):
        args = shlex.split(arg)
        if len(args) < 1:
            print(YELLOW + "  Usage: dnsspoof <redirect_ip> [interface] [packet_limit]" + RESET)
            return

        from modules.network.dns_spoof import run_dns_spoof
        redirect_ip = args[0]
        interface = args[1] if len(args) > 1 else "eth0"
        packet_limit = int(args[2]) if len(args) > 2 else 0

        print(CYAN + "\n  DNS SPOOFER" + RESET)
        print(CYAN + "  " + "-" * 40 + RESET)
        print(DIM + "  Enter domains to target. Type 'done' when finished." + RESET)
        
        targets = {}
        while True:
            domain = input("  Domain (or 'done'): ").strip()
            if domain.lower() == "done":
                break
            if domain:
                targets[domain] = redirect_ip

        if not targets:
            print(RED + "  [!] No domains specified." + RESET)
            return

        run_dns_spoof(targets, redirect_ip, interface, packet_limit)

    # Craft custom raw packets
    def do_craft(self, arg):
        args = shlex.split(arg)
        if len(args) < 2:
            print(YELLOW + "  Usage: craft <syn|icmp|udp> <target_ip> [port/payload]" + RESET)
            return

        from modules.network.packet_craft import send_syn, send_icmp, send_udp
        mode = args[0].lower()
        target_ip = args[1]

        print(CYAN + "\n  PACKET CRAFTER" + RESET)
        print(CYAN + "  " + "-" * 40 + RESET)

        if mode == "syn":
            port = int(args[2]) if len(args) > 2 else 80
            send_syn(target_ip, port, 12345, 3, 2.0)
        elif mode == "icmp":
            payload = args[2] if len(args) > 2 else "LYNKEUS"
            send_icmp(target_ip, payload, 4, 2.0)
        elif mode == "udp":
            port = int(args[2]) if len(args) > 2 else 53
            send_udp(target_ip, port, "LYNKEUS", 2, 2.0)
        else:
            print(RED + "  [!] Invalid packet structure type specified." + RESET)

    # Run stealth port scan
    def do_stealthscan(self, arg):
        args = shlex.split(arg)
        if len(args) < 1:
            print(YELLOW + "  Usage: stealthscan <target_ip> [ports] [threads] [min_delay] [max_delay]" + RESET)
            return

        from modules.stealth.stealth_scan import run_stealth_scan
        from utils.ports import parse_ports

        ip = args[0]
        ports = args[1] if len(args) > 1 else "1-1024"
        workers = int(args[2]) if len(args) > 2 else 5
        min_d = float(args[3]) if len(args) > 3 else 0.5
        max_d = float(args[4]) if len(args) > 4 else 2.0

        print(CYAN + "\n  STEALTH SCANNER" + RESET)
        print(CYAN + "  " + "-" * 40 + RESET)
        run_stealth_scan(ip, parse_ports(ports), 1.0, workers, min_d, max_d)

    # Spoof OS profile signatures via TTL
    def do_ttlspoof(self, arg):
        args = shlex.split(arg)
        if len(args) < 2:
            print(YELLOW + "  Usage: ttlspoof <target_ip> <port> [profile]" + RESET)
            return

        from modules.stealth.ttl_spoof import send_spoofed_syn
        target_ip = args[0]
        port = int(args[1])
        profile = args[2] if len(args) > 2 else "random"

        print(CYAN + "\n  TTL SPOOFER" + RESET)
        print(CYAN + "  " + "-" * 40 + RESET)
        send_spoofed_syn(target_ip, port, profile, 3, 2.0)

    # Rotate browser user-agent signatures
    def do_useragent(self, arg):
        from modules.stealth.user_agent import get_random_agent, get_all_agents, get_agent_count
        mode = arg.strip().lower()

        print(CYAN + "\n  USER AGENT ROTATOR" + RESET)
        print(CYAN + "  " + "-" * 40 + RESET)

        if mode == "random" or not mode:
            print(GREEN + f"  [+] Active Agent: {get_random_agent()}" + RESET)
        elif mode == "showall":
            for agent in get_all_agents():
                print(GREEN + f"  {agent}" + RESET)
        elif mode == "count":
            print(GREEN + f"  Pool Database Size: {get_agent_count()}" + RESET)
        else:
            print(RED + "  [!] Unknown parameter." + RESET)

    # Validate TCP queue resiliency
    def do_synflood(self, arg):
        args = shlex.split(arg)
        if len(args) < 2:
            print(YELLOW + "  Usage: synflood <target_ip> <port> [duration] [threads]" + RESET)
            return

        from modules.dos.syn_flood import run_syn_flood
        target_ip = args[0]
        port = int(args[1])
        duration = int(args[2]) if len(args) > 2 else 10
        threads = int(args[3]) if len(args) > 3 else 10

        run_syn_flood(target_ip, port, duration, threads)

    # Validate bandwidth throughput limits
    def do_volflood(self, arg):
        args = shlex.split(arg)
        if len(args) < 2:
            print(YELLOW + "  Usage: volflood <target_ip> <protocol> [port] [duration] [threads]" + RESET)
            return

        from modules.dos.udp_icmp_flood import run_volumetric_flood
        target_ip = args[0]
        protocol = args[1].upper()
        
        target_port = int(args[2]) if (len(args) > 2 and protocol == "UDP") else 0
        idx_offset = 1 if protocol == "UDP" else 0
        
        duration = int(args[2 + idx_offset]) if len(args) > (2 + idx_offset) else 10
        threads = int(args[3 + idx_offset]) if len(args) > (3 + idx_offset) else 5

        if protocol not in ["UDP", "ICMP"]:
            print(RED + "  [!] Supported variants: UDP or ICMP." + RESET)
            return

        run_volumetric_flood(target_ip, target_port, protocol, duration, threads, size=64)

    # Validate application thread pool persistence
    def do_slowloris(self, arg):
        args = shlex.split(arg)
        if len(args) < 2:
            print(YELLOW + "  Usage: slowloris <target_ip> <port> [connections] [interval]" + RESET)
            return

        from modules.dos.slowloris import run_slowloris
        target_ip = args[0]
        port = int(args[1])
        connections = int(args[2]) if len(args) > 2 else 100
        interval = int(args[3]) if len(args) > 3 else 15

        print(CYAN + "\n  SLOWLORIS HTTP RESILIENCY TEST" + RESET)
        print(CYAN + "  " + "-" * 40 + RESET)
        try:
            run_slowloris(target_ip, port, connections, interval)
        except KeyboardInterrupt:
            print(YELLOW + "\n  [!] Assessment terminated by operator." + RESET)

    # Execute continuous integration baseline tests
    def do_testall(self, arg):
        print(YELLOW + "\n  [*] Executing automated functional checks..." + RESET)
        os.system("python test_all.py")


def main():
    print_banner_main()
    print(DIM + "  Console interface active. Type 'help' or '?' for syntax reference. Type 'exit' to disconnect.\n" + RESET)
    
    shell = LynkeusShell()
    try:
        shell.cmdloop()
    except KeyboardInterrupt:
        print(CYAN + "\n\n  [!] Session disconnected securely." + RESET)
        sys.exit(0)


if __name__ == "__main__":
    main()
