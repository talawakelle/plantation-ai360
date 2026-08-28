from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.db.base import Base
from app.db.session import engine
import app.db.models  # noqa
Base.metadata.create_all(bind=engine)
print("PlantationAI 360 database initialized.")
