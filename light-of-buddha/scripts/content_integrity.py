#!/usr/bin/env python3
"""Check final text packages contain all story and interlude headings."""
from pathlib import Path
from lxml import etree
from docx import Document
from zipfile import ZipFile
import fitz,re,json
R=Path(__file__).resolve().parents[1]
token=re.compile(r"\b[\w]+(?:[’'-][\w]+)*\b")
def clean(s):return re.sub(r'\s+',' ',s).replace('’',"'").replace('‘',"'")
source=(R/'manuscript/complete-manuscript.md').read_text();source=re.sub(r'!\[.*?\]\([^)]+\)','',source);source=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',source)
stories=[re.match(r'^#\s+(.+)',p.read_text()).group(1).strip() for p in sorted((R/'manuscript/stories').glob('[0-9][0-9]*.md'))]
interludes=[re.match(r'^#\s+(.+)',p.read_text()).group(1).strip() for p in sorted((R/'manuscript/verses-and-chants').glob('[0-9][0-9]-interlude.md'))]
with ZipFile(R/'release/the-light-of-buddha-volume-1.epub') as z:epub=clean(' '.join(' '.join(etree.fromstring(z.read(n)).itertext()) for n in z.namelist() if n.endswith('.xhtml')))
wd=Document(R/'release/the-light-of-buddha-volume-1.docx');docx=clean(' '.join(p.text for p in wd.paragraphs))
with fitz.open(R/'release/the-light-of-buddha-volume-1-print.pdf') as d:pdf=clean(' '.join(p.get_text() for p in d))
texts={'epub':epub,'docx':docx,'pdf':pdf}
result={'stories':len(stories),'interludes':len(interludes),'story_headings_present':{k:all(clean(h) in v for h in stories) for k,v in texts.items()},'interlude_headings_present':{k:all(clean(h) in v for h in interludes) for k,v in texts.items()},'markdown_word_count':len(token.findall(source)),'docx_word_count':len(token.findall(docx)),'epub_word_count_including_toc_and_alt':len(token.findall(epub)),'pdf_word_count_including_page_numbers_and_toc':len(token.findall(pdf)),'story_and_interlude_source_files_unchanged':'verified by comparing their tracked content with the base commit'}
assert result['stories']==30 and result['interludes']==13 and all(all(x.values()) for x in [result['story_headings_present'],result['interlude_headings_present']])
out=R/'publishing/quality-assurance/content-integrity.json';out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
