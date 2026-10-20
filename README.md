# ZACUT 15.2 | Google discoverability and degree titles

Built *from version 15.1*. No modifications to `assets/app.js`, `assets/styles.css`, `data/zacut-corpus.json`, images, logos, or original research docs.

## Only changes to the existing website
- The position labels for Maximilian de Molière and Vladislav (Zeev) Slepoy now use Dr. / ד״ר. Chen Avizohar-Hagay was **already** labeled Dr. / ד״ר in v15.1 and is unchanged.
- `index.html` contains search-specific metadata, a canonical URL, and a no-JavaScript link to the static catalog. Visual layout and functionality are unchanged.

## Added search entry points
- `catalog.html`: accessible, linked alphabetical/corpus index of 469 manuscript entries.
- `entries/ZacutSH-001.html` etc.: 469 compact HTML pages containing **original unmodified text**, work and headword, stable URL, and a link back to the **same entry** in the interactive edition.
- `project.html`, `people.html`, `publications.html`: static source-derived informational pages, separate from (and with no impact on) the SPA.
- `assets/search-index.css`: shared CSS only for the above new static HTML pages.
- `sitemap.xml`: 474 absolute, crawler-readable URLs (homepage, four secondary pages, 469 entries).
- `robots.txt`: informational file; IMPORTANT: GitHub Pages serves this project under `/zacut/`, but crawler robots policy is read only at `https://elijah-dhlab.github.io/robots.txt`, not `/zacut/robots.txt`. The most reliable way to make the sitemap known is to **submit `https://elijah-dhlab.github.io/zacut/sitemap.xml` to Google Search Console**. Editing the host's real robots.txt would require control of the organization user-site repository and is not part of this version.

Google discovery/indexation is not guaranteed. The published repository and Pages site must be **publicly reachable** (no login, correct branch/source). To confirm, use Google Search Console URL Inspection and sitemap report.

## Source of truth and maintenance
`data/zacut-corpus.json` remains the source of truth for the 469 textual records; static entry pages were generated from this data and must be **regenerated** after any future edits to corpus or metadata. The release builder is archived as `tools/build-release-v15-2.py`; it expects the v15.1 baseline alongside the release in `/mnt/data` and can be adapted for future builds. The original interactive app remains byte-for-byte intact.

## Deploy
Extract the archive contents so `index.html`, `data/`, `assets/`, `entries/` and `sitemap.xml` are at the repository root. Publish from `main` / `(root)` in GitHub Pages. After deployment, verify a concrete entry URL and `sitemap.xml` return HTTP 200.
