#!/usr/bin/env python3
"""Package existing final files without rebuilding book content."""
from pathlib import Path
import hashlib,json,zipfile
root=Path(__file__).resolve().parents[1]
out=root.parent/'book-final-exports'; out.mkdir(exist_ok=True)
extras=['FINAL_PUBLICATION_AUDIT.md','KDP_AI_DISCLOSURE.md','KDP_RELEASE_CHECKLIST.md','COPYRIGHT_AUDIT.md','ARTWORK_REVIEW.md','EDITORIAL_REVIEW.md','SOURCE_VERIFICATION.md','README.md']
allfiles=sorted(p for p in root.rglob('*') if p.is_file() and not any(x in p.relative_to(root).parts for x in ['.git','__pycache__']) and p.suffix!='.pyc')
kindle=sorted(set(list((root/'release').glob('*'))+[root/x for x in extras]))
results=[]
for name,files in [('The_Light_of_Buddha_Volume_1_Complete.zip',allfiles),('The_Light_of_Buddha_Volume_1_Kindle_Package.zip',kindle)]:
 dest=out/name
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in files:
   z.write(p,'light-of-buddha/'+str(p.relative_to(root)))
 with zipfile.ZipFile(dest) as z:
  assert z.testzip() is None
  count=len(z.infolist())
 results.append({'file':name,'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'members':count,'crc_test':'pass'})
(out/'archive-verification.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
