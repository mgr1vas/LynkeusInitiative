# ─────────────────────────────────────────────
# reports/json_report.py
# Lynkeus — JSON report writer
# Saves everything Lynkeus found to a structured file
# ─────────────────────────────────────────────

import json
import datetime
from output.colors import CYAN, BOLD, RESET


def save_report(target, ip, results, output_file):
    """
    # Builds a structured report dict and writes it to JSON
    # Includes target, resolved IP, timestamp, and all open ports
    """

    # ── Build the report structure ───────────────────────────────
    report = {
        "tool":         "Lynkeus — See through every wall.",
        "scan_target":  target,
        "resolved_ip":  ip,
        "timestamp":    datetime.datetime.now().isoformat(),
        "total_open":   len(results),
        "open_ports":   results,
    }

    # ── Write to file with readable indentation ──────────────────
    with open(output_file, "w") as f:
        json.dump(report, f, indent=2)

    print (CYAN + "[*] Lynkeus report saved to: " + BOLD + output_file + RESET)
