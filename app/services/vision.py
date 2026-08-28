from pathlib import Path
from functools import lru_cache
from app.core.config import get_settings


class VisionModelNotReady(RuntimeError):
    pass


@lru_cache(maxsize=1)
def _load_model():
    settings = get_settings()
    path = Path(settings.vision_disease_model)
    if not path.exists():
        raise VisionModelNotReady(f"Disease model not found: {path}")
    try:
        from ultralytics import YOLO
    except ImportError as exc:
        raise VisionModelNotReady("Ultralytics is not installed. Install requirements-gpu.txt") from exc
    return YOLO(str(path))


def predict_disease(image_path: str) -> dict:
    model = _load_model()
    results = model.predict(source=image_path, verbose=False)
    if not results:
        return {"status": "NO_RESULT"}
    result = results[0]
    if getattr(result, "probs", None) is not None:
        top1 = int(result.probs.top1)
        conf = float(result.probs.top1conf)
        label = result.names[top1]
        return {
            "status": "OK",
            "task": "classification",
            "label": label,
            "confidence": conf,
            "uncertain": conf < 0.60,
        }
    boxes = getattr(result, "boxes", None)
    detections = []
    if boxes is not None:
        for box in boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            detections.append({"label": result.names[cls], "confidence": conf, "xyxy": [float(x) for x in box.xyxy[0]]})
    return {"status": "OK", "task": "detection", "detections": detections, "uncertain": not detections}
