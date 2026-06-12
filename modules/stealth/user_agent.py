#!/usr/bin/env python3

# modules/stealth/user_agent.py
# Lynkeus Initiative — User Agent Rotator
# Cycles through real browser identities on HTTP requests
# Prevents web servers from fingerprinting your scanner

import random


#  Pool of real browser user agent strings 
USER_AGENTS = [
    # Chrome on Windows 
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",

    # Firefox on Windows 
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",

    # Chrome on Linux 
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",

    # Firefox on Linux 
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",

    # Safari on macOS 
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",

    # Edge on Windows 
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",

    # Chrome on Android 
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.82 Mobile Safari/537.36",

    # Safari on iPhone 
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1",
]


def get_random_agent():
    """
    # Returns a randomly selected user agent string
    # Call this before every HTTP request to rotate identity
    """

    return random.choice(USER_AGENTS)


def get_all_agents():
    """
    # Returns the full list of available user agent strings
    """

    return USER_AGENTS


def get_agent_count():
    """
    # Returns the number of user agents in the pool
    """

    return len(USER_AGENTS)
