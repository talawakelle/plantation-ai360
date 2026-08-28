import argparse
from pathlib import Path


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="Classification dataset root with train/val/test folders")
    ap.add_argument("--model", default="yolo26n-cls.pt", help="Ultralytics classification checkpoint supported by installed version")
    ap.add_argument("--epochs", type=int, default=80)
    ap.add_argument("--imgsz", type=int, default=640)
    ap.add_argument("--batch", type=int, default=-1, help="-1 lets Ultralytics choose an automatic batch size")
    args=ap.parse_args()
    root=Path(args.data)
    if not (root/"train").exists() or not (root/"val").exists():
        raise SystemExit("Dataset must contain train/ and val/ directories. Split ORIGINAL images before augmentation to prevent leakage.")
    from ultralytics import YOLO
    model=YOLO(args.model)
    model.train(data=str(root), epochs=args.epochs, imgsz=args.imgsz, batch=args.batch, project="runs/classify", name="tea_disease", device=0, patience=15, plots=True)
    print("Training finished. Evaluate on a held-out test set before deployment.")

if __name__ == "__main__": main()
