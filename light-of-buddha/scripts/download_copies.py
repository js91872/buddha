from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED,ZIP_STORED
from PIL import Image
from io import BytesIO
import re,subprocess,json,hashlib
import fitz
r=Path('/workspace/light-of-buddha');out=Path('/workspace/shared/downloads/buddha-volume-1')
md=(r/'manuscript/complete-manuscript.md').read_text()
md=re.sub(r'!\[[^\]]*\]\([^)]+\)','',md)
(out/'complete-manuscript.md').write_text(md)
subprocess.run(['pandoc',str(out/'complete-manuscript.md'),'--standalone','--toc','--toc-depth=1','--metadata=title:THE LIGHT OF BUDDHA','-o',str(out/'complete-manuscript.docx')],check=True)
for ext in ['epub','docx']:
 src=r/f'release/the-light-of-buddha-volume-1.{ext}'
 dest=out/f'illustrated-review.{ext}'
 with ZipFile(src) as zin,ZipFile(dest,'w') as zout:
  for info in zin.infolist():
   data=zin.read(info.filename)
   if info.filename.lower().endswith(('.jpg','.jpeg','.png')):
    try:
     im=Image.open(BytesIO(data));im.thumbnail((800,1100));b=BytesIO()
     if info.filename.lower().endswith('.png'):im.save(b,format='PNG',optimize=True)
     else:im.convert('RGB').save(b,format='JPEG',quality=76,optimize=True)
     data=b.getvalue()
    except Exception:pass
   info.compress_type=ZIP_STORED if info.filename=='mimetype' else ZIP_DEFLATED
   zout.writestr(info,data)
 with ZipFile(dest) as z:assert z.testzip() is None
pdf=fitz.open(r/'release/the-light-of-buddha-volume-1-print.pdf')
pdf.rewrite_images(dpi_threshold=160,dpi_target=140,quality=76)
pdf.save(out/'illustrated-review.pdf',garbage=4,deflate=True)
pdf.close()
Image.open(r/'release/kindle-cover.jpg').save(out/'kindle-cover.jpg',quality=90,optimize=True)
(out/'READ-ME.txt').write_text('DOWNLOAD REVIEW COPIES\nThese contain the full book. The illustrated EPUB, DOCX and PDF use compressed images to reduce download size; they are not replacement print masters. Original publishing files remain in /workspace/light-of-buddha/release. complete-manuscript.docx and .md contain the complete text without illustrations. No publication has occurred.\n')
with ZipFile(out/'text-and-research.zip','w',ZIP_DEFLATED) as z:
 for p in [out/'complete-manuscript.docx',out/'complete-manuscript.md',out/'READ-ME.txt']:z.write(p,p.name)
 for base in ['research','manuscript','publishing/metadata']:
  for p in (r/base).rglob('*'):
   if p.is_file():z.write(p,'project/'+str(p.relative_to(r)))
 for p in r.glob('*.md'):z.write(p,'project/'+p.name)
rows=[]
for p in sorted(out.iterdir()):
 if p.is_file():rows.append({'file':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(out/'download-files.json').write_text(json.dumps(rows,indent=2))
print(json.dumps(rows,indent=2))
