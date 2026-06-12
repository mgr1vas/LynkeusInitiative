# ─────────────────────────────────────────────
# core/scanner.py
# Lynkeus — concurrent scan orchestration
# Spawns threads and collects open port results
# ─────────────────────────────────────────────

import concurrent.futures
from core.probe import scan_port
from output.display import print_result


def run_scan(ip, ports, timeout, workers):
    """
    # Launches a thread pool and scans all ports concurrently
    # Returns a sorted list of open port result dicts
    """

    open_ports = []

    # ── Spin up thread pool with the given worker count ──────────
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:

        # ── Submit one scan_port task per port ───────────────────
        futures = {
            executor.submit(scan_port, ip, port, timeout): port
            for port in ports
        }

        # ── Collect results as each thread finishes ──────────────
        for future in concurrent.futures.as_completed(futures):
            result = future.result()

            # ── Only keep open ports ─────────────────────────────
            if result:
                open_ports.append(result)
                print_result(result)

    # ── Sort by port number before returning ─────────────────────
    open_ports.sort(key=lambda x: x["port"])

    return open_ports
