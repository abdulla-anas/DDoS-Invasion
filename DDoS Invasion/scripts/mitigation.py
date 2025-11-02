#!/usr/bin/env python3
"""
mitigation.py
Simple in-memory mitigation utilities.
"""
import time
from collections import defaultdict, deque

class Mitigator:
    def __init__(self, block_window_seconds=300, max_requests_per_window=100, window_seconds=60):
        # block_window_seconds: how long to block an IP when flagged
        self.block_window_seconds = block_window_seconds
        self.max_requests_per_window = max_requests_per_window
        self.window_seconds = window_seconds

        self.request_logs = defaultdict(deque)  # ip -> deque of timestamps
        self.blocked_ips = {}  # ip -> unblock_time

    def is_blocked(self, ip):
        now = time.time()
        # Cleanup expired blocks
        expired = [ip_ for ip_, t in self.blocked_ips.items() if t <= now]
        for ip_ in expired:
            del self.blocked_ips[ip_]
        return ip in self.blocked_ips

    def register_request(self, ip):
        """Register a request from ip; return True if allowed, False if blocked"""
        now = time.time()
        if self.is_blocked(ip):
            return False

        q = self.request_logs[ip]
        q.append(now)

        # Remove old timestamps outside window
        cutoff = now - self.window_seconds
        while q and q[0] < cutoff:
            q.popleft()

        if len(q) > self.max_requests_per_window:
            # Block the IP temporarily
            self.blocked_ips[ip] = now + self.block_window_seconds
            # clear request log to save memory
            del self.request_logs[ip]
            return False
        return True

    def force_block(self, ip, duration=None):
        now = time.time()
        self.blocked_ips[ip] = now + (duration or self.block_window_seconds)

    def unblock(self, ip):
        if ip in self.blocked_ips:
            del self.blocked_ips[ip]
