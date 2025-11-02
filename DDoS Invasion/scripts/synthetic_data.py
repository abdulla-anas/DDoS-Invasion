#!/usr/bin/env python3
"""
generate_synthetic_data.py
Generates a synthetic dataset for DDoS detection.
Output CSV has features and a `label` column: 0 = normal, 1 = ddos
"""
import argparse
import numpy as np
import pandas as pd
from tqdm import tqdm
import os

def generate_samples(n_normal=5000, n_ddos=5000, seed=42):
    rng = np.random.RandomState(seed)

    # Features (illustrative; choose features commonly used in flow analysis)
    # - packet_rate: packets per second
    # - byte_rate: bytes per second
    # - avg_pkt_size: average packet size
    # - flow_duration: seconds
    # - src_ip_entropy: entropy of source IPs seen (0..1)
    # - syn_ratio: fraction of packets with SYN flag (0..1)
    # - distinct_dst_ports: number of distinct dst ports observed in flow
    # - concurrent_connections: number of simultaneous connections

    # Normal traffic distribution
    normal = pd.DataFrame({
        "packet_rate": rng.normal(loc=20, scale=5, size=n_normal).clip(1),
        "byte_rate": rng.normal(loc=2000, scale=800, size=n_normal).clip(100),
        "avg_pkt_size": rng.normal(loc=100, scale=20, size=n_normal).clip(40),
        "flow_duration": rng.exponential(scale=10, size=n_normal).clip(0.1, 300),
        "src_ip_entropy": rng.normal(loc=0.3, scale=0.1, size=n_normal).clip(0,1),
        "syn_ratio": rng.normal(loc=0.05, scale=0.02, size=n_normal).clip(0,1),
        "distinct_dst_ports": rng.poisson(lam=2, size=n_normal),
        "concurrent_connections": rng.poisson(lam=3, size=n_normal),
        "label": 0
    })

    # DDoS traffic distribution (higher packet rates, high byte rates, high syn ratio for SYN floods etc.)
    ddos = pd.DataFrame({
        "packet_rate": rng.normal(loc=800, scale=300, size=n_ddos).clip(10),
        "byte_rate": rng.normal(loc=200000, scale=100000, size=n_ddos).clip(1000),
        "avg_pkt_size": rng.normal(loc=150, scale=30, size=n_ddos).clip(40),
        "flow_duration": rng.exponential(scale=2, size=n_ddos).clip(0.01, 300),
        "src_ip_entropy": rng.normal(loc=0.9, scale=0.15, size=n_ddos).clip(0,1),
        "syn_ratio": rng.normal(loc=0.6, scale=0.25, size=n_ddos).clip(0,1),
        "distinct_dst_ports": rng.poisson(lam=1, size=n_ddos),
        "concurrent_connections": rng.poisson(lam=200, size=n_ddos),
        "label": 1
    })

    df = pd.concat([normal, ddos], ignore_index=True).sample(frac=1, random_state=seed).reset_index(drop=True)
    return df

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="data/ddos_synthetic.csv")
    parser.add_argument("--n-normal", type=int, default=5000)
    parser.add_argument("--n-ddos", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    df = generate_samples(n_normal=args.n_normal, n_ddos=args.n_ddos, seed=args.seed)
    df.to_csv(args.out, index=False)
    print(f"Wrote {len(df)} rows to {args.out}")

if __name__ == "__main__":
    main()
