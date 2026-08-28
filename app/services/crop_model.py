from __future__ import annotations
from pathlib import Path
import json
import joblib
import pandas as pd
from app.core.config import get_settings


FEATURES = [
    "month", "area_ha", "tea_age_years", "elevation_m",
    "rainfall_7d", "rainfall_30d", "temp_mean_7d",
    "labour_7d", "crop_lag_7d", "crop_lag_30d", "plucking_round_days",
]


class CropModelNotReady(RuntimeError):
    pass


def load_crop_model():
    settings = get_settings()
    model_path = Path(settings.crop_model)
    meta_path = Path(settings.crop_model_meta)
    if not model_path.exists() or not meta_path.exists():
        raise CropModelNotReady("Crop forecast model is not trained yet.")
    return joblib.load(model_path), json.loads(meta_path.read_text(encoding="utf-8"))


def predict_one(features: dict) -> dict:
    model, meta = load_crop_model()
    missing = [f for f in FEATURES if features.get(f) is None]
    if missing:
        return {"status": "DATA_NOT_PROVIDED", "missing": missing}
    X = pd.DataFrame([{f: features[f] for f in FEATURES}])
    pred = float(model.predict(X)[0])
    return {
        "status": "OK",
        "forecast_kg": max(0.0, pred),
        "model_name": meta.get("model_name"),
        "model_version": meta.get("version"),
        "metrics": meta.get("metrics", {}),
    }
