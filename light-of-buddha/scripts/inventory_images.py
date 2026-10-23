#!/usr/bin/env python3
"""Inventory source and derived raster art with stable hashes."""
from pathlib import Path
from PIL import Image
import csv,hashlib
R=Path(__file__).resolve().parents[1]
exts={'.jpg','.jpeg','.png','.webp','.gif','.tif','.tiff'}
rows=[]
for parent in ['artwork','cover','publishing/quality-assurance','publishing/kindle/images','release']:
 for p in sorted((R/parent).rglob('*')):
  if not p.is_file() or p.suffix.lower() not in exts:continue
  try:
   with Image.open(p) as im:width,height,fmt=im.width,im.height,im.format
  except Exception:continue
  rows.append({'path':str(p.relative_to(R)),'format':fmt,'width_px':width,'height_px':height,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
out=R/'publishing/quality-assurance/image-inventory.csv';out.parent.mkdir(parents=True,exist_ok=True)
with out.open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['path','format','width_px','height_px','bytes','sha256']);w.writeheader();w.writerows(rows)
print(f'Inventoried {len(rows)} source, working, release and proof images.')
