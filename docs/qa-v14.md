# ZACUT V14 QA results (2026-10-12)

## Scope

- v14 GitHub package has `index.html`, assets, corpus JSON and site-content JSON at relative paths suitable for a project subpath such as `/zacut/`.
- Corpus JSON is byte-identical to provided source; 469 entries retained.
- Site content contains four updated photo URLs from the editor and twelve bibliographic items, every one with a linked academic/publisher record or full publication.
- Original Hebrew title of the Baumgarten–Necker 2025 joint paper has not been established; the item is excluded.
- Five-letter Hebrew headwords are extracted by actual Hebrew letters (`U+05D0` through `U+05EA`), ignoring punctuation, spaces and pointing, with dedicated responsive typography.

## Browser QA

Using Chromium against the standalone HTML generated from exactly the ZIP's CSS/JS and JSON:

- 11 article/chapter cards + 1 volume card, all linked, grouped into project and related research.
- Tested five-letter headword `ZacutSH-017` (אנקתם): all five letters are in the machine DOM and rendered.
- Nine routes on desktop (home, edition, dictionary, search, structure, lab, compare, About project, About publications), in Hebrew and English: no page-level horizontal overflow.
- Nine routes on 390px mobile including team and publications: no page-level horizontal overflow.
- No browser JavaScript errors.

**Qualification:** Browser QA was conducted using the standalone HTML representation. Direct automated navigation to a `file://` local path was blocked by the environment; the actual published GitHub Pages deployment has not yet been tested. Image hosts were unavailable for local downloads; only source URLs and fallback behavior have been implemented.
