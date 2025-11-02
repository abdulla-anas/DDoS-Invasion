#!/usr/bin/env python3
"""
realtime_monitor.py
Simulate realtime event stream, classify each event using trained model,
and apply mitigation (rate limiting / IP blocking).
"""
import argparse
import time
import random
import joblib
import numpy as np
from mitigation import Mitigator
from utils import generate_request_from_ip
from collections import defaultdict

FEATURE_ORDER = ["packet_rate","byte_rate","avg_pkt_size","flow_duration","src_ip_entropy","syn_ratio","distinct_dst_ports","concurrent_connections"]

def ip_pool(num_legit=200, num_bots=100, seed=42):
    rng = random.Random(seed)
    legit = [f"10.0.0.{i+1}" for i in range(num_legit)]
    bots = [f"172.16.0.{i+1}" for i in range(num_bots)]
    return legit, bots

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="models/rf_model.pkl")
    parser.add_argument("--scaler", default="models/scaler.pkl")
    parser.add_argument("--duration", type=int, default=60, help="Simulate for N seconds")
    parser.add_argument("--attack-chance", type=float, default=0.02, help="Chance that an event is attack-like")
    args = parser.parse_args()

    clf = joblib.load(args.model)
    scaler = joblib.load(args.scaler)
    mitigator = Mitigator(block_window_seconds=120, max_requests_per_window=150, window_seconds=10)

    legit, bots = ip_pool()
    start = time.time()
    stats = defaultdict(int)

    print("Starting simulated realtime monitor. Ctrl-C to stop.")
    try:
        while time.time() - start < args.duration:
            # Simulate a burst of requests per second
            events_this_sec = random.randint(50, 300)
            for _ in range(events_this_sec):
                # Choose whether this event comes from botnet or legit
                if random.random() < args.attack_chance:
                    # Attack event: pick bot IP more likely
                    ip = random.choice(bots)
                    e = generate_request_from_ip(ip, attack=True)
                else:
                    ip = random.choice(legit)
                    e = generate_request_from_ip(ip, attack=False)
                    # small chance legitimate IP gets compromised and attacks briefly
                    if random.random() < 0.001:
                        e = generate_request_from_ip(ip, attack=True)

                # Mitigator check by IP first
                allowed = mitigator.register_request(e["src_ip"])
                if not allowed:
                    stats["blocked_by_rate_limit"] += 1
                    continue

                # Build feature vector and classify
                x = np.array([e[f] for f in FEATURE_ORDER]).reshape(1, -1)
                x_scaled = scaler.transform(x)
                pred = clf.predict(x_scaled)[0]  # 0 normal, 1 ddos

                if pred == 1:
                    # trigger mitigation: block IP for a while
                    mitigator.force_block(e["src_ip"], duration=60)
                    stats["detected_and_blocked"] += 1
                else:
                    stats["allowed"] += 1

            # print periodic stats
            print(f"[t={int(time.time()-start)}s] allowed={stats['allowed']} detected_blocked={stats['detected_and_blocked']} rate_limited={stats['blocked_by_rate_limit']}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped by user.")

    print("Final stats:", dict(stats))

if __name__ == "__main__":
    main()
