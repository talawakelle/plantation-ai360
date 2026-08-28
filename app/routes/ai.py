from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import require_admin
from app.db.session import get_db
from app.services.crop_model import predict_one, CropModelNotReady
from app.services.decision_engine import field_risk

router = APIRouter(tags=["decision-ai"], dependencies=[Depends(require_admin)])

@router.post("/crop/predict")
def crop_predict(features: dict):
    try:
        return predict_one(features)
    except CropModelNotReady as exc:
        return {"status":"MODEL_NOT_READY","message":str(exc)}

@router.get("/field-risk/{field_id}")
def risk(field_id: int, as_of: date | None = None, db: Session = Depends(get_db)):
    return field_risk(db, field_id, as_of)
