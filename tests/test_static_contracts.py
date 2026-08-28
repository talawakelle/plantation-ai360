from pathlib import Path

def test_critical_files_exist():
    root=Path(__file__).resolve().parents[1]
    for p in ["app/main.py","app/db/models.py","app/services/vision.py","app/services/crop_model.py","frontend/index.html","docker-compose.yml"]:
        assert (root/p).exists(), p

def test_no_trained_model_shipped_as_fake():
    root=Path(__file__).resolve().parents[1]
    assert not (root/"models/vision/tea_disease/best.pt").exists()
    assert not (root/"models/crop/crop_forecast.joblib").exists()
