# PlantationAI 360 architecture — v0.1

## Layers

1. **Source systems** — LifeHRMS, MD Booklet DB, estate spreadsheets/SQL, factory systems, sustainability records, weather APIs, documents.
2. **Ingestion/validation** — read-only extraction, schema mapping, source provenance, data quality gates.
3. **Operational warehouse** — PostgreSQL/PostGIS in production; SQLite only for local development.
4. **Feature/model layer** — crop forecasting, vision, factory analytics, workforce anomalies, sustainability compliance.
5. **Decision engine** — combines validated model outputs and transparent business/agronomic rules.
6. **Knowledge AI** — evidence-first retrieval from Booklet/docs/warehouse; unsupported answers return Data Not Provided.
7. **Admin web app** — initially one admin role, RBAC-ready database/API boundary later.

## Non-negotiable rules

- Source systems remain authoritative and are not modified by AI ingestion.
- Predictions are not facts; every prediction stores model/version/data provenance.
- Model outputs must expose uncertainty or prediction intervals when technically meaningful.
- Public image datasets may bootstrap models but do not prove local production accuracy.
- External weather is supplementary when estate measurements exist.
- Decision-engine rules require agronomic validation before operational recommendations are treated as policy.
