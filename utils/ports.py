# utils/ports.py
# Lynkeus — port argument parser
# Turns the -p flag into a clean list of integers

def parse_ports(port_arg):
    """
    # Accepts three formats:
    #   Single port  →  '80'
    #   Range        →  '1-1024'
    #   Comma list   →  '22,80,443'
    #   Mixed        →  '22,80,1000-1010'
    # Returns a sorted, deduplicated list of integers
    """

    ports = []

    for part in port_arg.split(","):
        part = part.strip()

        # Handle range like '1-1024'
        if "-" in part:
            start, end = part.split("-", 1)
            ports.extend(range(int(start), int(end) + 1))

        # Handle single port like '80'
        else:
            ports.append(int(part))

    # Deduplicate and sort before returning
    return sorted(set(ports))
