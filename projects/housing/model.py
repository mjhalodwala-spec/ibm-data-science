import argparse, pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

def main():
 p=argparse.ArgumentParser(); p.add_argument("csv"); p.add_argument("--target",required=True); a=p.parse_args(); df=pd.read_csv(a.csv)
 y=df.pop(a.target); cats=df.select_dtypes(include="object").columns.tolist(); nums=df.select_dtypes(exclude="object").columns.tolist()
 prep=ColumnTransformer([("num",Pipeline([("impute",SimpleImputer(strategy="median")),("scale",StandardScaler())]),nums),("cat",Pipeline([("impute",SimpleImputer(strategy="most_frequent")),("encode",OneHotEncoder(handle_unknown="ignore"))]),cats)])
 Xtr,Xte,ytr,yte=train_test_split(df,y,test_size=.2,random_state=42)
 for name,m in [("median_baseline",DummyRegressor(strategy="median")),("ridge",Ridge(alpha=1.0)),("random_forest",RandomForestRegressor(n_estimators=250,min_samples_leaf=2,random_state=42))]:
  pipe=Pipeline([("prep",prep),("model",m)]); pipe.fit(Xtr,ytr); pred=pipe.predict(Xte); print(name,{"MAE":round(mean_absolute_error(yte,pred),2),"RMSE":round(mean_squared_error(yte,pred)**.5,2),"R2":round(r2_score(yte,pred),3)})
if __name__=="__main__":main()
