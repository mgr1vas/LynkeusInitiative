#!/usr/bin/env python3

# ─────────────────────────────────────────────
# modules/stealth/stealth_scan.py
# Lynkeus Initiative — Stealth Scan Engine
# Wraps the core scanner with timing randomisation
# and decoy techniques to reduce IDS detection
# Lab use only — run against machines you own
# ─────────────────────────────────────────────

import random
import time
import socket
import concurrent.futures

from utils.port_names import PORT_NAMES
from output.colors import GREEN, YELLOW, CYAN, DIM, BOLD, RESET


def stealth_probe(ip, port, timeout, min_delay, max_delay):
    """
    # Scans a single port with a randomised delay before connecting
    # Randomised timing breaks regular scan interval signatures
    # that IDS tools like Snort use to detect port scans
    """

    # ── Random sleep before each probe ───────────────────────────
    jitter = random.uniform(min_delay, max_delay)
    time.sleep(jitter)

    try:
        # ── Attempt TCP connection ────────────────────────────────
        with socket.create_connection((ip, port), timeout=timeout):
            pass

        service = PORT_NAMES.get(port, "Unknown")

        return {
            "port":    port,
            "state":   "open",
            "service": service,
            "jitter":  round(jitter, 3),
        }

    except (ConnectionRefusedError, socket.timeout, OSError):
        return None


def randomise_ports(ports):
    """
    # Shuffles the port list so scans don't run in sequential order
    # Sequential port scanning is one of the easiest IDS signatures to detect
    """

    shuffled = list(ports)
    random.shuffle(shuffled)
    return shuffled


def run_stealth_scan(ip, ports, timeout, workers, min_delay, max_delay):
    """
    # Full stealth scan — randomised order + jittered timing
    # Lower worker count and higher delays = harder to detect
    # Returns sorted list of open port result dicts
    """

    print ("")
    print (CYAN + "=" * 55 + RESET)
    print (BOLD + "  STEALTH SCAN ENGINE" + RESET)
    print (CYAN + "=" * 55 + RESET)
    print ("  Target     : " + BOLD + ip + RESET)
    print ("  Ports      : " + str(len(ports)) + " queued")
    print ("  Jitter     : " + str(min_delay) + "s – " + str(max_delay) + "s per probe")
    print ("  Workers    : " + str(workers))
    print (DIM + "  Scan order randomised. Timing obfuscated." + RESET)
    print (CYAN + "-" * 55 + RESET)
    print ("")

    # ── Shuffle port order to avoid sequential scan detection ─────
    randomised_ports = randomise_ports(ports)

    open_ports = []

    # ── Lower thread count recommended for stealth ────────────────
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:

        futures = {
            executor.submit(
                stealth_probe, ip, port, timeout, min_delay, max_delay
            ): port
            for port in randomised_ports
        }

        for future in concurrent.futures.as_completed(futures):
            result = future.result()

            if result:
                open_ports.append(result)

                # ── Print open port with jitter info ──────────────
                port_col    = BOLD + str(result["port"]).ljust(6) + RESET
                service_col = YELLOW + result["service"].ljust(12) + RESET
                jitter_col  = DIM + "(+" + str(result["jitter"]) + "s)" + RESET

                print ("  " + GREEN + "OPEN" + RESET + "  " + port_col + "  " + service_col + "  " + jitter_col)

    # ── Sort by port number ───────────────────────────────────────
    open_ports.sort(key=lambda x: x["port"])

    print ("")
    print (CYAN + "-" * 55 + RESET)
    print ("  " + BOLD + "Stealth scan complete." + RESET + "  " + GREEN + str(len(open_ports)) + " open port(s)" + RESET + " found.")
    print (CYAN + "=" * 55 + RESET)
    print ("")

    return open_ports
