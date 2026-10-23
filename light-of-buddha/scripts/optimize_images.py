#!/usr/bin/env python3
"""Build separate reflowable-Kindle image renditions; source/print art stays untouched."""
from pathlib import Path
from PIL import Image
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
src=ROOT/'artwork/story-illustrations';dest=ROOT/'publishing/kindle/images';dest.mkdir(parents=True,exist_ok=True)
rows=[]
for n in range(1,31):
 source=src/f'{n:02}.jpg';target=dest/f'{n:02}.jpg'
 with Image.open(source) as im:
  im=im.convert('RGB')
  if max(im.size)>1600:
   im.thumbnail((1200,1600),Image.Resampling.LANCZOS)
  im.save(target,'JPEG',quality=82,optimize=True,progressive=True,subsampling=0)
  rows.append({'source':str(source.relative_to(ROOT)),'source_format':'JPEG','source_dimensions':Image.open(source).size,'source_bytes':source.stat().st_size,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'kindle':str(target.relative_to(ROOT)),'kindle_format':'JPEG','kindle_dimensions':im.size,'kindle_bytes':target.stat().st_size,'kindle_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'quality':82,'subsampling':'4:4:4'})
report={'purpose':'Reflowable Kindle image renditions only; print PDF continues to use untouched originals. Native masters and original JPEG assets remain in artwork/story-illustrations/.','images':rows,'source_total_bytes':sum(x['source_bytes'] for x in rows),'kindle_total_bytes':sum(x['kindle_bytes'] for x in rows),'saved_bytes':sum(x['source_bytes'] for x in rows)-sum(x['kindle_bytes'] for x in rows)}
(ROOT/'publishing/quality-assurance/image-optimization.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='images'},indent=2))
