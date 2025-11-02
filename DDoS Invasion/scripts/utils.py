#!/usr/bin/env python3
"""
utils.py
Helpers for feature extraction for simulated requests.
"""
import random
import time
import numpy as np

def generate_request_from_ip(ip, attack=False, seed=None):
    """
    Generate a request event dict with features approximating a flow snapshot.
    attack: if True, features mimic an attack request/flow
    """
    rng = np.random.RandomState(seed)
    if not attack:
        packet_rate = float(rng.normal(loc=20, scale=5).clip(1))
        byte_rate = float(rng.normal(loc=2000, scale=800).clip(100))
        avg_pkt_size = float(rng.normal(loc=100, scale=20).clip(40))
        flow_duration = float(rng.exponential(scale=10).clip(0.1, 300))
        src_ip_entropy = float(rng.normal(loc=0.3, scale=0.1).clip(0,1))
        syn_ratio = float(rng.normal(loc=0.05, scale=0.02).clip(0,1))
        distinct_dst_ports = int(rng.poisson(lam=2))
        concurrent_connections = int(rng.poisson(lam=3))
    else:
        packet_rate = float(rng.normal(loc=800, scale=300).clip(10))
        byte_rate = float(rng.normal(loc=200000, scale=100000).clip(1000))
        avg_pkt_size = float(rng.normal(loc=150, scale=30).clip(40))
        flow_duration = float(rng.exponential(scale=2).clip(0.01, 300))
        src_ip_entropy = float(rng.normal(loc=0.9, scale=0.15).clip(0,1))
        syn_ratio = float(rng.normal(loc=0.6, scale=0.25).clip(0,1))
        distinct_dst_ports = int(rng.poisson(lam=1))
        concurrent_connections = int(rng.poisson(lam=200))

    return {
        "packet_rate": packet_rate,
        "byte_rate": byte_rate,
        "avg_pkt_size": avg_pkt_size,
        "flow_duration": flow_duration,
        "src_ip_entropy": src_ip_entropy,
        "syn_ratio": syn_ratio,
        "distinct_dst_ports": distinct_dst_ports,
        "concurrent_connections": concurrent_connections,
        "src_ip": ip,
        "timestamp": time.time()
    }
