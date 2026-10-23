#!/usr/bin/env python3
"""Independent, bounded local checks. Does not claim EPUBCheck or device review."""
from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from urllib.parse import unquote,urlsplit
import posixpath,json,re,shutil
from PIL import Image,ImageDraw
import fitz
R=Path(__file__).resolve().parents[1]; Q=R/'publishing/quality-assurance'
checks={}; issues=[]
stories=sorted((R/'manuscript/stories').glob('[0-9][0-9]*.md'))
checks['story_count']=len(stories)
checks['story_narrative_word_counts']={}
for s in stories:
 text=s.read_text(); narrative=text.split('## Wisdom to Remember')[0]
 narrative=re.sub(r'!\[.*?\]\([^)]+\)','',narrative)
 narrative=re.sub(r'^#+.*$','',narrative,flags=re.M)
 checks['story_narrative_word_counts'][s.name]=len(re.findall(r"\b[\w]+(?:[’'-][\w]+)*\b",narrative))
checks['story_count_pass']=len(stories)==30
checks['story_images']={}
for n in range(1,31):
 p=R/f'artwork/story-illustrations/{n:02}.jpg'
 if not p.exists(): issues.append('Missing illustration '+str(n));continue
 with Image.open(p) as im: checks['story_images'][str(n)]={'pixels':im.size,'mode':im.mode,'ppi_at_four_inches':round(im.width/4,1)}
p=R/'release/kindle-cover.jpg'
if p.exists():
 with Image.open(p) as im:checks['cover']={'size':im.size,'mode':im.mode,'bytes':p.stat().st_size,'pass':im.size==(1600,2560) and im.mode=='RGB' and p.stat().st_size<50_000_000}
else:issues.append('Missing Kindle marketing cover')
with ZipFile(R/'release/the-light-of-buddha-volume-1.epub') as z:
 names=z.namelist(); links=[]; parse=[]; alt=[]; textchars=0; fragments=[]
 ids={}
 for name in names:
  if name.endswith(('.xhtml','.svg')):
   try: ids[name]=set(etree.fromstring(z.read(name)).xpath('//@id'))
   except etree.XMLSyntaxError:pass
 for name in names:
  if not name.endswith(('.xhtml','.opf','.ncx','.xml')):continue
  try: tree=etree.fromstring(z.read(name))
  except etree.XMLSyntaxError as e:parse.append(str(e));continue
  if name.endswith('.xhtml'):textchars+=len(''.join(tree.itertext()))
  for e in tree.iter():
   if e.tag.endswith('}img') and not e.get('alt'):alt.append(name)
   for attr in ('src','href','{http://www.w3.org/1999/xlink}href'):
    v=e.get(attr)
    if not v or urlsplit(v).scheme:continue
    target=posixpath.normpath(posixpath.join(posixpath.dirname(name),unquote(urlsplit(v).path))) if urlsplit(v).path else name
    fragment=unquote(urlsplit(v).fragment)
    if fragment and target in ids and fragment not in ids[target]:fragments.append({'from':name,'target':v})
    if target not in names:links.append({'from':name,'target':v})
 opf=etree.fromstring(z.read(next(n for n in names if n.endswith('.opf'))))
 ns={'o':'http://www.idpf.org/2007/opf','d':'http://purl.org/dc/elements/1.1/'}
 titles=opf.xpath('//d:title/text()',namespaces=ns)
 contributors=opf.xpath('//d:contributor/text()',namespaces=ns)
 roles=opf.xpath('//o:meta[@property="role"]/text()',namespaces=ns)
 image_count=len(opf.xpath('//o:item[starts-with(@media-type,"image/")]',namespaces=ns))
 ncx=etree.fromstring(z.read(next(n for n in names if n.endswith('.ncx'))))
 ncx_title=ncx.xpath('string(//*[local-name()="docTitle"]/*[local-name()="text"])')
 ncx_uid=ncx.xpath('string(//*[local-name()="meta"][@name="dtb:uid"]/@content)')
 opf_uid=opf.xpath('string(//d:identifier)',namespaces=ns)
 cover_tree=etree.fromstring(z.read(next(n for n in names if n.endswith('cover.xhtml'))))
 svg=cover_tree.find('.//{http://www.w3.org/2000/svg}svg')
 checks['cover_accessibility']={'role':svg.get('role'),'labelledby':svg.get('aria-labelledby'),'title':svg.xpath('string(*[local-name()="title"])'),'description':svg.xpath('string(*[local-name()="desc"])'),'pass':svg.get('role')=='img' and bool(svg.xpath('string(*[local-name()="title"])')) and bool(svg.xpath('string(*[local-name()="desc"])'))}
 checks['ncx']={'title':ncx_title,'uid_matches_opf':ncx_uid==opf_uid,'pass':ncx_title=='THE LIGHT OF BUDDHA' and ncx_uid==opf_uid}
 checks['epub_metadata']={'titles':titles,'contributors':contributors,'roles':roles,'raster_image_resources':image_count,'pass':'THE LIGHT OF BUDDHA' in titles and 'Jaspal Singh' in contributors and 'com' in roles and image_count==31}
 checks['epub']={'xml_errors':parse,'missing_local_links':links,'missing_image_alt':alt,'missing_fragment_ids':fragments,'text_characters':textchars,'uncompressed_first_entry_mimetype':z.infolist()[0].filename=='mimetype' and z.infolist()[0].compress_type==0,'pass':not(parse or links or alt or fragments)}
