# Formal EPUBCheck provenance and actual result

Official release: https://github.com/w3c/epubcheck/releases/download/v5.4.0/epubcheck-5.4.0.zip

Release ZIP SHA-256 verified by root: `33350c61038e71dfb3d45a76aed04bf5481e6d5500cb780f6e98db8bbd15a28c`.

Installed jar: `/workspace/tools/epubcheck/epubcheck-5.4.0/epubcheck.jar`, with release dependencies alongside. Validator binaries remain outside the project/archive; download the official release to repeat the test.

Actual version: EPUBCheck v5.4.0. Actual command:

```sh
python scripts/epubcheck.py --jar /workspace/tools/epubcheck/epubcheck-5.4.0/epubcheck.jar
python scripts/validate.py --require-epubcheck
python scripts/report.py
```

Actual Java execution is recorded in epubcheck.log: exit0, zero fatals/errors/warnings/infos. See epubcheck-result.json for the jar and exact EPUB SHA-256 values; epubcheck-detailed.json retains the complete formal machine-readable report. No EPUB corrections were needed for this formal pass.

Kindle Previewer is unavailable on PATH and was not run. EPUBCheck does not replace Amazon conversion/device review, human proofreading or physical print proof approval.
