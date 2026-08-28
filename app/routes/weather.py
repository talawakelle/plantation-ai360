from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.security import require_admin
from app.db.session import get_db
from app.db.models import Field, WeatherRecord
from app.services.nasa_power import fetch_daily

router = APIRouter(tags=["weather-ai"], dependencies=[Depends(require_admin)])

@router.post("/nasa/sync")
def nasa_sync(field_id: int, start: str = Query(pattern=r"^\d{8}$"), end: str = Query(pattern=r"^\d{8}$"), db: Session = Depends(get_db)):
    field = db.get(Field, field_id)
    if not field:
        raise HTTPException(404, "Field not found")
    lat = field.latitude or (field.division.estate.latitude if field.division and field.division.estate else None)
    lon = field.longitude or (field.division.estate.longitude if field.division and field.division.estate else None)
    if lat is None or lon is None:
        raise HTTPException(422, {"code":"LOCATION_NOT_PROVIDED","message":"Field or estate latitude/longitude is required."})
    rows = fetch_daily(lat, lon, start, end)
    inserted=0; updated=0
    for row in rows:
        existing = db.scalar(select(WeatherRecord).where(
            WeatherRecord.field_id == field_id,
            WeatherRecord.record_date == row["record_date"],
            WeatherRecord.source == "NASA_POWER",
        ))
        if existing:
            for k,v in row.items():
                if k != "record_date": setattr(existing,k,v)
            updated += 1
        else:
            db.add(WeatherRecord(field_id=field_id, source="NASA_POWER", **row)); inserted += 1
    db.commit()
    return {"field_id": field_id, "inserted": inserted, "updated": updated, "source": "NASA_POWER"}
