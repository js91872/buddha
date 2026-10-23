# THE LIGHT OF BUDDHA — Volume 1

30 Timeless Stories of Wisdom, Compassion & Inner Peace  
Compiled by Jaspal Singh

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

`--final` requires the complete sequence01–30. Omitting it permits an explicitly partial smoke build during editing. The script assembles `manuscript/complete-manuscript.md`, inserts four thematic part headings and thirteen interludes according to `manuscript/verses-and-chants/insertion-map.json`, then creates EPUB3, DOCX and a6x9-inch no-bleed PDF in `release/`. Individual chapter image paths are normalised for the combined build. The print edition has an automatically paginated contents list, PDF outline/bookmarks, Unicode fonts, page numbers and illustrations displayed at four inches wide. Its page count follows the actual content, rather than forcing the approximate100-page target.

The automatically created reports in `publishing/quality-assurance/` record actual Pandoc commands, exit codes, EPUB XML/navigation/asset/fragment checks, image dimensions, print page size and text-margin checks. These scripts do not claim Kindle Previewer or EPUBCheck validation. See release-report.md and dedicated validation logs for the actual available checks. Story illustrations, generated cover masters and proofread typography must already exist; the script never manufactures replacement art. A paperback full-wrap cover requires approved print specifications and is intentionally excluded.

## Additional reproducible checks and artwork preparation

The Python package versions used are recorded in `requirements.txt`; system Pandoc was 3.1.11.1. With the retained masters in place, `python scripts/prepare_art.py` refreshes story JPEGs, briefs, alt text and contact sheets. It also synchronises manuscript image descriptions with the actual selected scenes. `python scripts/cover.py` and `python scripts/cover_concepts.py` rebuild the separately composited cover typography and concept comparison. Neither process calls an image-generation service.

`python scripts/editorial_check.py` checks all thirty narrative lengths, required sections and duplicated paragraphs. `python scripts/font_check.py` checks manuscript character coverage in the installed print font (requires fonttools). These checks supplement source reading and visual inspection; they cannot establish historical truth or artistic perfection. Artwork generation is non-deterministic and is represented by retained native masters and detailed art briefs, rather than a promise to recreate identical images.
