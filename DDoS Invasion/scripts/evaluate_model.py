#!/usr/bin/env python3
"""
evaluate_model.py
Load a saved model and evaluate on a CSV dataset (full or test split).
"""
import argparse
import joblib
import os
from data_prep import load_dataset, prepare_train_test
from sklearn.metrics import classification_report, confusion_matrix

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, help="Path to model .pkl")
    parser.add_argument("--scaler", required=True, help="Path to scaler .pkl")
    parser.add_argument("--data", required=True, help="CSV path for evaluation")
    args = parser.parse_args()

    if not os.path.exists(args.model) or not os.path.exists(args.scaler):
        raise FileNotFoundError("Model or scaler file not found")

    clf = joblib.load(args.model)
    scaler = joblib.load(args.scaler)
    df = load_dataset(args.data)
    X_train, X_test, y_train, y_test, _ = prepare_train_test(df)

    # We got X_test from prepare_train_test already scaled by a new scaler; we need to rescale using loaded scaler.
    # So recompute with no scaler fit:
    features = df.drop(columns=["label"]).copy() if "label" in df.columns else df
    # But simpler: recompute X_test via splitting with same function and then re-scale using loaded scaler
    from sklearn.model_selection import train_test_split
    X = df[[c for c in features.columns if c != "label"]] if "label" in df.columns else df
    X = df[[col for col in ["packet_rate","byte_rate","avg_pkt_size","flow_duration","src_ip_entropy","syn_ratio","distinct_dst_ports","concurrent_connections"]]].fillna(0.0).values
    y = df["label"].astype(int).values
    _, X_test_raw, _, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    X_test_scaled = scaler.transform(X_test_raw)

    y_pred = clf.predict(X_test_scaled)
    print("Classification report:")
    print(classification_report(y_test, y_pred, digits=4))
    print("Confusion matrix:")
    print(confusion_matrix(y_test, y_pred))

if __name__ == "__main__":
    main()
