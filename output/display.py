# output/display.py
# Lynkeus — all terminal output lives here
# Nothing else in the project prints to stdout

import datetime
from output.colors import GREEN, YELLOW, CYAN, DIM, BOLD, RESET


# ASCII art banner printed at startup
LYNKEUS_ASCII = """
     echo ".____                   __                        ";
echo "|    |    ___.__. ____ |  | __ ____  __ __  ______";
echo "|    |   <   |  |/    \\|  |/ // __ \\|  |  \\/  ___/";
echo "|    |___ \\___  |   |  \\    <\\  ___/|  |  /\\___ \\ ";
echo "|_______ \\/ ____|___|  /__|_ \\\\___  >____//____  >";
echo "        \\/\\/         \\/     \\/    \\/           \\/ ";
"""

# Tagline printed below the ASCII art
TAGLINE = "  See through every wall.  |  Port Scanner + Banner Grabber"


def print_banner(target, ip, port_count):
    """
    # Prints the full Lynkeus ASCII header with scan metadata
    """

    # ASCII logo
    print (CYAN + LYNKEUS_ASCII + RESET)
    print (DIM + TAGLINE + RESET)
    print ("")
    print (CYAN + "=" * 72 + RESET)

    # Show resolved IP only if it differs from typed target
    if target != ip:
        print ("  Target  : " + BOLD + target + RESET + "  (" + ip + ")")
    else:
        print ("  Target  : " + BOLD + target + RESET)

    print ("  Ports   : " + str(port_count) + " ports queued")
    print ("  Started : " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print (CYAN + "-" * 72 + RESET)
    print ("")


def print_result(result):
    """
    # Prints a single open port result as a formatted row
    # Dims the placeholder when no banner was returned
    """

    port    = str(result["port"]).ljust(6)
    service = YELLOW + result["service"].ljust(12) + RESET

    # Dim the placeholder so real banners stand out
    if result["banner"] == "No banner":
        banner = DIM + "No banner" + RESET
    else:
        banner = result["banner"]

    print ("  " + GREEN + "OPEN" + RESET + "  " + BOLD + port + RESET + "  " + service + "  " + banner)


def print_summary(open_count, total_count):
    """
    # Prints the final scan summary line
    """

    print ("")
    print (CYAN + "-" * 72 + RESET)
    print ("  " + BOLD + "Scan complete." + RESET + "  "
           + GREEN + str(open_count) + " open port(s)" + RESET
           + " found out of " + str(total_count) + " scanned.")
    print (CYAN + "=" * 72 + RESET)
    print ("")
