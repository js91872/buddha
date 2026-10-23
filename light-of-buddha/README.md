# THE LIGHT OF BUDDHA — Volume 1

30 Timeless Stories of Wisdom, Compassion & Inner Peace  
Compiled and Retold by Jaspal Singh

This is an unpublished production package for final human editorial and publishing approval. Nothing has been submitted to Amazon. Read `release/release-report.md`, `EDITORIAL_REVIEW.md`, `SOURCE_VERIFICATION.md`, `ARTWORK_REVIEW.md`, `COPYRIGHT_AUDIT.md` and `KDP_RELEASE_CHECKLIST.md` before release.

## Editorial approach

Thirty original literary retellings based on identifiable Pali canonical texts, arranged in four thematic parts. This first volume deliberately concentrates on early Buddhist sources transmitted in Theravada; it does not claim to represent every Buddhist tradition. Canonical means included in a religious textual collection, not independently established history. Scene-setting is literary reconstruction. Parables and supernatural episodes are identified; dialogue is rendered indirectly rather than invented as verbatim Buddha quotations. Brief Pali interludes have separately identified meanings and sources.

## Project map

- `research/`: reference ledger, source records and contextual art research.
- `manuscript/`: modular editable text and assembled reading manuscript.
- `artwork/`: source masters, optimised story images, briefs, alt text and provenance.
- `cover/`: three concept studies, selected standalone painting and editable typography process.
- `publishing/`: build styles, metadata and actual quality checks.
- `release/`: review copies in EPUB, PDF and DOCX, Kindle marketing cover, metadata and report.
- `scripts/`: reproducible production and checking scripts. Generated illustration masters are preserved; artwork generation itself is not deterministic.

## Rebuilding

Use Python 3, Pillow, ReportLab and Pandoc; the build script documents further dependencies. Run from this project directory. The cover uses installed Nimbus Roman and DejaVu Sans; check font availability on another machine. `python scripts/cover.py` rebuilds the selected cover from its retained master. See `scripts/` for the book build command and actual QA logs in `publishing/quality-assurance/`.

No ISBN, publisher address, publication date, personal biography or ownership declaration has been invented. Contributor role mapping must be confirmed in the current KDP interface while preserving the exact visible compiler credit. Do not publish without explicit approval.

## Rebuild the review editions

Requirements: Python3 with ReportLab, Pillow, lxml, python-docx and PyMuPDF; Pandoc3; installed Noto Serif regular/bold/italic TTF fonts under `/usr/share/fonts/truetype/noto`. Fonts are embedded in the print PDF, not the reflowable EPUB. No external service is contacted by the build.

```sh
cd /workspace/light-of-buddha
python scripts/build.py --final
python scripts/validate.py > publishing/quality-assurance/validation-command.log
python scripts/report.py
```

`--final` requires the complete sequence01–30. Omitting it permits an explicitly partial smoke build during editing. The script assembles `manuscript/complete-manuscript.md`, inserts four thematic part headings and thirteen interludes according to `manuscript/verses-and-chants/insertion-map.json`, then creates EPUB3, DOCX and a6x9-inch no-bleed PDF in `release/`. Individual chapter image paths are normalised for the combined build. The print edition has an automatically paginated contents list, PDF outline/bookmarks, Unicode fonts, page numbers and illustrations displayed at 3.74 inches wide (300 native ppi). Its page count follows the actual content, rather than forcing the approximate100-page target.

The automatically created reports in `publishing/quality-assurance/` record actual Pandoc commands, exit codes, EPUB XML/navigation/asset/fragment checks, image dimensions, print page size and text-margin checks. These scripts do not claim Kindle Previewer or EPUBCheck validation. See release-report.md and dedicated validation logs for the actual available checks. Story illustrations, generated cover masters and proofread typography must already exist; the script never manufactures replacement art. A paperback full-wrap cover requires approved print specifications and is intentionally excluded.

## Additional reproducible checks and artwork preparation

The Python package versions used are recorded in `requirements.txt`; system Pandoc was 3.1.11.1. With the retained masters in place, `python scripts/prepare_art.py` refreshes story JPEGs, briefs, alt text and contact sheets. It also synchronises manuscript image descriptions with the actual selected scenes. `python scripts/cover.py` and `python scripts/cover_concepts.py` rebuild the separately composited cover typography and concept comparison. Neither process calls an image-generation service.

`python scripts/editorial_check.py` checks all thirty narrative lengths, required sections and duplicated paragraphs. `python scripts/font_check.py` checks manuscript character coverage in the installed print font (requires fonttools). These checks supplement source reading and visual inspection; they cannot establish historical truth or artistic perfection. Artwork generation is non-deterministic and is represented by retained native masters and detailed art briefs, rather than a promise to recreate identical images.

## Final audit and preserved originals

The final audit retains all thirty story illustrations and makes bounded editorial corrections. The approved current credit is **Compiled and Retold by Jaspal Singh**. Current publishing administration includes KDP_AI_DISCLOSURE.md; disclosure notes are not a claim that the book is entirely human written or illustrated.

The original project archive is preserved unchanged at /workspace/the-light-of-buddha-volume-1-project.zip and in the verified original GitHub export. A complete before-final-audit snapshot is retained separately at /workspace/light-of-buddha-before-final-audit. The newly named complete and Kindle packages are separate exports, not replacements for the original archive. See FINAL_PUBLICATION_AUDIT.md for actual final results, retrieval links and outstanding human/account checks.

## Formal EPUB validation

The final audited EPUB passes official EPUBCheck 5.4.0 with zero errors and warnings. The validator is downloaded separately from https://github.com/w3c/epubcheck/releases/tag/v5.4.0 and is not bundled with this book. Preserve its dependency folders when extracting the official ZIP.

```sh
python scripts/epubcheck.py --jar /absolute/path/to/epubcheck-5.4.0/epubcheck.jar
python scripts/validate.py --require-epubcheck > publishing/quality-assurance/validation-command.log
python scripts/report.py
python scripts/package_final.py
```

The formal result records the exact EPUB SHA-256. Any EPUB edit invalidates that result until the checker runs again. Kindle Previewer/device checks are separate and remain pending.
