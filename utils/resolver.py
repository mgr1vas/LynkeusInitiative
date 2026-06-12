# utils/resolver.py
# Lynkeus — hostname to IP resolution
# Before Lynkeus can look, he needs to know where to look

import socket
import sys


def resolve_target(target):
    """
    # Converts a hostname to its IPv4 address
    # Exits cleanly with an error if DNS resolution fails
    """

    try:
        ip = socket.gethostbyname(target)
        return ip

    except socket.gaierror:
        # ── Cannot resolve — exit with a clean message ───────────
        print ("[!] Lynkeus could not resolve host: " + target)
        sys.exit(1)
