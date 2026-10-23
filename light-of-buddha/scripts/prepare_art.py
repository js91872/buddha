from pathlib import Path
import json,csv,shutil,hashlib,re
from PIL import Image,ImageOps,ImageDraw
from artwork_data import SCENES
R=Path(__file__).resolve().parents[1]
paths=json.loads((R/'artwork/generated-paths.json').read_text())
masters=R/'artwork/story-illustrations/masters';masters.mkdir(exist_ok=True)
rows=[]
display_titles={}
for i,(title,scene,medium,ref) in enumerate(SCENES,1):
 id=f'{i:02}'
 stories=list((R/'manuscript/stories').glob(id+'-*.md'))
 if stories:
  story=stories[0];text=story.read_text();title=re.sub(r'^#\s*\d+\.\s*','',text.splitlines()[0])
  text=re.sub(r'!\[[^\]]*\]\(([^)]+)\)',lambda m:'!['+scene+']('+m[1]+')',text,count=1)
  story.write_text(text)
 display_titles[id]=title
 p=paths.get(id)
 if not p: continue
 src=Path(p); dest=masters/f'{id}.png'
 if src.exists():shutil.copy2(src,dest)
 im=Image.open(dest).convert('RGB');im.save(R/f'artwork/story-illustrations/{id}.jpg',quality=94,subsampling=0,dpi=(300,300))
 alt=scene
 (R/f'artwork/alt-text/{id}.txt').write_text(alt+'\n')
 brief=f'''# {id}. {title}\n\nSource anchor: {ref}, Pali Canon, Theravada transmission.\n\n## Narrative scene\n{scene}\n\n## Art direction\nMedium treatment: {medium}; AI-generated simulation, not a physical original painting. Portrait composition, meaningful restrained gesture and nuanced expression. Indigo, teal, ivory, ochre and earth; natural light. South Asian people, ancient north Indian landscape, simple draped cloth, clay vessels and modest rural structures. No modern objects or indiscriminate East Asian/Tibetan motifs.\n\nCharacter continuity: adult Buddha with gentle South Asian features, tightly curled dark hair and ochre robe; the pre-awakening seeker is lean with simple hair. The final journey uses an elderly face. These are devotional artistic conventions, not a recovered historical likeness. Avoid jewelry, excessive luminosity and ornamental spectacle.\n\nComposition and gesture: stage the stated encounter clearly; give each person a distinct expression and credible hands. Parable and conceptual scenes are illustrations of teachings rather than claims that the depicted encounter literally took place. Brahma/Mara belong to the canonical religious narrative. Scenery and props not specified by the source are artistic reconstruction.\n\nHistorical reference framework: research/art-history-references.md. No third-party artwork used as a visual input.\n\n## Asset\nMaster: masters/{id}.png; native size {im.width}×{im.height}. Optimised image: {id}.jpg. No cropping of story painting. At 4-inch width effective resolution {im.width/4:.0f} ppi; DPI metadata does not add detail.\n\nAlt text: {alt}\n\n## Inspection\nSee ARTWORK_REVIEW.md and QA contact sheets. Automated checks establish decoding, dimensions and distinct files, not artistic perfection. Final human art approval remains required.\n'''
 (R/f'artwork/illustration-briefs/{id}.md').write_text(brief)
 rows.append(dict(asset=f'artwork/story-illustrations/{id}.jpg',title=title,source=f'masters/{id}.png',creator='OpenAI image generation; directed in this project',status='AI-generated; no third-party input artwork',license='Service output; publisher must confirm applicable account terms and local protection',reference=ref,width=im.width,height=im.height,sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),alt_text=alt))
for p,label in [('cover/final/cover-art-source.png','Selected cover artwork'),('cover/concepts/three-concepts-source.png','Three cover concept study')]:
 im=Image.open(R/p)
 rows.append(dict(asset=p,title=label,source='OpenAI image-generation tool in this session',creator='OpenAI image generation; directed in this project',status='AI-generated; no third-party input artwork',license='Service output; publisher must confirm applicable account terms and local protection',reference='Devotional Buddha under Bodhi tree',width=im.width,height=im.height,sha256=hashlib.sha256((R/p).read_bytes()).hexdigest(),alt_text='A serene Buddha beneath heart-shaped Bodhi leaves.'))
with (R/'artwork/source-and-rights-register.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
# Contact sheets, six at a time; labels are production aids only.
for start in range(1,31,6):
 sheet=Image.new('RGB',(1200,1100),'#f6f0e3');d=ImageDraw.Draw(sheet)
 for j in range(6):
  id=f'{start+j:02}';p=R/f'artwork/story-illustrations/{id}.jpg'
  if not p.exists(): continue
  im=Image.open(p);im.thumbnail((380,495));x=(j%3)*400+(400-im.width)//2;y=(j//3)*550
  sheet.paste(im,(x,y));d.text(((j%3)*400+15,y+505),f'{id} {display_titles.get(id,SCENES[start+j-1][0])}',fill='black')
 sheet.save(R/f'publishing/quality-assurance/art-contact-{start:02}.jpg')
print(f'Prepared {len(paths)} story images and provenance rows.')
