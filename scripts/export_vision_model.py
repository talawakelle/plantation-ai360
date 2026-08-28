import argparse
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--weights", required=True); ap.add_argument("--imgsz", type=int, default=640); args=ap.parse_args()
    if not Path(args.weights).exists(): raise SystemExit("Weights file not found")
    from ultralytics import YOLO
    model=YOLO(args.weights)
    out=model.export(format="onnx", imgsz=args.imgsz, simplify=True)
    print("Exported:", out)

if __name__ == "__main__": main()
