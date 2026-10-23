# The Light of Buddha — Volume 1 release report

Status: complete local production package for final human editorial and publishing approval. **Not submitted or published.** This is not a claim that every requested release gate has passed. Kindle Previewer, independent human scholarship, full professional proofreading and physical proof approval remain outstanding.

## Contents delivered

Thirty original literary retellings, four thematic parts, thirteen Pali verse/refuge interludes, half-title and full title pages, publication information, dedication, introduction, glossary, pronunciation guide, source notes, selected bibliography, closing reflection, series note and neutral compiler note. Exact display credit: **Compiled and Retold by Jaspal Singh**.

The complete reader-facing manuscript contains 25,276 words under the recorded token-counting method, including front/back matter, headings and source notes, with image alt text and hyperlink URLs excluded. Narratives contain approximately 16,127 words in total; individual narrative counts range from 512 to 575 under the documented automated counting method (illustration alt text and appended reflections/source notes excluded). See validation.json for each story. All thirty story images and the cover are present. The EPUB is reflowable rather than a fixed-layout replica of print.

The companion print PDF has **129 pages**, six by nine inches, no bleed, embedded Noto Serif text fonts, large illustrations displayed at 3.74 inches wide, automatic page-numbered contents and PDF bookmarks. This exceeds the approximate 100-page target because complete narratives, large illustrations, interludes and source apparatus have been retained at comfortable reading size. Do not reduce text merely to claim 100 pages.

## Actual local checks

- `python scripts/build.py --final`: completed; Pandoc command lines and exit codes in epub-build.log and docx-build.log.
- `python scripts/validate.py`: completed; machine-readable results in validation.json.
- EPUB XML parse errors: 0; missing local linked resources: 0; missing fragment IDs: 0; missing image alt attributes: 0.
- EPUB metadata checked: exact main title and subtitle, contributor Jaspal Singh with compiler role `com`, and 31 raster-image resources.
- EPUB functional navigation document detected: True; MIME packaging checked. Structural checks passed: True.
- PDF page size: [[432.0, 648.0]] points; empty pages detected: []; text-margin flags: []; replacement-character flags: [].
- Cover: 1600×2560 pixels, RGB, 2,127,324 bytes; local dimensions/mode/size gate passed: True.
- Every PDF page rendered to contact-sheet thumbnails for layout inspection; wisdom, reflection and source notes are grouped to prevent isolated source-note pages; these are not a substitute for reading every printed line. Sample full-page renders retained.
- EPUBCheck: **passed on this exact EPUB; see epubcheck.log and epubcheck-result.json**.
- Kindle Previewer, Amazon online previewers, physical proof and device font-resize tests: **not run** in this environment.

## Required human and publisher decisions

Read EDITORIAL_REVIEW.md, SOURCE_VERIFICATION.md, ARTWORK_REVIEW.md, COPYRIGHT_AUDIT.md and KDP_RELEASE_CHECKLIST.md. A qualified Buddhist/Pali reader should approve interpretations, verse meanings and pronunciation. A professional human editor should approve the final prose and proofread the built files. An art reviewer should inspect all final artwork at full size, including hands, expressions and source-specific details. Automated checks cannot prove cultural accuracy or aesthetic excellence.

Generated story-art masters are generally 1122×1402 pixels, 300 PPI when displayed 3.74 inches wide. The selected cover master is 992×1586 pixels and was resized to 1600×2560 pixels; a higher-resolution master would be desirable. Upsampling does not restore original painted detail. Review source masters and native image-resolution measurements before choosing print quality and obtaining a colour proof.

Research scope: all thirty English source anchors were checked, and all thirteen Pali interludes received a separate AI-agent review against cited root texts. Broader resources and two consulted Anālayo 2021 scholarly articles are documented in research/cross-tradition-context.md and research/scholarly-context.md; Indian and international museum references inform the art briefs. This is not a full Pali, Sanskrit, Chinese or Tibetan textual collation, nor independent human professional scholarly review.

The book uses AI-generated prose, English verse renderings and cover/interior imagery, not merely AI-assisted editing. KDP disclosure must accurately reflect those uses. No blanket claim of exclusive human authorship or universal copyright protection is made. Modern source translations remain distinct from ancient narratives; source-specific rights need publisher approval.

KDP's publicly accessible contributor guidance does not enumerate every live dropdown role. The structured EPUB uses compiler role `com`; confirm an accurate live KDP role before upload and do not silently substitute Author. Publisher/imprint, ISBN, date, territorial rights, price and final copyright notice remain publisher decisions. No personal biography beyond the neutral supplied compiler description has been invented.

A paperback full-wrap cover is intentionally absent: approved final trim, page count, paper/ink and bleed choices are required before calculating it. No KDP submission, upload or publication has occurred. Final user approval is required before any such action.

## Delivered files and integrity

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| the-light-of-buddha-volume-1.epub | 30,792,392 | `84d6fb15f5e2295af978ff5837a224bd8f3f846b5f127c3a77f9805b9a1969b0` |
| the-light-of-buddha-volume-1-print.pdf | 35,981,571 | `b4ab9618a2d01f3a5c6fff7b87cca45c0c66b683f566c8154566107b085b7564` |
| the-light-of-buddha-volume-1.docx | 28,631,958 | `13b63e5e404f491dfdfaa10db4feb194398cb9e0920f856b2e289b3590e17063` |
| kindle-cover.jpg | 2,127,324 | `95841f362eb381eec80855059579a70f12399817d2834e2609a2d13d10e3d7d8` |
| metadata.md | 9,003 | `b63c1eb24195fe394b0211e9440a59d635983fca8d8d56d4eb8f19ea6afc12bd` |

Build instructions are in README.md. Source files, art briefs, provenance records, native image masters, research records, typography assets, scripts and QA logs remain in the project tree. SHA256SUMS covers the principal release files listed above.
