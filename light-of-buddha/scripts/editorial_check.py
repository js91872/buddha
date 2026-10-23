"""Editorial integrity checks; do not establish historical truth or replace reading."""
from pathlib import Path
from collections import Counter
import re,json
R=Path(__file__).resolve().parents[1]
report={'scope':'Mechanical editorial checks only; source truth and literary quality require reading.','stories':[],'errors':[],'duplicate_paragraphs':[]}
paragraphs={}
for p in sorted((R/'manuscript/stories').glob('[0-9][0-9]-*.md')):
 s=p.read_text();body=s.split('## Wisdom to Remember')[0]
 narrative=re.sub(r'^#.*$|!\[[^\]]*\]\([^)]*\)','',body,flags=re.M)
 words=re.findall(r"\b[\w]+(?:[’'-][\w]+)*\b",narrative)
 missing=[h for h in ['## Wisdom to Remember','## A Reflection for Today','## Source Note'] if h not in s]
 row={'file':str(p.relative_to(R)),'narrative_words':len(words),'required_sections_missing':missing,'source_url':bool(re.search(r'https://',s)),'illustration':bool(re.search(r'!\[[^\]]+\]',s))}
 report['stories'].append(row)
 if len(words)<500 or len(words)>750:report['errors'].append(f'{p.name}: narrative count {len(words)} outside500–750')
 if missing or not row['source_url'] or not row['illustration']:report['errors'].append(f'{p.name}: missing structural content')
 for para in narrative.split('\n\n'):
  para=para.strip()
  if len(para)>100:paragraphs.setdefault(para,[]).append(p.name)
report['duplicate_paragraphs']=[{'text':k,'files':v} for k,v in paragraphs.items() if len(v)>1]
if len(report['stories'])!=30:report['errors'].append(f"Expected30 stories, found{len(report['stories'])}")
report['total_narrative_words']=sum(x['narrative_words'] for x in report['stories'])
out=R/'publishing/quality-assurance/editorial-mechanical.json';out.write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({'stories':len(report['stories']),'narrative_words':report['total_narrative_words'],'errors':report['errors'],'duplicate_paragraphs':len(report['duplicate_paragraphs'])},ensure_ascii=False,indent=2))
raise SystemExit(bool(report['errors'] or report['duplicate_paragraphs']))
