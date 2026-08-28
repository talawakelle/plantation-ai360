from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from datetime import datetime
import json
import joblib
import numpy as np
import pandas as pd
from sqlalchemy import select
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from app.db.session import SessionLocal
from app.db.models import CropRecord, WeatherRecord, LabourRecord, Field
from app.services.crop_model import FEATURES
from app.core.config import get_settings


def build_dataset(db):
    crop=pd.read_sql(select(CropRecord), db.bind)
    weather=pd.read_sql(select(WeatherRecord), db.bind)
    labour=pd.read_sql(select(LabourRecord), db.bind)
    fields=pd.read_sql(select(Field), db.bind)
    if crop.empty: return crop
    crop["record_date"]=pd.to_datetime(crop["record_date"])
    crop=crop.sort_values(["field_id","record_date"])
    daily=crop.groupby(["field_id","record_date"],as_index=False).agg(green_leaf_kg=("green_leaf_kg","sum"),plucking_round_days=("plucking_round_days","mean"))
    if not weather.empty:
        weather["record_date"]=pd.to_datetime(weather["record_date"])
        w=weather.groupby(["field_id","record_date"],as_index=False).agg(rainfall_mm=("rainfall_mm","mean"),temp_mean_c=("temp_mean_c","mean"))
        daily=daily.merge(w,on=["field_id","record_date"],how="left")
    else:
        daily["rainfall_mm"]=np.nan; daily["temp_mean_c"]=np.nan
    if not labour.empty:
        labour["record_date"]=pd.to_datetime(labour["record_date"])
        l=labour.groupby(["field_id","record_date"],as_index=False).agg(worker_days=("worker_days","sum"))
        daily=daily.merge(l,on=["field_id","record_date"],how="left")
    else: daily["worker_days"]=np.nan
    f=fields[["id","area_ha","planted_year","elevation_m"]].rename(columns={"id":"field_id"})
    daily=daily.merge(f,on="field_id",how="left")
    daily["month"]=daily.record_date.dt.month
    daily["tea_age_years"]=daily.record_date.dt.year-daily.planted_year
    daily["rainfall_7d"]=daily.groupby("field_id").rainfall_mm.transform(lambda s:s.rolling(7,min_periods=1).sum())
    daily["rainfall_30d"]=daily.groupby("field_id").rainfall_mm.transform(lambda s:s.rolling(30,min_periods=1).sum())
    daily["temp_mean_7d"]=daily.groupby("field_id").temp_mean_c.transform(lambda s:s.rolling(7,min_periods=1).mean())
    daily["labour_7d"]=daily.groupby("field_id").worker_days.transform(lambda s:s.rolling(7,min_periods=1).sum())
    daily["crop_lag_7d"]=daily.groupby("field_id").green_leaf_kg.transform(lambda s:s.shift(1).rolling(7,min_periods=1).sum())
    daily["crop_lag_30d"]=daily.groupby("field_id").green_leaf_kg.transform(lambda s:s.shift(1).rolling(30,min_periods=1).sum())
    return daily


def main():
    db=SessionLocal()
    try: df=build_dataset(db)
    finally: db.close()
    if df.empty or len(df)<200:
        raise SystemExit(f"Not enough crop history for training. Need at least 200 usable daily records; found {len(df)}.")
    data=df.dropna(subset=FEATURES+["green_leaf_kg"]).sort_values("record_date")
    if len(data)<200: raise SystemExit(f"Only {len(data)} complete rows after feature preparation. Load weather/labour/field master data.")
    split=int(len(data)*0.8); train=data.iloc[:split]; test=data.iloc[split:]
    Xtr=train[FEATURES]; ytr=train.green_leaf_kg; Xte=test[FEATURES]; yte=test.green_leaf_kg
    candidates={
        "random_forest":RandomForestRegressor(n_estimators=350,min_samples_leaf=2,n_jobs=-1,random_state=42),
        "hist_gradient_boosting":HistGradientBoostingRegressor(max_iter=350,l2_regularization=1.0,random_state=42),
    }
    scored=[]
    for name,model in candidates.items():
        model.fit(Xtr,ytr); pred=model.predict(Xte)
        mae=float(mean_absolute_error(yte,pred)); rmse=float(mean_squared_error(yte,pred)**0.5)
        scored.append((mae,rmse,name,model))
        print(name,"MAE",round(mae,2),"RMSE",round(rmse,2))
    mae,rmse,name,winner=sorted(scored,key=lambda x:x[0])[0]
    s=get_settings(); model_path=Path(s.crop_model); meta_path=Path(s.crop_model_meta); model_path.parent.mkdir(parents=True,exist_ok=True)
    joblib.dump(winner,model_path)
    meta={"model_name":name,"version":datetime.utcnow().strftime("%Y%m%d%H%M%S"),"features":FEATURES,"metrics":{"mae":mae,"rmse":rmse,"test_rows":len(test),"train_rows":len(train)},"data_max_date":str(data.record_date.max().date())}
    meta_path.write_text(json.dumps(meta,indent=2),encoding="utf-8")
    print("Saved winner:",name,model_path)

if __name__ == "__main__": main()
