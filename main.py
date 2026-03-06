"""Credit scoring pipeline for UCI Credit Card dataset.

Run:
    python main.py
"""

from __future__ import annotations

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.model_selection import train_test_split


DATA_PATH = "UCI_Credit_Card.csv"
RANDOM_STATE = 42


def load_and_prepare_data(path: str) -> tuple[pd.DataFrame, pd.Series]:
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    df = df.rename(columns={"default payment next month": "default"})

    if "default" not in df.columns:
        raise ValueError("Target column 'default payment next month' was not found in the dataset.")

    cat_features = ["SEX", "EDUCATION", "MARRIAGE"]
    df[cat_features] = df[cat_features].astype(str)
    df = pd.get_dummies(df, columns=cat_features, drop_first=True)

    bill_cols = [f"BILL_AMT{i}" for i in range(1, 7)]
    pay_cols = [f"PAY_AMT{i}" for i in range(1, 7)]

    df["avg_bill_amt"] = df[bill_cols].mean(axis=1)
    df["avg_pay_amt"] = df[pay_cols].mean(axis=1)
    df["pay_ratio"] = df["avg_pay_amt"] / (df["avg_bill_amt"] + 1e-5)

    y = df["default"]
    drop_columns = [col for col in ["ID", "default"] if col in df.columns]
    X = df.drop(columns=drop_columns)
    return X, y


def risk_category(score: float) -> str:
    if score <= 300:
        return "High Risk"
    if score <= 450:
        return "Medium Risk"
    return "Low Risk"


def main() -> None:
    X, y = load_and_prepare_data(DATA_PATH)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=RANDOM_STATE,
    )

    clf = RandomForestClassifier(
        n_estimators=200,
        random_state=RANDOM_STATE,
        class_weight="balanced",
    )
    clf.fit(X_train, y_train)

    y_pred_proba = clf.predict_proba(X_test)[:, 1]
    y_pred = clf.predict(X_test)

    print(f"ROC-AUC: {roc_auc_score(y_test, y_pred_proba):.4f}")
    print(classification_report(y_test, y_pred))
    print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))

    result = X_test.copy()
    result["PD"] = y_pred_proba
    result["Credit_Score"] = (600 - result["PD"] * 300).round().astype(int)
    result["Risk_Category"] = result["Credit_Score"].apply(risk_category)

    print("\nSample predictions:")
    print(result[["PD", "Credit_Score", "Risk_Category"]].head())

    print("\nRisk distribution:")
    print(result["Risk_Category"].value_counts())


if __name__ == "__main__":
    main()
