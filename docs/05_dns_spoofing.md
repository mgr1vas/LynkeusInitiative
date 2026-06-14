# DNS Spoofing

## What it is
DNS spoofing is an attack where you intercept a DNS query from a victim and send back a fake answer, redirecting them to an IP address you control instead of the real one. The victim types a real domain, but ends up on your machine.

## What DNS is
DNS stands for Domain Name System. It is the internet's phone book. When you type `google.com` into a browser, your computer does not know where that is, it asks a DNS server "what IP address does google.com point to?" The DNS server replies with something like `142.250.185.46` and your computer connects there.

DNS was designed in the 1980s with no authentication. A DNS reply is trusted simply because it arrives. This is what makes DNS spoofing possible.

## How it works
For DNS spoofing to work, the attacker must be positioned to intercept traffic between the victim and the DNS server. On a local network this is achieved by running ARP spoofing first, tricking the victim's machine into routing all its traffic through the attacker's machine.

Once in position, Lynkeus:
1. Sniffs all UDP traffic on port 53 (the DNS port)
2. When it sees a DNS query for a domain in the spoof list, it immediately crafts a fake DNS response
3. The fake response points the domain to the attacker's controlled IP
4. It sends the fake response back to the victim before the real DNS server can reply
5. The victim's browser connects to the attacker's machine instead

## Wildcard spoofing
Lynkeus supports wildcard spoofing with `{"*": "ip"}`.  This intercepts and redirects every single DNS query on the network regardless of domain. Every website the victim tries to visit goes to your controlled IP.

## Why it matters in pentesting
DNS spoofing is the foundation of man-in-the-middle attacks on local networks. Combined with a fake login page (credential harvesting), it becomes one of the most effective attacks in a physical or internal network pentest. You redirect the victim to your page, they enter their credentials thinking they are on the real site, you capture everything.

## Why it matters in blue teaming
Understanding DNS spoofing teaches you:
- Why DNSSEC (DNS Security Extensions) exists — it adds cryptographic signatures to DNS replies
- Why DNS-over-HTTPS (DoH) was developed — encrypts DNS queries so they cannot be intercepted
- How to detect DNS spoofing in SIEM logs — look for duplicate DNS responses or responses from unexpected sources

## Key terms
- **DNS** — Domain Name System, translates domain names to IP addresses
- **UDP port 53** — the port DNS traffic travels on
- **Query** — a request asking what IP address a domain points to
- **Response** — the answer containing the IP address
- **Man-in-the-middle (MitM)** — an attacker positioned between two communicating parties
- **DNSSEC** — an extension to DNS that uses digital signatures to verify responses are authentic