from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.security import require_admin
from app.db.session import get_db
from app.db.models import Estate, Division, Field
from app.schemas import EstateIn, DivisionIn, FieldIn

router = APIRouter(tags=["master-data"], dependencies=[Depends(require_admin)])

@router.post("/estates")
def create_estate(payload: EstateIn, db: Session = Depends(get_db)):
    if db.scalar(select(Estate).where(Estate.code == payload.code)):
        raise HTTPException(409, "Estate code already exists")
    obj = Estate(**payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return {"id": obj.id, **payload.model_dump()}

@router.get("/estates")
def list_estates(db: Session = Depends(get_db)):
    return [{"id": x.id, "company": x.company, "code": x.code, "name": x.name} for x in db.scalars(select(Estate).order_by(Estate.company, Estate.name)).all()]

@router.post("/divisions")
def create_division(payload: DivisionIn, db: Session = Depends(get_db)):
    obj = Division(**payload.model_dump()); db.add(obj); db.commit(); db.refresh(obj)
    return {"id": obj.id, **payload.model_dump()}

@router.post("/fields")
def create_field(payload: FieldIn, db: Session = Depends(get_db)):
    obj = Field(**payload.model_dump()); db.add(obj); db.commit(); db.refresh(obj)
    return {"id": obj.id, **payload.model_dump()}

@router.get("/hierarchy")
def hierarchy(db: Session = Depends(get_db)):
    estates = db.scalars(select(Estate).order_by(Estate.company, Estate.name)).all()
    out=[]
    for e in estates:
        out.append({
            "id": e.id, "company": e.company, "code": e.code, "name": e.name,
            "divisions": [{
                "id": d.id, "code": d.code, "name": d.name,
                "fields": [{"id": f.id, "code": f.code, "name": f.name, "area_ha": f.area_ha} for f in d.fields]
            } for d in e.divisions]
        })
    return out
