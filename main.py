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