with fitz.open(R/'release/the-light-of-buddha-volume-1-print.pdf') as d:
 fonts={}; oob=[]; sizes=set(); badglyph=[]; images=[]; rendered_fonts=set()
 for i,p in enumerate(d):
  sizes.add((round(p.rect.width,2),round(p.rect.height,2)))
  for f in p.get_fonts():fonts[f[0]]=f
  for block in p.get_text('dict')['blocks']:
   for line in block.get('lines',[]):
    for span in line['spans']:rendered_fonts.add(span['font'])
  for b in p.get_text('blocks'):
   if b[0]<30 or b[2]>402 or b[1]<25 or b[3]>626:oob.append(i+1)
  if '\ufffd' in p.get_text():badglyph.append(i+1)
 archive=Q/'interim-layouts';archive.mkdir(exist_ok=True)
 for old in Q.glob('print-contact-*.jpg'):shutil.move(str(old),str(archive/old.name))
 for first in range(0,len(d),20):
  sheet=Image.new('RGB',(800,1160),'#e6e3dd');draw=ImageDraw.Draw(sheet)
  for i in range(first,min(first+20,len(d))):
   pix=d[i].get_pixmap(matrix=fitz.Matrix(.33,.33),alpha=False)
   thumb=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
   thumb.thumbnail((145,220));x=((i-first)%5)*160+7;y=((i-first)//5)*290+18
   sheet.paste(thumb,(x,y));draw.text((x,y+225),str(i+1),fill='black')
  sheet.save(Q/f'print-contact-{first+1:03}.jpg',quality=90)
 checks['print']={'pages':len(d),'page_sizes_points':sorted(sizes),'rendered_font_names':sorted(rendered_fonts),'font_count':len(fonts),'font_file_extensions':sorted(set(f[1] for f in fonts.values())),'text_near_page_edges':sorted(set(oob)),'replacement_character_pages':badglyph,'six_by_nine_pass':sizes=={(432.0,648.0)}}
checks['issues']=issues
checks['limitations']=['No Kindle Previewer/device check performed.','No claim of full human proofreading or Buddhist scholarship review.','Structural checks do not constitute EPUBCheck validation.','Native image resolution is measured; upsampling does not create original detail.']
Q.mkdir(exist_ok=True,parents=True);(Q/'validation.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks,indent=2))
