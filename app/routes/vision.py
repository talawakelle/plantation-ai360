from pathlib import Path
import hashlib
from tempfile import NamedTemporaryFile
from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session
from app.core.security import require_admin
from app.db.session import get_db
from app.db.models import PredictionLog, DiseaseEvent
from app.services.vision import predict_disease, VisionModelNotReady
from datetime import date

router = APIRouter(tags=["vision-ai"], dependencies=[Depends(require_admin)])

@router.post("/disease/predict")
async def disease_predict(file: UploadFile = File(...), field_id: int | None = Form(default=None), save_event: bool = Form(default=False), db: Session = Depends(get_db)):
    content = await file.read()
    if not content:
        return {"status":"DATA_NOT_PROVIDED","message":"Image is empty."}
    suffix = Path(file.filename or "upload.jpg").suffix or ".jpg"
    with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(content); tmp_path=tmp.name
    try:
        try:
            result = predict_disease(tmp_path)
        except VisionModelNotReady as exc:
            return {"status":"MODEL_NOT_READY","message":str(exc)}
        input_hash = hashlib.sha256(content).hexdigest()
        db.add(PredictionLog(model_name="tea_disease", model_version="active", task="vision_disease", entity_type="field", entity_id=field_id, prediction=result, input_hash=input_hash, source_ref=file.filename))
        if save_event and field_id and result.get("status") == "OK" and not result.get("uncertain") and result.get("label"):
            db.add(DiseaseEvent(field_id=field_id, observed_date=date.today(), label=result["label"], confidence=result.get("confidence"), source="PlantationAI", image_path=None, verified=False))
        db.commit()
        return result
    finally:
        Path(tmp_path).unlink(missing_ok=True)
