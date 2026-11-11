import argparse
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import HistGradientBoostingClassifier

def main():
    p=argparse.ArgumentParser(); p.add_argument("csv"); p.add_argument("--target", required=True); a=p.parse_args()
    df=pd.read_csv(a.csv)
    if a.target not in df: raise SystemExit(f"Target {a.target!r} not found")
    y=df.pop(a.target)
    if y.nunique()!=2: raise SystemExit("Target must have exactly two classes")
    cats=df.select_dtypes(include="object").columns.tolist(); nums=df.select_dtypes(exclude="object").columns.tolist()
    prep=ColumnTransformer([("num",Pipeline([("impute",SimpleImputer(strategy="median")),("scale",StandardScaler())]),nums),("cat",Pipeline([("impute",SimpleImputer(strategy="most_frequent")),("encode",OneHotEncoder(handle_unknown="ignore"))]),cats)])
    Xtr,Xte,ytr,yte=train_test_split(df,y,test_size=.25,random_state=42,stratify=y)
    for name,model in [("logistic",LogisticRegression(max_iter=2000,class_weight="balanced")),("hist_gradient_boosting",HistGradientBoostingClassifier(max_iter=150,class_weight="balanced",random_state=42))]:
        pipe=Pipeline([("prep",prep),("model",model)]); pipe.fit(Xtr,ytr); pred=pipe.predict(Xte); prob=pipe.predict_proba(Xte)[:,1]
        print(f"\n{name}: ROC AUC={roc_auc_score(yte,prob):.3f}"); print(classification_report(yte,pred,zero_division=0))
if __name__=="__main__": main()
