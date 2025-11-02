#!/usr/bin/env python3
"""
data_prep.py
Helpers for loading and preprocessing the CSV dataset.
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

DEFAULT_FEATURES = [
    "packet_rate",
    "byte_rate",
    "avg_pkt_size",
    "flow_duration",
    "src_ip_entropy",
    "syn_ratio",
    "distinct_dst_ports",
    "concurrent_connections",
]

def load_dataset(path):
    df = pd.read_csv(path)
    # Basic sanitization: ensure expected columns exist
    missing = [c for c in DEFAULT_FEATURES + ["label"] if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in dataset: {missing}")
    return df

def prepare_train_test(df, test_size=0.2, random_state=42):
    X = df[DEFAULT_FEATURES].fillna(0.0).values
    y = df["label"].astype(int).values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, stratify=y, random_state=random_state)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler
