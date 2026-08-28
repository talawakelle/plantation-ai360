from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sqlalchemy import select
from app.db.session import SessionLocal
from app.db.models import Estate, Division, Field

def main():
    db=SessionLocal()
    try:
        if db.scalar(select(Estate).where(Estate.code=="DEMO")):
            print("Demo already exists"); return
        e=Estate(company="TTEL",code="DEMO",name="Demo Estate",latitude=6.95,longitude=80.75,elevation_m=1200)
        d=Division(code="D1",name="Demo Division"); e.divisions.append(d)
        d.fields.append(Field(code="F01",name="Demo Field 01",area_ha=10,planted_year=2010,elevation_m=1250,latitude=6.95,longitude=80.75))
        db.add(e); db.commit(); print("Seeded demo estate/division/field")
    finally: db.close()
if __name__=="__main__": main()
