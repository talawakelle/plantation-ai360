# PlantationAI 360 v0.1.0 — Foundation Build

Built 12 August 2026.

## Implemented

- Admin-only FastAPI application
- Estate/division/field relational master
- Operational warehouse entities for crop, weather, fertilizer, spray, disease, labour, factory and sustainability data
- Model registry and prediction audit schema
- NASA POWER daily weather ingestion connector
- CSV/XLSX ingestion with strict column mapping
- Tea disease inference endpoint with explicit MODEL_NOT_READY behavior
- GPU training/export scripts for Ultralytics classification models
- Sri Lankan tea disease raw-image preparation pipeline with SHA-256 provenance, exact duplicate exclusion and deterministic train/val/test splitting
- Crop forecast feature/training scaffold with chronological holdout and model comparison
- Evidence-gated field-risk starter: missing source data returns DATA_NOT_PROVIDED
- Admin dashboard shell
- SQLite dev and PostGIS production scaffolds
- Windows/Linux run helpers

## Deliberately not claimed yet

- No trained production tea disease model is bundled.
- No crop forecast accuracy is claimed before real historical data are imported and held-out evaluation is run.
- No field-risk heuristic is approved as agronomic policy.
- No public image accuracy is claimed as TTE estate accuracy.

## Next build gate

Import actual estate/division/field master plus historical crop, weather and labour data. In parallel, acquire the pinned Sri Lankan public image dataset and train the first vision baseline.
