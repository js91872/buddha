# Final production audit

Updated final-audit build, 23 October2026. Preserved the existing stories, artwork, original project snapshot and build structure. No satisfactory illustration was regenerated.

The approved display credit is now **Compiled and Retold by Jaspal Singh** in generated EPUB description, accessible cover description, PDF metadata, DOCX core properties, title pages and release report. EPUB structured person name remains Jaspal Singh with compiler role `com`; this does not imply personal manual translation or painting. Root updated the approved cover and reader-facing source files before the content freeze.

Print and editable Word illustration widths changed from4inches to3.74inches: the existing1122-pixel images now display at300effectivePPI without synthetic upsampling. Body type remains10.4points in print. The final no-bleed six-by-nine PDF is129pages, retaining complete narratives, all artwork, interludes and source notes. It has a page-numbered contents list, bookmarks, embedded Noto Serif text fonts and grouped wisdom/reflection/source sections. All seven final contact sheets were reviewed for layout, and the new title page was inspected at full size. No gross clipping or missing images were observed. This overview is not a claim of human proofreading or physical colour proof approval.

Actual commands completed:

```sh
python scripts/build.py --final
python scripts/validate.py
python scripts/report.py
```

The validator now exits nonzero on failed production gates. It checks story/interlude/image counts, story lengths, exact credit, EPUB XML/local resources/fragments/navigation metadata, accessible SVG cover, backward-compatible NCX title/identifier, marketing-cover dimensions, print margins/page size, and editable DOCX ZIP/XML/media/section size/credit. All local gates passed. DOCX contains30embedded story images and a6×9-inch section; XML/ZIP checks passed. Actual commands and machine-readable results are retained under publishing/quality-assurance/.

The complete manuscript count is25,276words under the validator's Unicode-token method, excluding illustration alt descriptions and hyperlink URLs but including headings, front/back matter and source notes. Narrative-only count is16,127words. Other editorial counting methods may differ slightly on compound words; no story was shortened to force a page target.

Official EPUBCheck5.4.0 was downloaded and installed by root outside the project at /workspace/tools/epubcheck/epubcheck-5.4.0/epubcheck.jar. This agent ran scripts/epubcheck.py against the exact final EPUB: exit0, zero fatals, zero errors, zero warnings and zero informational messages. No EPUB changes were necessary. The result is bound to EPUB SHA-256 `84d6fb15f5e2295af978ff5837a224bd8f3f846b5f127c3a77f9805b9a1969b0`. The formal output, version, command, detailed JSON and hash evidence are retained in publishing/quality-assurance/. `python scripts/validate.py --require-epubcheck` passed, enforcing both a successful formal result and an exact hash match. The earlier blocked network attempt did not supply the validator; root's later successful download did.

Neither KindlePreviewer nor kindlepreviewer is available on PATH. Kindle device/Previewer review, Amazon previewers, human professional approval and a physical print proof remain outstanding. No Amazon upload or publication was performed.
