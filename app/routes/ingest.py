from pathlib import Path
from tempfile import NamedTemporaryFile
from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
from app.core.security import require_admin
from app.db.session import get_db
from app.db.models import CropRecord, WeatherRecord, FertilizerRecord, SprayRecord, DiseaseEvent, LabourRecord, FactoryRecord, SustainabilityRecord

router = APIRouter(tags=["data-ingestion"], dependencies=[Depends(require_admin)])

MODELS = {
    "crop": CropRecord,
    "weather": WeatherRecord,
    "fertilizer": FertilizerRecord,
    "spray": SprayRecord,
    "disease": DiseaseEvent,
    "labour": LabourRecord,
    "factory": FactoryRecord,
    "sustainability": SustainabilityRecord,
}

@router.post("/table")
async def ingest_table(dataset: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    if dataset not in MODELS:
        raise HTTPException(422, {"code":"UNSUPPORTED_DATASET","supported":sorted(MODELS)})
    content = await file.read()
    suffix = Path(file.filename or "data.csv").suffix.lower()
    with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(content); path=Path(tmp.name)
    try:
        if suffix in {".xlsx", ".xlsm"}:
            df = pd.read_excel(path)
        elif suffix == ".csv":
            df = pd.read_csv(path)
        else:
            raise HTTPException(422, "Only .csv, .xlsx, .xlsm are supported in Phase 1")
        df = df.where(pd.notnull(df), None)
        model=MODELS[dataset]
        valid_cols={c.name for c in model.__table__.columns if c.name != "id"}
        unknown=[c for c in df.columns if c not in valid_cols]
        if unknown:
            raise HTTPException(422, {"code":"COLUMN_MAPPING_REQUIRED","unknown_columns":unknown,"expected_columns":sorted(valid_cols)})
        inserted=0; errors=[]
        for idx,row in df.iterrows():
            values={k:v for k,v in row.to_dict().items() if k in valid_cols and v is not None}
            for key in ("record_date","application_date","observed_date"):
                if key in values:
                    values[key]=pd.to_datetime(values[key]).date()
            try:
                with db.begin_nested():
                    db.add(model(**values)); db.flush()
                inserted += 1
            except Exception as exc:
                errors.append({"row":int(idx)+2,"error":str(exc)[:300]})
        db.commit()
        return {"dataset":dataset,"inserted":inserted,"errors":errors[:50],"error_count":len(errors)}
    finally:
        path.unlink(missing_ok=True)
