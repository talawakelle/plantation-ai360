from datetime import date
from pydantic import BaseModel, Field as PydField


class EstateIn(BaseModel):
    company: str
    code: str
    name: str
    latitude: float | None = None
    longitude: float | None = None
    elevation_m: float | None = None


class DivisionIn(BaseModel):
    estate_id: int
    code: str
    name: str


class FieldIn(BaseModel):
    division_id: int
    code: str
    name: str | None = None
    area_ha: float | None = None
    planted_year: int | None = None
    clone: str | None = None
    elevation_m: float | None = None
    latitude: float | None = None
    longitude: float | None = None
    pruning_cycle: str | None = None


class CropRecordIn(BaseModel):
    field_id: int
    record_date: date
    green_leaf_kg: float = PydField(ge=0)
    budget_kg: float | None = PydField(default=None, ge=0)
    plucking_round_days: float | None = PydField(default=None, ge=0)
    source: str = "internal"


class WeatherRecordIn(BaseModel):
    field_id: int
    record_date: date
    rainfall_mm: float | None = None
    temp_min_c: float | None = None
    temp_max_c: float | None = None
    temp_mean_c: float | None = None
    humidity_pct: float | None = None
    solar_mj_m2: float | None = None
    wind_m_s: float | None = None
    source: str = "estate"


class FertilizerRecordIn(BaseModel):
    field_id: int
    application_date: date
    product: str
    quantity_kg: float | None = None
    quantity_l: float | None = None
    source: str = "internal"


class SprayRecordIn(BaseModel):
    field_id: int
    application_date: date
    chemical: str
    purpose: str | None = None
    quantity_l: float | None = None
    quantity_kg: float | None = None
    source: str = "internal"


class DiseaseEventIn(BaseModel):
    field_id: int
    observed_date: date
    label: str
    severity_pct: float | None = PydField(default=None, ge=0, le=100)
    confidence: float | None = PydField(default=None, ge=0, le=1)
    source: str = "historical"
    image_path: str | None = None
    verified: bool = False


class LabourRecordIn(BaseModel):
    field_id: int
    record_date: date
    work_type: str
    workers: float | None = None
    worker_days: float | None = None
    output_kg: float | None = None
    source: str = "LifeHRMS"


class FactoryRecordIn(BaseModel):
    estate_id: int
    record_date: date
    green_leaf_intake_kg: float | None = None
    made_tea_kg: float | None = None
    outturn_pct: float | None = None
    moisture_pct: float | None = None
    fermentation_minutes: float | None = None
    energy_kwh: float | None = None
    quality_score: float | None = None
    grade: str | None = None
    source: str = "internal"


class SustainabilityRecordIn(BaseModel):
    estate_id: int
    record_date: date
    indicator_code: str
    value_numeric: float | None = None
    value_text: str | None = None
    unit: str | None = None
    source: str = "RA"
    evidence_ref: str | None = None
