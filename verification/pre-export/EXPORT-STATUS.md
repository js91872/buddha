# Book export verification

The original book and original archive have not been regenerated, rewritten, or uploaded.

All five existing release checksums match. All 319 archive members pass CRC checks and match their current project files byte for byte. The archive remains 240,017,651 bytes, with SHA-256 recorded in archive.sha256. The only non-cache project file not contained in the original archive is scripts/download_copies.py, added later as a download helper; no original book content is missing.

GitHub is connected at account level, but this task has no Git repository or remote. None of the accessible repository names identifies the book. No destination was selected and no branch, commit, LFS upload, release or asset was created. The GitHub CLI authentication check did not pass; an installed Git LFS binary alone is not evidence of working authenticated upload. No generic cloud-file upload or release-asset upload tool is available in this session.

## Retrieval

The exact original archive is /workspace/the-light-of-buddha-volume-1-project.zip. The exact publishing files remain in /workspace/light-of-buddha/release/. Workspace paths are not independently verified HTTPS download URLs. Previous mobile download errors have not been diagnosed as a size limit.

Open https://chatgpt.com/library in a desktop browser under the same account/workspace. If the archive is listed, select it and use Download. Library membership of this shell-created archive cannot be checked with the current tools, so this is a conditional route, not a claimed completed export. Official help: https://help.openai.com/en/articles/20001052-using-library-to-manage-files-in-chatgpt

If the archive is absent from Library or download still fails, a specific authorized destination repository and a working supported upload path are needed. Supply owner/repository or connect a dedicated private book repository. The 240 MB archive must not be committed as a normal Git blob; an authenticated LFS or release-asset mechanism must be verified first. No public upload is implied.

After obtaining the archive, verify SHA-256 using `shasum -a 256 the-light-of-buddha-volume-1-project.zip` on macOS, `sha256sum the-light-of-buddha-volume-1-project.zip` on Linux, or `Get-FileHash .\the-light-of-buddha-volume-1-project.zip -Algorithm SHA256` in Windows PowerShell. Compare to archive.sha256, then extract the ZIP.
