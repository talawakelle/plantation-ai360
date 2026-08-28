#!/usr/bin/env bash
set -euo pipefail
[ -f .env ] || cp .env.example .env
python scripts/init_db.py
python -m uvicorn app.main:app --host 0.0.0.0 --port 8780 --reload
