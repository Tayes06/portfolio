import numpy as np
import pandas as pd
from typing import List, Dict, Any
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

SAMPLE_TRANSACTIONS = [
    {"amount": 35.50, "merchant": "Amazon", "category": "Shopping", "hour": 14, "day_of_week": 3, "distance_from_home": 2.1, "is_anomaly": False},
    {"amount": 4200.00, "merchant": "Unknown", "category": "Transfer", "hour": 3, "day_of_week": 6, "distance_from_home": 850.0, "is_anomaly": True},
    {"amount": 12.99, "merchant": "Netflix", "category": "Entertainment", "hour": 20, "day_of_week": 1, "distance_from_home": 0.0, "is_anomaly": False},
    {"amount": 89.40, "merchant": "Walmart", "category": "Groceries", "hour": 11, "day_of_week": 0, "distance_from_home": 3.5, "is_anomaly": False},
    {"amount": 15000.00, "merchant": "CryptoExchange", "category": "Investment", "hour": 1, "day_of_week": 5, "distance_from_home": 1200.0, "is_anomaly": True},
    {"amount": 65.00, "merchant": "Uber", "category": "Transport", "hour": 22, "day_of_week": 4, "distance_from_home": 8.0, "is_anomaly": False},
    {"amount": 250.00, "merchant": "BestBuy", "category": "Electronics", "hour": 15, "day_of_week": 2, "distance_from_home": 5.0, "is_anomaly": False},
    {"amount": 9800.00, "merchant": "ForeignBank", "category": "Wire Transfer", "hour": 4, "day_of_week": 7, "distance_from_home": 3200.0, "is_anomaly": True},
    {"amount": 7.50, "merchant": "Starbucks", "category": "Food", "hour": 8, "day_of_week": 1, "distance_from_home": 1.2, "is_anomaly": False},
    {"amount": 550.00, "merchant": "Macy's", "category": "Shopping", "hour": 13, "day_of_week": 0, "distance_from_home": 4.0, "is_anomaly": False},
    {"amount": 22300.00, "merchant": "OffshoreAccount", "category": "Transfer", "hour": 2, "day_of_week": 6, "distance_from_home": 5000.0, "is_anomaly": True},
    {"amount": 45.00, "merchant": "Shell", "category": "Gas", "hour": 17, "day_of_week": 2, "distance_from_home": 2.5, "is_anomaly": False},
    {"amount": 175.00, "merchant": "DeltaAir", "category": "Travel", "hour": 9, "day_of_week": 4, "distance_from_home": 45.0, "is_anomaly": False},
    {"amount": 6200.00, "merchant": "UnknownATM", "category": "Withdrawal", "hour": 23, "day_of_week": 5, "distance_from_home": 680.0, "is_anomaly": True},
    {"amount": 28.50, "merchant": "Dominos", "category": "Food", "hour": 19, "day_of_week": 6, "distance_from_home": 0.8, "is_anomaly": False},
]

FEATURES = ["amount", "hour", "day_of_week", "distance_from_home"]


class AnomalyDetectionService:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self._fitted = False

    def _prepare_data(self, transactions: List[Dict]) -> np.ndarray:
        df = pd.DataFrame(transactions)
        X = df[FEATURES].values
        return X

    def fit(self):
        X = self._prepare_data(SAMPLE_TRANSACTIONS)
        X_scaled = self.scaler.fit_transform(X)
        self.model = IsolationForest(contamination=0.2, random_state=42, n_estimators=100)
        self.model.fit(X_scaled)
        self._fitted = True

    def predict(self, transaction: Dict) -> Dict[str, Any]:
        if not self._fitted:
            self.fit()
        df = pd.DataFrame([transaction])
        X = df[FEATURES].values
        X_scaled = self.scaler.transform(X)
        pred = self.model.predict(X_scaled)[0]
        score = self.model.decision_function(X_scaled)[0]
        anomaly_score = float(2.0 / (1.0 + np.exp(-score)) - 1.0)
        return {
            "is_anomaly": bool(pred == -1),
            "anomaly_score": round(anomaly_score, 4),
            "confidence": round(abs(anomaly_score), 4),
        }

    def get_all_predictions(self) -> List[Dict]:
        if not self._fitted:
            self.fit()
        results = []
        for tx in SAMPLE_TRANSACTIONS:
            result = self.predict(tx)
            results.append({**tx, **result})
        return results

    def get_statistics(self) -> Dict:
        if not self._fitted:
            self.fit()
        results = self.get_all_predictions()
        df = pd.DataFrame(results)
        total = len(df)
        anomalies = df[df["is_anomaly"] == True].shape[0]
        normal = total - anomalies
        total_amount = df["amount"].sum()
        anomaly_amount = df[df["is_anomaly"] == True]["amount"].sum()
        return {
            "total_transactions": total,
            "anomalies_detected": int(anomalies),
            "normal_transactions": int(normal),
            "anomaly_rate": round(anomalies / total * 100, 2) if total else 0,
            "total_amount": round(total_amount, 2),
            "anomaly_amount": round(anomaly_amount, 2),
            "anomaly_percent_amount": round(anomaly_amount / total_amount * 100, 2) if total_amount else 0,
        }


anomaly_service = AnomalyDetectionService()
