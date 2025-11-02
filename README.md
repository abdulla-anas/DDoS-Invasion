# DDoS-Invasion

**The characteristics of DDoS attack, i.e., having different appearance with different
scenarios, make it difficult to detect. This paper will review and analyze different
existing DDoS detecting techniques against different parameters, discusses
their advantage and disadvantages, and propose a hybrid statistical model that
could significantly mitigate these attacks and be a better alternative solution for
current detection problems, hence the Evaluaion of DDoS came ahead.**



It is an academic mini project

How to run (short):

***Create a virtualenv and install deps:***
    $python -m venv venv
    $source venv/bin/activate
    $pip install -r requirements.txt

***Generate synthetic dataset:***
    $python scripts/generate_synthetic_data.py --out data/ddos_synthetic.csv

***Train model:***
    $python scripts/train_model.py --data data/ddos_synthetic.csv --output models/

***Evaluate:***
    $python scripts/evaluate_model.py --model models/rf_model.pkl --scaler models/scaler.pkl --data data/ddos_synthetic.csv

***Run simulated realtime monitor:***
    $python scripts/realtime_monitor.py --model models/rf_model.pkl --scaler models/scaler.pkl --duration 60


--------------------------------------------------------------------------------------------------
Replace the synthetic CSV with a real labeled dataset (CICIDS, NSL-KDD) for better realism. Ensure columns match DEFAULT_FEATURES or adapt data_prep.py.

Replace RandomForest with a sequential model (LSTM) for flow-sequence detection and/or gradient-boosting (XGBoost) for higher performance.
