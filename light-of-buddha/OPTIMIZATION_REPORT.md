# Kindle and print optimization report

Completed 23 October 2026 against the previously audited release. The story text and verse/chants were left intact. Only the compiler credit was aligned to the requested wording, **Compiled by Jaspal Singh**, and the layout and image packaging were optimized.

## Before and after

| Deliverable | Before | Optimized | Change |
| --- | ---: | ---: | ---: |
| Reflowable EPUB | 30,792,392 bytes | 16,413,506 bytes | 14,378,886 bytes smaller (46.7%) |
| Paperback PDF | 35,981,571 bytes | 35,978,999 bytes | 2,572 bytes smaller; print images retained unchanged |
| Separate Kindle cover JPEG | 2,127,324 bytes | 1,366,890 bytes | 760,434 bytes smaller (35.8%) |
| Print page count | 129 | 124 | 5 pages fewer (3.9%) |
| EPUB image payloads, including cover | 30,673,917 bytes | 16,272,969 bytes | 14,400,948 bytes smaller (46.9%) |
| Story artwork in EPUB | 28,546,593 bytes | 14,906,079 bytes | 13,640,514 bytes smaller (47.8%) |

Exact machine-readable data is in `publishing/quality-assurance/optimization-metrics.json`. `publishing/quality-assurance/image-inventory.csv` inventories 157 source, working, release and proof images with pixel dimensions, formats, byte sizes and SHA-256 hashes. Per-illustration source and Kindle rendition measurements are in `image-optimization.json`.

## Layout and reading experience

The print compositor no longer forces a page break between each story. Front matter remains intentionally separated; the four part openings, story headings and illustration sequence retain their designed hierarchy. Stories and back matter flow into available space. H1/H2 styles keep headings with following text, body text uses widow/orphan control, and the PDF preserves 6×9-inch trim, 0.65-inch margins, embedded Noto Serif and consistent centered page numbers. The linked contents and PDF bookmarks are rebuilt from the final pagination.

All 124 pages were rendered to a contact-sheet overview. No blank pages, margin flags or replacement characters were found. The only pages below 35 extracted text words are 1 (half-title), 2 (title), 4 (dedication) and 10 (part/story opening with illustration); these are intentional. Page count remains above 100 because the complete stories, illustrations, thirteen verse interludes and source apparatus are retained without filler.

The EPUB is reflowable EPUB 3 with selectable text, linked navigation, accessible image alt text and responsive image sizing. Roman-script Pali diacritics pass the Noto Serif font coverage check; the current manuscript contains no Devanagari Hindi/Sanskrit text. It no longer fixes images to viewport height. The typography uses reader-selected serif defaults, 1.45 line-height, fluid margins, and widow/orphan control. Story sections stay in a continuous XHTML reading flow; the navigation remains linked. No duplicate image payloads were found among the 31 images.

## Image handling

Original 1122×1402 story JPEGs, their 1122×1402 PNG masters and the historical cover/source artwork are preserved in `artwork/` and `cover/`. The print PDF continues to embed the unchanged 300-PPI-at-3.74-inch story images. A separate 30-image Kindle set uses same-dimension optimized JPEG renditions (quality 82, 4:4:4 chroma, progressive encoding); it changes only Kindle assets and does not degrade print art. The cover remains portrait 1600×2560 RGB JPEG, suitable for Kindle marketing. Its separate typography was recomposited from the retained painting with the exact compiler credit.

## Content preservation and verification

The 30 story source files, thirteen Pali interludes, translations and meanings compare byte-for-byte unchanged against the base commit `6a7a7821e4e3605be516f7ddfce97e73b9899c2b`. The editable Markdown project remains in `manuscript/`; no story was rewritten or removed. The final EPUB, PDF and DOCX are rebuilt from that source. SHA-256 hashes for the release files are in `release/SHA256SUMS`.

Actual checks: `python scripts/build.py --final`; `python scripts/validate.py --require-epubcheck`; `python scripts/font_check.py`; `python scripts/epubcheck.py --jar /workspace/tools/epubcheck/epubcheck-5.4.0/epubcheck.jar`. Official EPUBCheck 5.4.0 passed on the final EPUB with zero fatals, errors, warnings or usage messages. Structural checks found linked navigation, valid local resources and fragments, all image alt text, no blank print pages, correct trim and exact requested credit in EPUB, print PDF and DOCX.

