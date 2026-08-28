"""Prepare a leakage-resistant classification dataset from RAW source images.

Input shape:
  SOURCE_ROOT/<source class folders>/*.jpg

Output:
  OUTPUT_ROOT/train/<canonical class>/*.jpg
  OUTPUT_ROOT/val/<canonical class>/*.jpg
  OUTPUT_ROOT/test/<canonical class>/*.jpg
  OUTPUT_ROOT/manifest.csv

Use RAW originals only. Do not point this at an offline-augmented source folder.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import shutil
from pathlib import Path

IMAGE_EXTS={'.jpg','.jpeg','.png','.webp','.bmp'}

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def split_for(key: str, train_pct: int, val_pct: int) -> str:
    bucket=int(hashlib.sha256(key.encode()).hexdigest()[:8],16)%100
    if bucket < train_pct: return 'train'
    if bucket < train_pct+val_pct: return 'val'
    return 'test'

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',required=True)
    ap.add_argument('--output',required=True)
    ap.add_argument('--source-name',default='Sri_Lankan_Tea_Leaf_Dataset_v4')
    ap.add_argument('--label-map',default='configs/vision_label_map.json')
    ap.add_argument('--train',type=int,default=70)
    ap.add_argument('--val',type=int,default=15)
    ap.add_argument('--dry-run',action='store_true')
    args=ap.parse_args()
    if args.train+args.val>=100: raise SystemExit('train + val must be < 100')
    src=Path(args.source); out=Path(args.output)
    mapping=json.loads(Path(args.label_map).read_text(encoding='utf-8'))
    rows=[]; seen_hashes={}; unknown_labels=set(); duplicate_count=0
    for class_dir in sorted([p for p in src.iterdir() if p.is_dir()]):
        canonical=mapping.get(class_dir.name) or mapping.get(class_dir.name.lower())
        if not canonical:
            unknown_labels.add(class_dir.name); continue
        for p in sorted(class_dir.rglob('*')):
            if not p.is_file() or p.suffix.lower() not in IMAGE_EXTS: continue
            digest=sha256(p)
            if digest in seen_hashes:
                duplicate_count+=1
                rows.append({'source_file':str(p),'source_name':args.source_name,'source_class':class_dir.name,'canonical_class':canonical,'sha256':digest,'split':'DUPLICATE_EXCLUDED','copied_file':'','duplicate_of':seen_hashes[digest]})
                continue
            seen_hashes[digest]=str(p)
            split=split_for(digest,args.train,args.val)
            dest=out/split/canonical/f'{digest[:16]}{p.suffix.lower()}'
            if not args.dry_run:
                dest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,dest)
            rows.append({'source_file':str(p),'source_name':args.source_name,'source_class':class_dir.name,'canonical_class':canonical,'sha256':digest,'split':split,'copied_file':str(dest),'duplicate_of':''})
    if unknown_labels:
        raise SystemExit('Unmapped source class folders: '+', '.join(sorted(unknown_labels))+'. Update configs/vision_label_map.json explicitly; do not guess label equivalence.')
    if not rows: raise SystemExit('No supported images found.')
    out.mkdir(parents=True,exist_ok=True)
    manifest=out/'manifest.csv'
    with manifest.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    counts={}
    for r in rows:
        k=(r['split'],r['canonical_class']); counts[k]=counts.get(k,0)+1
    print('Prepared dataset:',out)
    print('Exact duplicates excluded:',duplicate_count)
    for k,v in sorted(counts.items()): print(k[0],k[1],v)
    print('Manifest:',manifest)

if __name__=='__main__': main()
