# core/probe.py
# Lynkeus — low-level TCP probe + banner grab
# The eye that looks through the wall

import socket
from utils.port_names import PORT_NAMES


def scan_port(ip, port, timeout):
    """
    # Attempts a TCP connection to the target port
    # Returns a result dict if open, None if closed or filtered
    """

    try:
        # Attempt TCP handshake
        with socket.create_connection((ip, port), timeout=timeout):
            pass

        # Port is open — identify service and grab banner
        banner  = grab_banner(ip, port, timeout)
        service = PORT_NAMES.get(port, "Unknown")

        return {
            "port":    port,
            "state":   "open",
            "service": service,
            "banner":  banner,
        }

    except (ConnectionRefusedError, socket.timeout, OSError):
        # Port is closed or filtered — nothing to report
        return None


def grab_banner(ip, port, timeout):
    """
    # Reconnects to an open port and reads the first response line
    # Sends an HTTP HEAD request for web ports, newline for all others
    """

    try:
        with socket.create_connection((ip, port), timeout=timeout) as s:
            s.settimeout(timeout)

            # HTTP probe for web-facing ports
            if port in (80, 443, 8080, 8443):
                s.sendall(b"HEAD / HTTP/1.0\r\nHost: target\r\n\r\n")
            else:
                # Generic nudge — lets the service speak first
                s.sendall(b"\r\n")

            # Decode the response and return the first line
            raw    = s.recv(1024).decode("utf-8", errors="ignore").strip()
            banner = raw.split("\n")[0][:120]

            return banner if banner else "No banner"

    except Exception:
        return "No banner"
