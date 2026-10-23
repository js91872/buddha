"""Check manuscript glyph coverage in the print font; not a visual proof."""
from pathlib import Path
from fontTools.ttLib import TTFont
import json
root=Path(__file__).resolve().parents[1]
text=(root/'manuscript/complete-manuscript.md').read_text()
font=TTFont('/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf')
codepoints=set().union(*(set(t.cmap) for t in font['cmap'].tables))
missing=sorted(set(c for c in text if not c.isspace() and ord(c) not in codepoints))
report={'font':'NotoSerif-Regular.ttf','unsupported_manuscript_characters':missing,'pass':not missing}
(root/'publishing/quality-assurance/font-coverage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False));raise SystemExit(bool(missing))
