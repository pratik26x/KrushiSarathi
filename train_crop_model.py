"""
KrushiSarathi — train RandomForest crop classifier from Crop_data.csv and save crop_recommendation_model.pkl.
Feature order matches app.py: N, P, K, temperature, humidity, ph, rainfall.
"""
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "Crop_data.csv"
MODEL_PATH = ROOT / "crop_recommendation_model.pkl"

FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
TARGET = "crop"


def main():
    df = pd.read_csv(CSV_PATH)
    missing = [c for c in FEATURES + [TARGET] if c not in df.columns]
    if missing:
        raise SystemExit(f"CSV missing columns: {missing}")

    X = df[FEATURES].to_numpy()
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    acc = accuracy_score(y_test, clf.predict(X_test))
    print(f"Hold-out accuracy (20% stratified): {acc:.4f}")

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    print(f"Saved model ({len(y)} samples, {y.nunique()} classes) -> {MODEL_PATH}")


if __name__ == "__main__":
    main()
