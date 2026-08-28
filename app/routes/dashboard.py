from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.core.security import require_admin
from app.db.session import get_db
from app.db.models import Estate, Division, Field, CropRecord, DiseaseEvent, FactoryRecord, PredictionLog

router = APIRouter(tags=["dashboard"], dependencies=[Depends(require_admin)])

@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    def count(model): return db.scalar(select(func.count(model.id))) or 0
    crop_total = db.scalar(select(func.sum(CropRecord.green_leaf_kg))) or 0.0
    return {
        "estates": count(Estate), "divisions": count(Division), "fields": count(Field),
        "crop_records": count(CropRecord), "crop_kg": crop_total,
        "disease_events": count(DiseaseEvent), "factory_records": count(FactoryRecord),
        "ai_predictions": count(PredictionLog),
    }
