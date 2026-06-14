# Banner Grabbing

## What it is
Banner grabbing is the technique of connecting to an open port and reading the first message the service sends back. This first message is called a banner and it almost always contains identifying information, the name of the software, its version number, and sometimes the operating system.

## How it works
When a service starts listening on a port, it is configured to greet incoming connections with a response. Lynkeus connects to the open port and either:

- Sends a generic newline to nudge the service into responding
- Sends an HTTP HEAD request for web-facing ports (80, 443, 8080, 8443)

The first line of whatever comes back is the banner.

## What a banner looks like
**SSH banner:**
```
SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.6
```
This tells you the SSH version (8.9p1), the OS (Ubuntu), and the patch level.

**HTTP banner:**
```
HTTP/1.1 200 OK
Server: Apache/2.4.52 (Ubuntu)
```
This tells you it is Apache version 2.4.52 running on Ubuntu.

**FTP banner:**
```
220 ProFTPD 1.3.5e Server ready
```
This tells you the FTP software and exact version.

## Why it matters in pentesting
Version numbers are gold. Once you know a service is running Apache 2.4.52 or OpenSSH 8.9, you can search for known CVEs (vulnerabilities) for that exact version. Banner grabbing turns an open port into a named, versioned target.

## Defensive awareness
From the blue team perspective, banners are information leakage. Defenders often configure services to return fake or empty banners to slow down attackers. As a blue teamer you should know your own banners, what version information your services are exposing to anyone who connects.