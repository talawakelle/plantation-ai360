from pathlib import Path
import csv
import json

from ultralytics import YOLO
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)

WEIGHTS = Path(r"H:\PlantationAI360\runs\classify\runs\classify\tea_disease\weights\best.pt")
TEST_ROOT = Path(r"H:\PlantationAI360\data\vision\tea_disease\test")
OUT = Path(r"H:\PlantationAI360\runs\classify\tea_disease_test_report")
OUT.mkdir(parents=True, exist_ok=True)

if not WEIGHTS.exists():
    raise SystemExit(f"MODEL NOT FOUND: {WEIGHTS}")

if not TEST_ROOT.exists():
    raise SystemExit(f"TEST DATA NOT FOUND: {TEST_ROOT}")

model = YOLO(str(WEIGHTS))

class_names = [
    model.names[i]
    for i in sorted(model.names.keys())
]

y_true = []
y_pred = []
rows = []

for true_class_dir in sorted(TEST_ROOT.iterdir()):
    if not true_class_dir.is_dir():
        continue

    true_label = true_class_dir.name

    results = model.predict(
        source=str(true_class_dir),
        imgsz=640,
        device=0,
        verbose=False,
        stream=True,
    )

    for result in results:
        pred_id = int(result.probs.top1)
        predicted = result.names[pred_id]
        confidence = float(result.probs.top1conf)

        y_true.append(true_label)
        y_pred.append(predicted)

        rows.append({
            "image": str(result.path),
            "actual": true_label,
            "predicted": predicted,
            "confidence": confidence,
            "correct": true_label == predicted,
        })

accuracy = accuracy_score(y_true, y_pred)
balanced = balanced_accuracy_score(y_true, y_pred)
macro_f1 = f1_score(y_true, y_pred, average="macro")
weighted_f1 = f1_score(y_true, y_pred, average="weighted")

report = classification_report(
    y_true,
    y_pred,
    labels=class_names,
    output_dict=True,
    zero_division=0,
)

matrix = confusion_matrix(
    y_true,
    y_pred,
    labels=class_names,
)

with open(OUT / "predictions.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["image", "actual", "predicted", "confidence", "correct"],
    )
    writer.writeheader()
    writer.writerows(rows)

with open(OUT / "classification_report.json", "w", encoding="utf-8") as f:
    json.dump(
        {
            "accuracy": accuracy,
            "balanced_accuracy": balanced,
            "macro_f1": macro_f1,
            "weighted_f1": weighted_f1,
            "per_class": report,
        },
        f,
        indent=2,
    )

with open(OUT / "confusion_matrix.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["actual\\predicted"] + class_names)
    for label, row in zip(class_names, matrix):
        writer.writerow([label] + row.tolist())

print()
print("=" * 70)
print("PLANTATIONAI 360 - TEA DISEASE HELD-OUT TEST")
print("=" * 70)
print(f"Images             : {len(y_true)}")
print(f"Accuracy           : {accuracy:.4f}")
print(f"Balanced Accuracy  : {balanced:.4f}")
print(f"Macro F1           : {macro_f1:.4f}")
print(f"Weighted F1        : {weighted_f1:.4f}")
print()
print(classification_report(
    y_true,
    y_pred,
    labels=class_names,
    digits=4,
    zero_division=0,
))
print("Saved to:", OUT)
