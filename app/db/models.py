from __future__ import annotations
from datetime import date, datetime
from sqlalchemy import String, Integer, Float, Date, DateTime, ForeignKey, Text, UniqueConstraint, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Estate(Base):
    __tablename__ = "estates"
    id: Mapped[int] = mapped_column(primary_key=True)
    company: Mapped[str] = mapped_column(String(32), index=True)
    code: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    elevation_m: Mapped[float | None] = mapped_column(Float, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    divisions: Mapped[list[Division]] = relationship(back_populates="estate", cascade="all, delete-orphan")


class Division(Base):
    __tablename__ = "divisions"
    __table_args__ = (UniqueConstraint("estate_id", "code", name="uq_division_estate_code"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    estate_id: Mapped[int] = mapped_column(ForeignKey("estates.id"), index=True)
    code: Mapped[str] = mapped_column(String(40), index=True)
    name: Mapped[str] = mapped_column(String(120))
    estate: Mapped[Estate] = relationship(back_populates="divisions")
    fields: Mapped[list[Field]] = relationship(back_populates="division", cascade="all, delete-orphan")


class Field(Base):
    __tablename__ = "fields"
    __table_args__ = (UniqueConstraint("division_id", "code", name="uq_field_division_code"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    division_id: Mapped[int] = mapped_column(ForeignKey("divisions.id"), index=True)
    code: Mapped[str] = mapped_column(String(40), index=True)
    name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    area_ha: Mapped[float | None] = mapped_column(Float, nullable=True)
    planted_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    clone: Mapped[str | None] = mapped_column(String(80), nullable=True)
    elevation_m: Mapped[float | None] = mapped_column(Float, nullable=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    pruning_cycle: Mapped[str | None] = mapped_column(String(80), nullable=True)
    division: Mapped[Division] = relationship(back_populates="fields")


class CropRecord(Base):
    __tablename__ = "crop_records"
    __table_args__ = (UniqueConstraint("field_id", "record_date", "source", name="uq_crop_field_date_source"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    field_id: Mapped[int] = mapped_column(ForeignKey("fields.id"), index=True)
    record_date: Mapped[date] = mapped_column(Date, index=True)
    green_leaf_kg: Mapped[float] = mapped_column(Float)
    budget_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    plucking_round_days: Mapped[float | None] = mapped_column(Float, nullable=True)
    source: Mapped[str] = mapped_column(String(80), default="internal")


class WeatherRecord(Base):
    __tablename__ = "weather_records"
    __table_args__ = (UniqueConstraint("field_id", "record_date", "source", name="uq_weather_field_date_source"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    field_id: Mapped[int] = mapped_column(ForeignKey("fields.id"), index=True)
    record_date: Mapped[date] = mapped_column(Date, index=True)
    rainfall_mm: Mapped[float | None] = mapped_column(Float, nullable=True)
    temp_min_c: Mapped[float | None] = mapped_column(Float, nullable=True)
    temp_max_c: Mapped[float | None] = mapped_column(Float, nullable=True)
    temp_mean_c: Mapped[float | None] = mapped_column(Float, nullable=True)
    humidity_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    solar_mj_m2: Mapped[float | None] = mapped_column(Float, nullable=True)
    wind_m_s: Mapped[float | None] = mapped_column(Float, nullable=True)
    source: Mapped[str] = mapped_column(String(80), default="estate")


class FertilizerRecord(Base):
    __tablename__ = "fertilizer_records"
    id: Mapped[int] = mapped_column(primary_key=True)
    field_id: Mapped[int] = mapped_column(ForeignKey("fields.id"), index=True)
    application_date: Mapped[date] = mapped_column(Date, index=True)
    product: Mapped[str] = mapped_column(String(120))
    quantity_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    quantity_l: Mapped[float | None] = mapped_column(Float, nullable=True)
    source: Mapped[str] = mapped_column(String(80), default="internal")


class SprayRecord(Base):
    __tablename__ = "spray_records"
    id: Mapped[int] = mapped_column(primary_key=True)
    field_id: Mapped[int] = mapped_column(ForeignKey("fields.id"), index=True)
    application_date: Mapped[date] = mapped_column(Date, index=True)
    chemical: Mapped[str] = mapped_column(String(120))
    purpose: Mapped[str | None] = mapped_column(String(180), nullable=True)
    quantity_l: Mapped[float | None] = mapped_column(Float, nullable=True)
    quantity_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    source: Mapped[str] = mapped_column(String(80), default="internal")


class DiseaseEvent(Base):
    __tablename__ = "disease_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    field_id: Mapped[int] = mapped_column(ForeignKey("fields.id"), index=True)
    observed_date: Mapped[date] = mapped_column(Date, index=True)
    label: Mapped[str] = mapped_column(String(120), index=True)
    severity_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    source: Mapped[str] = mapped_column(String(80), default="historical")
    image_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    verified: Mapped[bool] = mapped_column(Boolean, default=False)


class LabourRecord(Base):
    __tablename__ = "labour_records"
    id: Mapped[int] = mapped_column(primary_key=True)
    field_id: Mapped[int] = mapped_column(ForeignKey("fields.id"), index=True)
    record_date: Mapped[date] = mapped_column(Date, index=True)
    work_type: Mapped[str] = mapped_column(String(100), index=True)
    workers: Mapped[float | None] = mapped_column(Float, nullable=True)
    worker_days: Mapped[float | None] = mapped_column(Float, nullable=True)
    output_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    source: Mapped[str] = mapped_column(String(80), default="LifeHRMS")


class FactoryRecord(Base):
    __tablename__ = "factory_records"
    id: Mapped[int] = mapped_column(primary_key=True)
    estate_id: Mapped[int] = mapped_column(ForeignKey("estates.id"), index=True)
    record_date: Mapped[date] = mapped_column(Date, index=True)
    green_leaf_intake_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    made_tea_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    outturn_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    moisture_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    fermentation_minutes: Mapped[float | None] = mapped_column(Float, nullable=True)
    energy_kwh: Mapped[float | None] = mapped_column(Float, nullable=True)
    quality_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    grade: Mapped[str | None] = mapped_column(String(80), nullable=True)
    source: Mapped[str] = mapped_column(String(80), default="internal")


class SustainabilityRecord(Base):
    __tablename__ = "sustainability_records"
    id: Mapped[int] = mapped_column(primary_key=True)
    estate_id: Mapped[int] = mapped_column(ForeignKey("estates.id"), index=True)
    record_date: Mapped[date] = mapped_column(Date, index=True)
    indicator_code: Mapped[str] = mapped_column(String(80), index=True)
    value_numeric: Mapped[float | None] = mapped_column(Float, nullable=True)
    value_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    unit: Mapped[str | None] = mapped_column(String(40), nullable=True)
    source: Mapped[str] = mapped_column(String(120), default="RA")
    evidence_ref: Mapped[str | None] = mapped_column(Text, nullable=True)


class ModelRegistry(Base):
    __tablename__ = "model_registry"
    id: Mapped[int] = mapped_column(primary_key=True)
    model_name: Mapped[str] = mapped_column(String(120), index=True)
    version: Mapped[str] = mapped_column(String(60), index=True)
    task: Mapped[str] = mapped_column(String(80), index=True)
    artifact_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    metrics: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    training_data_ref: Mapped[str | None] = mapped_column(Text, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class PredictionLog(Base):
    __tablename__ = "prediction_log"
    id: Mapped[int] = mapped_column(primary_key=True)
    model_name: Mapped[str] = mapped_column(String(120), index=True)
    model_version: Mapped[str] = mapped_column(String(60), index=True)
    task: Mapped[str] = mapped_column(String(80), index=True)
    entity_type: Mapped[str] = mapped_column(String(40), index=True)
    entity_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    prediction: Mapped[dict] = mapped_column(JSON)
    input_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    source_ref: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
