# Data workspace

Do not overwrite source operational files. Copy/import source data into the PlantationAI warehouse through controlled ingestion.

Recommended folders:

- `raw/` immutable source snapshots
- `staged/` mapped/cleaned tables
- `vision/tea_disease/` image training data
- `exports/` generated datasets/results

Never place secrets or database passwords inside this folder.
