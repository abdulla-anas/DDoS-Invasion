#!/usr/bin/env python3
"""
train_model.py
Trains a RandomForest classifier on the dataset and saves the model + scaler.
"""
import argparse
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from data_prep import load_dataset, prepare_train_test

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="CSV dataset path")
    parser.add_argument("--output", default="models/", help="Output directory for model and scaler")
    parser.add_argument("--n-estimators", type=int, default=200)
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    print("Loading dataset...")
    df = load_dataset(args.data)
    X_train, X_test, y_train, y_test, scaler = prepare_train_test(df)

    print("Training RandomForest...")
    clf = RandomForestClassifier(n_estimators=args.n_estimators, random_state=42, n_jobs=-1)
    clf.fit(X_train, y_train)

    print("Evaluating on test set...")
    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred, digits=4))

    model_path = os.path.join(args.output, "rf_model.pkl")
    scaler_path = os.path.join(args.output, "scaler.pkl")
    joblib.dump(clf, model_path)
    joblib.dump(scaler, scaler_path)
    print(f"Saved model to {model_path} and scaler to {scaler_path}")

if __name__ == "__main__":
    main()
