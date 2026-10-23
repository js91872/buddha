#!/usr/bin/env python3
"""Write a release report from actual completed local validation output."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];Q=R/'publishing/quality-assurance';D=R/'release'
b=json.loads((Q/'build-checks.json').read_text());v=json.loads((Q/'validation.json').read_text())
assert b['stories']==30 and v['story_count_pass'],'Refuse final report for partial book'
counts=v['story_narrative_word_counts'];words=sum(counts.values())
assets=[]
for name in ['the-light-of-buddha-volume-1.epub','the-light-of-buddha-volume-1-print.pdf','the-light-of-buddha-volume-1.docx','kindle-cover.jpg','metadata.md']:
 p=D/name;assets.append((name,p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest()))
rows='\n'.join(f'| {n} | {size:,} | `{sha}` |' for n,size,sha in assets)
(D/'SHA256SUMS').write_text('\n'.join(f'{sha}  {n}' for n,size,sha in assets)+'\n')
report=f'''# The Light of Buddha — Volume 1 release report

Status: complete local production package for final human editorial and publishing approval. **Not submitted or published.** This is not a claim that every requested release gate has passed. EPUBCheck, Kindle Previewer, independent human scholarship, full professional proofreading and physical proof approval remain outstanding.

## Contents delivered

Thirty original literary retellings, four thematic parts, thirteen Pali verse/refuge interludes, half-title and full title pages, publication information, dedication, introduction, glossary, pronunciation guide, source notes, selected bibliography, closing reflection, series note and neutral compiler note. Exact display credit: **Compiled by Jaspal Singh**.

Narratives contain approximately {words:,} words in total; individual narrative counts range from {min(counts.values())} to {max(counts.values())} under the documented automated counting method (illustration alt text and appended reflections/source notes excluded). See validation.json for each story. All thirty story images and the cover are present. The EPUB is reflowable rather than a fixed-layout replica of print.

The companion print PDF has **{b['pdf_pages']} pages**, six by nine inches, no bleed, embedded Noto Serif text fonts, large illustrations displayed at four inches wide, automatic page-numbered contents and PDF bookmarks. This exceeds the approximate 100-page target because complete narratives, large illustrations, interludes and source apparatus have been retained at comfortable reading size. Do not reduce text merely to claim 100 pages.

## Actual local checks

- `python scripts/build.py --final`: completed; Pandoc command lines and exit codes in epub-build.log and docx-build.log.
- `python scripts/validate.py`: completed; machine-readable results in validation.json.
- EPUB XML parse errors: {len(v['epub']['xml_errors'])}; missing local linked resources: {len(v['epub']['missing_local_links'])}; missing fragment IDs: {len(v['epub']['missing_fragment_ids'])}; missing image alt attributes: {len(v['epub']['missing_image_alt'])}.
- EPUB metadata checked: exact main title and subtitle, contributor Jaspal Singh with compiler role `com`, and 31 raster-image resources.
- EPUB functional navigation document detected: {b['epub_has_navigation']}; MIME packaging checked. Structural checks passed: {v['epub']['pass']}.
- PDF page size: {v['print']['page_sizes_points']} points; empty pages detected: {b['pdf_empty_pages']}; text-margin flags: {v['print']['text_near_page_edges']}; replacement-character flags: {v['print']['replacement_character_pages']}.
- Cover: {v['cover']['size'][0]}×{v['cover']['size'][1]} pixels, {v['cover']['mode']}, {v['cover']['bytes']:,} bytes; local dimensions/mode/size gate passed: {v['cover']['pass']}.
- Every PDF page rendered to contact-sheet thumbnails for layout inspection; wisdom, reflection and source notes are grouped to prevent isolated source-note pages; these are not a substitute for reading every printed line. Sample full-page renders retained.
- EPUBCheck: **not run**, absent locally and download unavailable through the environment; see epubcheck.log for actual attempts.
- Kindle Previewer, Amazon online previewers, physical proof and device font-resize tests: **not run** in this environment.

## Required human and publisher decisions

Read EDITORIAL_REVIEW.md, SOURCE_VERIFICATION.md, ARTWORK_REVIEW.md, COPYRIGHT_AUDIT.md and KDP_RELEASE_CHECKLIST.md. A qualified Buddhist/Pali reader should approve interpretations, verse meanings and pronunciation. A professional human editor should approve the final prose and proofread the built files. An art reviewer should inspect all final artwork at full size, including hands, expressions and source-specific details. Automated checks cannot prove cultural accuracy or aesthetic excellence.

Generated story-art masters are generally 1122×1402 pixels, approximately 280 PPI when displayed four inches wide. The selected cover master is 992×1586 pixels and was resized to 1600×2560 pixels; a higher-resolution master would be desirable. Upsampling does not restore original painted detail. Review source masters and native image-resolution measurements before choosing print quality and obtaining a colour proof.

Research scope: all thirty English source anchors were checked, and all thirteen Pali interludes received a separate AI-agent review against cited root texts. Broader resources and two consulted Anālayo 2021 scholarly articles are documented in research/cross-tradition-context.md and research/scholarly-context.md; Indian and international museum references inform the art briefs. This is not a full Pali, Sanskrit, Chinese or Tibetan textual collation, nor independent human professional scholarly review.

The book uses AI-generated prose, English verse renderings and cover/interior imagery, not merely AI-assisted editing. KDP disclosure must accurately reflect those uses. No blanket claim of exclusive human authorship or universal copyright protection is made. Modern source translations remain distinct from ancient narratives; source-specific rights need publisher approval.

KDP's publicly accessible contributor guidance does not enumerate every live dropdown role. The structured EPUB uses compiler role `com`; confirm an accurate live KDP role before upload and do not silently substitute Author. Publisher/imprint, ISBN, date, territorial rights, price and final copyright notice remain publisher decisions. No personal biography beyond the neutral supplied compiler description has been invented.

A paperback full-wrap cover is intentionally absent: approved final trim, page count, paper/ink and bleed choices are required before calculating it. No KDP submission, upload or publication has occurred. Final user approval is required before any such action.

## Delivered files and integrity

| File | Bytes | SHA-256 |
| --- | ---: | --- |
{rows}

Build instructions are in README.md. Source files, art briefs, provenance records, native image masters, research records, typography assets, scripts and QA logs remain in the project tree. SHA256SUMS covers the principal release files listed above.
'''
(D/'release-report.md').write_text(report)
print('Wrote complete release report with actual checks and hashes')
