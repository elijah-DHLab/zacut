# ZACUT V16 verification — 22 October 2026

## Scope
Base release: V15.2. This release changes only: Eliezer Baumgarten database-development credit; slight letter-spacing in small circular name seals; bilingual user guide in About; accessibility, privacy and rights/data-use sections; and footer links to these sections.

## Functional testing
- Chromium Playwright on a standalone HTML package (390 px, 768 px, 1440 px).
- 39 route/viewport combinations exercised, including home, edition, lexicon, search, anatomy, data lab, comparison, project, team and all four new About subsections.
- 11 guide chapters rendered in Hebrew and in English.
- Guide internal navigation and English language switching checked.
- No JavaScript exceptions or document-level horizontal overflow in these checks.

## Regression / unchanged assets
Byte-for-byte comparison against the V15.2 GitHub release: original 469 indexed entry HTML files, dataset JSON (469 entries), sitemap, robots.txt, search-index styles, logos, images, existing docs and other assets are unchanged. Modified files: README.md, assets/app.js, assets/styles.css, data/site-content.json. Added files: docs/user-guide-v16.json, docs/policies-v16.md and this report. In the site-content JSON, the only modified team record is Eliezer Baumgarten's description (HE and EN).

## Publishing / legal limitations
- Accessibility statement does **not** certify compliance; formal review is outstanding. Interactive network usability and keyboard accessibility require specialist assessment.
- Privacy statement reflects observed site implementation and should be rechecked when external services change.
- Data use text sets out the requested non-commercial research-with-credit policy, but no blanket Creative Commons license or institutional legal approval is claimed.
- Browser verification of the actual publicly hosted GitHub Pages URL is not included.
- Photographs sourced externally in earlier releases still depend on those services, except the already-local photo of Chen Avizohar-Hagay.
