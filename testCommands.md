# 1. Network Discovery & Reconnaissance
scan 127.0.0.1 21-80 50 0.5
arpscan 192.168.1.0/24 1.5

# 2. Service Access Control & Authentication Checks
sshbrute 192.168.1.100 root,admin wordlists/common_passes.txt 4 0.2
ftpbrute 192.168.1.100 anonymous,user wordlists/ftp_passes.txt 2 1.0
httpbrute http://192.168.1.100/login admin wordlists/http_passes.txt 5 0.0

# 3. Network Infrastructure Testing
dnsspoof 192.168.1.20 eth0 25
craft syn 192.168.1.1 443
craft icmp 192.168.1.1 SYSTEM_CHECK
craft udp 192.168.1.1 53

# 4. Traffic & Signature Obfuscation
stealthscan 192.168.1.50 80,443,8080 2 1.5 4.0
ttlspoof 192.168.1.1 80 windows
useragent random
useragent showall
useragent count

# 5. Service & State Exhaustion Resilience Tests
synflood 192.168.1.200 80 15 20
volflood 192.168.1.200 UDP 53 10 10
volflood 192.168.1.200 ICMP 0 10 5
slowloris 192.168.1.200 80 150 10

# 6. Global Automation Check
testall
