#!/usr/bin/env python3
# Benign UDP client for controlled testing.
import socket
import ipaddress
import time

def is_private_or_local(ip_str):
    ip = ipaddress.ip_address(ip_str)
    return ip.is_private or ip.is_loopback

TARGET = "192.168.8.53"   # change only to private/local IPs you control
PORT = 9999
PACKET_COUNT = 5000000      # small number for testing
DELAY_SEC = 0 # 0.05       # delay between packets

if not is_private_or_local(TARGET):
    raise SystemExit("Refusing to send traffic to public IPs. Use localhost or a private IP you control.")

message = b"test-packet-" + b"x" * 1000  # ~112 bytes

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.settimeout(1.0)
    print(f"Sending {PACKET_COUNT} packets to {TARGET}:{PORT} (safe testing)")
    for i in range(PACKET_COUNT):
        s.sendto(message, (TARGET, PORT))
        # try:
        #     data, addr = s.recvfrom(4096)
        #     print(f"{i+1}/{PACKET_COUNT} got reply: {data[:100]!r}")
        # except socket.timeout:
        #     print(f"{i+1}/{PACKET_COUNT} no reply (timeout)")
        #time.sleep(DELAY_SEC)
    print("Finished")
