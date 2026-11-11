import argparse
from pathlib import Path
import requests
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.dummy import DummyClassifier

API = "https://api.spacexdata.com/v4/launches/query"

def fetch_launches():
    response = requests.post(API, json={"query": {}, "options": {"pagination": False, "populate": ["rocket", "payloads", "launchpad", "cores.core"]}}, timeout=60)
    response.raise_for_status()
    return response.json()["docs"]

def build_table(docs):
    rows = []
    for launch in docs:
        for core in launch.get("cores", []):
            outcome = core.get("landing_success")
            if outcome is None:
                continue
            payloads = [p for p in launch.get("payloads", []) if isinstance(p, dict)]
            masses = [p.get("mass_kg") for p in payloads if p.get("mass_kg") is not None]
            site = launch.get("launchpad") or {}
            rocket = launch.get("rocket") or {}
            rows.append({"success": int(bool(outcome)), "launch_site": site.get("name"), "orbit": ",".join(sorted({p.get("orbit", "unknown") for p in payloads})), "payload_mass_kg": sum(masses) if masses else None, "flight_number": launch.get("flight_number"), "reuse_count": core.get("flight"), "booster": rocket.get("name")})
    return pd.DataFrame(rows).drop_duplicates()

def evaluate(df):
    y = df.pop("success")
    X = df.drop(columns=["booster"], errors="ignore")
    categorical = X.select_dtypes(include="object").columns.tolist()
    numeric = X.select_dtypes(exclude="object").columns.tolist()
    prep = ColumnTransformer([("num", Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric), ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))]), categorical)])
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    models = {"baseline": DummyClassifier(strategy="most_frequent"), "logistic_regression": LogisticRegression(max_iter=2000, class_weight="balanced"), "random_forest": RandomForestClassifier(n_estimators=300, min_samples_leaf=2, class_weight="balanced", random_state=42)}
    scoring = {"accuracy": "accuracy", "precision": "precision", "recall": "recall", "f1": "f1", "roc_auc": "roc_auc"}
    for name, estimator in models.items():
        result = cross_validate(Pipeline([("prep", prep), ("model", estimator)]), X, y, cv=cv, scoring=scoring, error_score="raise")
        print(name, {metric: round(result[f"test_{metric}"].mean(), 3) for metric in scoring})
    print("Rows:", len(X), "Positive rate:", round(y.mean(), 3))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="reports/spacex")
    args = parser.parse_args()
    table = build_table(fetch_launches())
    if len(table) < 25 or table.success.nunique() < 2:
        raise SystemExit("Not enough labeled launches for a meaningful stratified comparison.")
    out = Path(args.output); out.mkdir(parents=True, exist_ok=True)
    table.to_csv(out / "launches_clean.csv", index=False)
    evaluate(table.copy())

if __name__ == "__main__": main()
