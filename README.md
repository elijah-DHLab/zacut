# ZACUT 15 | Anatomy of a Name

Version 15 incorporates the accepted design work of 14.1 into the standard site. There is no experimental banner or toggle.

## Changes from version 14

- Five-letter Hebrew headwords in the letter machine use the SAME font size as four-letter headwords. Character tracking is adjusted instead of shrinking type.
- Dictionary alphabet emblem and quick entry links for the selected initial letter.
- Animated letter-assembly seal when moving to a different entry in the reading edition; honors `prefers-reduced-motion`.
- Circular headword seals in the edition, lexicon lists/details, and search results.
- The experimental formal-spelling similarity feature has been COMPLETELY REMOVED, including its calculations and controls.
- Responsive dictionary width correction from the experimental branch retained.

## Publication and corpus content

Exactly the same data and publications as version 14: 469 entries, annotation offsets preserved, bilingual UI, full network atlas. Images supplied as external URLs remain dependent on their original hosts. No IIIF integration has been added.

## Install on GitHub Pages

Extract **the contents** of the ZIP into the repository root, where `index.html`, `assets/` and `data/` are siblings. Use GitHub Settings > Pages > Deploy from branch: `main` and `/(root)`. The GitHub build loads `assets/app.js`, `assets/styles.css`, `data/site-content.json`, and `data/zacut-corpus.json` over HTTP. Opening `index.html` directly via `file://` will not load the JSON; use the separate standalone HTML preview for local inspection.

## Sources and tests

`docs/publications-sources-v14.md`: verified bibliographic links. `docs/qa-v15.md`: validation and limits.
