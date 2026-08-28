from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import require_admin
from app.db.session import get_db
from app.db.models import CropRecord, WeatherRecord, FertilizerRecord, SprayRecord, DiseaseEvent, LabourRecord, FactoryRecord, SustainabilityRecord
from app.schemas import CropRecordIn, WeatherRecordIn, FertilizerRecordIn, SprayRecordIn, DiseaseEventIn, LabourRecordIn, FactoryRecordIn, SustainabilityRecordIn

router = APIRouter(tags=["operations"], dependencies=[Depends(require_admin)])


def create(model, payload, db):
    obj=model(**payload.model_dump()); db.add(obj); db.commit(); db.refresh(obj); return {"id": obj.id, **payload.model_dump()}

@router.post("/crop")
def crop(payload: CropRecordIn, db: Session = Depends(get_db)): return create(CropRecord,payload,db)
@router.post("/weather")
def weather(payload: WeatherRecordIn, db: Session = Depends(get_db)): return create(WeatherRecord,payload,db)
@router.post("/fertilizer")
def fertilizer(payload: FertilizerRecordIn, db: Session = Depends(get_db)): return create(FertilizerRecord,payload,db)
@router.post("/spray")
def spray(payload: SprayRecordIn, db: Session = Depends(get_db)): return create(SprayRecord,payload,db)
@router.post("/disease")
def disease(payload: DiseaseEventIn, db: Session = Depends(get_db)): return create(DiseaseEvent,payload,db)
@router.post("/labour")
def labour(payload: LabourRecordIn, db: Session = Depends(get_db)): return create(LabourRecord,payload,db)
@router.post("/factory")
def factory(payload: FactoryRecordIn, db: Session = Depends(get_db)): return create(FactoryRecord,payload,db)
@router.post("/sustainability")
def sustainability(payload: SustainabilityRecordIn, db: Session = Depends(get_db)): return create(SustainabilityRecord,payload,db)
