# PlantationAI 360 v0.1.0

Integrated AI decision-support platform for tea plantation operations.

## Phase 1 scope in this package

This is the foundation build for the final PlantationAI 360 platform. It already includes:

- Admin-only API shell
- Estate → Division → Field master hierarchy
- Central operational data schema
- Crop, weather, fertilizer, spray, disease, labour and factory record endpoints
- NASA POWER daily weather connector
- Generic CSV/Excel ingestion endpoint
- AI model registry and prediction audit log
- Crop forecasting training/inference service
- Tea disease vision inference service (loads a trained Ultralytics model when available)
- Disease training/export scripts for NVIDIA GPU workstation
- Field risk / decision-engine starter
- Static Admin dashboard
- Docker/PostgreSQL/PostGIS production scaffold
- SQLite development mode
- Windows PowerShell launch helpers
- Tests and smoke checks

The system intentionally returns `MODEL_NOT_READY` or `DATA_NOT_PROVIDED` rather than fabricating AI outputs.

## Recommended workstation

For training, use the NVIDIA RTX 3060 12 GB machine with **Python 3.11** and a CUDA-compatible PyTorch installation. Keep CUDA/PyTorch installation separate from the normal Python dependency install because the correct wheel depends on the installed driver/CUDA environment.

## Quick start — Windows

```powershell
cd PlantationAI360_v0.1.0
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python scripts\init_db.py
python -m uvicorn app.main:app --host 0.0.0.0 --port 8780 --reload
```

Open:

- Dashboard: http://127.0.0.1:8780/
- API docs: http://127.0.0.1:8780/docs
- Health: http://127.0.0.1:8780/api/v1/health

Default development admin token is defined in `.env.example`. **Change it before any network deployment.**

## GPU setup

Install PyTorch for the CUDA version supported by the GPU machine, then:

```powershell
pip install -r requirements-gpu.txt
python scripts\gpu_check.py
```

## Tea disease model training

Dataset folder expected by the starter trainer:

```text
data/vision/tea_disease/
  train/
    Healthy/
    Blister_Blight/
    ...
  val/
    Healthy/
    Blister_Blight/
    ...
  test/
    ...
```

Train:

```powershell
python scripts\train_tea_disease.py --data data\vision\tea_disease --model yolo26n-cls.pt --epochs 80 --imgsz 640
```

The default model name is configurable because Ultralytics model families evolve. Use a classification checkpoint supported by the installed Ultralytics version.

Export:

```powershell
python scripts\export_vision_model.py --weights runs\classify\tea_disease\weights\best.pt
```

Copy `best.pt` to:

```text
models/vision/tea_disease/best.pt
```

and restart the API. The `/api/v1/vision/disease/predict` endpoint will then use it.

## Crop forecasting

Upload historical records using the ingestion endpoint or insert them through `/api/v1/operations/crop`.

Train a model:

```powershell
python scripts\train_crop_forecast.py
```

The first implementation benchmarks a deterministic seasonal baseline against tree-based models and records held-out MAE/RMSE. It saves the winner only if enough data exist.

## NASA POWER weather

The service uses the NASA POWER daily point API for supplementary weather variables. Estate actual weather should remain the preferred source where available.

Example API call after creating a field with latitude/longitude:

```text
POST /api/v1/weather/nasa/sync?field_id=1&start=20260101&end=20260812
```

## Production deployment

`docker-compose.yml` provides a PostGIS-backed deployment scaffold. Before production:

1. Replace all development secrets.
2. Use HTTPS via reverse proxy.
3. Restrict database/network access.
4. Add backup jobs.
5. Connect source systems with read-only credentials.
6. Add real organization SSO/RBAC before enabling non-admin users.

## Architecture rule

Every machine prediction is auditable. `model_name`, `model_version`, source entity, prediction, confidence/interval, input snapshot hash and timestamp belong in the prediction log.

No source/model support → no guessed answer.
