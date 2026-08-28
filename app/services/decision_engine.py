from datetime import date, timedelta
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.db.models import CropRecord, WeatherRecord, DiseaseEvent, LabourRecord, SprayRecord


def field_risk(db: Session, field_id: int, as_of: date | None = None) -> dict:
    as_of = as_of or date.today()
    d30 = as_of - timedelta(days=30)
    d14 = as_of - timedelta(days=14)

    weather_count = db.scalar(select(func.count(WeatherRecord.id)).where(
        WeatherRecord.field_id == field_id, WeatherRecord.record_date.between(d30, as_of))) or 0
    labour_count = db.scalar(select(func.count(LabourRecord.id)).where(
        LabourRecord.field_id == field_id, LabourRecord.record_date.between(d14, as_of))) or 0
    crop_count = db.scalar(select(func.count(CropRecord.id)).where(
        CropRecord.field_id == field_id, CropRecord.record_date.between(d14, as_of))) or 0

    missing=[]
    if weather_count == 0: missing.append("recent_weather")
    if labour_count == 0: missing.append("recent_labour")
    if crop_count == 0: missing.append("recent_crop")
    if missing:
        return {
            "status":"DATA_NOT_PROVIDED",
            "field_id":field_id,
            "as_of":as_of.isoformat(),
            "missing":missing,
            "risk_score":None,
            "priority":None,
            "message":"Risk score not calculated because required evidence is missing.",
        }

    rain = db.scalar(select(func.sum(WeatherRecord.rainfall_mm)).where(
        WeatherRecord.field_id == field_id, WeatherRecord.record_date.between(d30, as_of))) or 0.0
    disease_count = db.scalar(select(func.count(DiseaseEvent.id)).where(
        DiseaseEvent.field_id == field_id, DiseaseEvent.observed_date.between(d30, as_of))) or 0
    labour = db.scalar(select(func.sum(LabourRecord.worker_days)).where(
        LabourRecord.field_id == field_id, LabourRecord.record_date.between(d14, as_of))) or 0.0
    last_spray = db.scalar(select(func.max(SprayRecord.application_date)).where(SprayRecord.field_id == field_id))
    crop_14 = db.scalar(select(func.sum(CropRecord.green_leaf_kg)).where(
        CropRecord.field_id == field_id, CropRecord.record_date.between(d14, as_of))) or 0.0

    # Transparent prototype scoring only. Thresholds/weights require agronomic validation.
    score = 0.0
    reasons = []
    if disease_count >= 2:
        score += 35; reasons.append({"signal":"recent_disease_events","value":disease_count,"weight":35})
    elif disease_count == 1:
        score += 20; reasons.append({"signal":"recent_disease_events","value":disease_count,"weight":20})
    if rain >= 250:
        score += 20; reasons.append({"signal":"30d_rainfall_mm","value":rain,"weight":20})
    # Zero labour is now a real observation because labour records exist in the required window.
    if labour <= 0:
        score += 20; reasons.append({"signal":"14d_worker_days_zero","value":labour,"weight":20})
    # Spray history is informational only until source completeness is explicitly known.
    if last_spray is not None:
        days_since=(as_of-last_spray).days
        reasons.append({"signal":"days_since_last_recorded_spray","value":days_since,"weight":0})
    if crop_14 <= 0:
        score += 15; reasons.append({"signal":"14d_crop_zero","value":crop_14,"weight":15})

    score=min(100.0,score)
    priority="CRITICAL" if score>=75 else "HIGH" if score>=50 else "MEDIUM" if score>=25 else "NORMAL"
    return {
        "status":"OK", "field_id":field_id, "as_of":as_of.isoformat(),
        "risk_score":score, "priority":priority, "reasons":reasons,
        "warning":"Prototype transparent scoring. Validate thresholds and weights with agronomic evidence before operational use.",
    }
