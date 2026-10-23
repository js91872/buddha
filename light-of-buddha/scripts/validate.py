#!/usr/bin/env python3
"""Independent, bounded local checks. Does not claim EPUBCheck or device review."""
from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from urllib.parse import unquote,urlsplit
import posixpath,json,re,shutil,sys,hashlib
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
 with Image.open(p) as im: checks['story_images'][str(n)]={'pixels':im.size,'mode':im.mode,'display_width_inches':3.74,'effective_print_ppi':round(im.width/3.74,1)}
p=R/'release/kindle-cover.jpg'
if p.exists():
 with Image.open(p) as im:checks['cover']={'size':im.size,'mode':im.mode,'bytes':p.stat().st_size,'pass':im.size==(1600,2560) and im.mode=='RGB' and p.stat().st_size<50_000_000}
else:issues.append('Missing Kindle marketing cover')
with ZipFile(R/'release/the-light-of-buddha-volume-1.epub') as z:
 names=z.namelist(); links=[]; parse=[]; alt=[]; textchars=0; fragments=[]; all_epub_text=[]
 ids={}
 for name in names:
  if name.endswith(('.xhtml','.svg')):
   try: ids[name]=set(etree.fromstring(z.read(name)).xpath('//@id'))
   except etree.XMLSyntaxError:pass
 for name in names:
  if not name.endswith(('.xhtml','.opf','.ncx','.xml')):continue
  try: tree=etree.fromstring(z.read(name))
  except etree.XMLSyntaxError as e:parse.append(str(e));continue
  if name.endswith('.xhtml'):
   textchars+=len(''.join(tree.itertext()));all_epub_text.append(''.join(tree.itertext()))
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
 checks['epub_credit']={'approved_credit_present':any('Compiled and Retold by Jaspal Singh' in t for t in all_epub_text),'old_credit_present':any('Compiled by Jaspal Singh' in t for t in all_epub_text)}
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
 checks['print']={'pages':len(d),'page_sizes_points':sorted(sizes),'rendered_font_names':sorted(rendered_fonts),'font_count':len(fonts),'font_file_extensions':sorted(set(f[1] for f in fonts.values())),'text_near_page_edges':sorted(set(oob)),'replacement_character_pages':badglyph,'six_by_nine_pass':sizes=={(432.0,648.0)},'approved_credit_present':any('Compiled and Retold by Jaspal Singh' in p.get_text() for p in d)}
checks['issues']=issues
checks['limitations']=['No Kindle Previewer/device check performed.','No claim of full human proofreading or Buddhist scholarship review.','Structural checks do not constitute EPUBCheck validation.','Native image resolution is measured; upsampling does not create original detail.']
Q.mkdir(exist_ok=True,parents=True)

# Validate editable Word content and exit nonzero when objective production gates fail.
from docx import Document
with ZipFile(R/'release/the-light-of-buddha-volume-1.docx') as z:
 docx_zip_error=z.testzip()
 docx_xml_errors=[]
 for name in z.namelist():
  if name.endswith('.xml'):
   try:etree.fromstring(z.read(name))
   except etree.XMLSyntaxError:docx_xml_errors.append(name)
 media=[n for n in z.namelist() if n.startswith('word/media/')]
wd=Document(R/'release/the-light-of-buddha-volume-1.docx')
word_text='\n'.join(p.text for p in wd.paragraphs)
checks['docx']={'zip_error':docx_zip_error,'xml_errors':docx_xml_errors,'embedded_images':len(media),'approved_credit_present':'Compiled and Retold by Jaspal Singh' in word_text,'old_credit_present':'Compiled by Jaspal Singh' in word_text,'section_sizes_inches':[[round(sec.page_width/914400,2),round(sec.page_height/914400,2)] for sec in wd.sections]}
checks['docx']['pass']=not docx_zip_error and not docx_xml_errors and len(media)==30 and checks['docx']['approved_credit_present'] and not checks['docx']['old_credit_present'] and checks['docx']['section_sizes_inches']==[[6.0,9.0]]
formal=Q/'epubcheck-result.json'
checks['epubcheck']={'available_result':formal.exists(),'pass':False}
if formal.exists():
 result=json.loads(formal.read_text());actual=hashlib.sha256((R/'release/the-light-of-buddha-volume-1.epub').read_bytes()).hexdigest()
 checks['epubcheck']=dict(result,available_result=True,hash_matches_current_epub=result.get('epub_sha256')==actual)
 checks['epubcheck']['pass']=result.get('exit_code')==0 and result.get('epub_sha256')==actual
full=(R/'manuscript/complete-manuscript.md').read_text()
full=re.sub(r'!\[.*?\]\([^)]+\)','',full)
full=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',full)
checks['complete_manuscript_word_count']=len(re.findall(r"\b[\w]+(?:[’'-][\w]+)*\b",full))
checks['word_count_method']='Unicode word tokens with optional internal apostrophe or hyphen; image alt and hyperlink URLs excluded; all reader-facing prose/headings/source notes included'
checks['gates']={'narrative_lengths':all(500<=n<=750 for n in checks['story_narrative_word_counts'].values()),'thirty_stories':checks['story_count_pass'],'thirteen_interludes':len(list((R/'manuscript/verses-and-chants').glob('[0-9][0-9]-interlude.md')))==13,'thirty_images':len(checks['story_images'])==30,'cover':checks.get('cover',{}).get('pass',False),'epub_structure':checks['epub']['pass'] and checks['epub']['uncompressed_first_entry_mimetype'],'epub_metadata':checks['epub_metadata']['pass'],'epub_credit':checks['epub_credit']['approved_credit_present'] and not checks['epub_credit']['old_credit_present'],'ncx':checks['ncx']['pass'],'cover_accessibility':checks['cover_accessibility']['pass'],'pdf':checks['print']['six_by_nine_pass'] and checks['print']['approved_credit_present'] and not checks['print']['text_near_page_edges'] and not checks['print']['replacement_character_pages'],'docx':checks['docx']['pass']}
if '--require-epubcheck' in sys.argv:checks['gates']['epubcheck']=checks['epubcheck']['pass']
checks['all_requested_gates_pass']=all(checks['gates'].values()) and not issues
(Q/'validation.json').write_text(json.dumps(checks,indent=2));print(json.dumps({'gates':checks['gates'],'all_requested_gates_pass':checks['all_requested_gates_pass']},indent=2))
raise SystemExit(0 if checks['all_requested_gates_pass'] else 1)
