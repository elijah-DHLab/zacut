# Zacut Research Environment, version 13

Static bilingual research environment for the original 469-entry Zacut corpus.

## Deployment

Upload the **contents** of this directory to a GitHub repository configured for GitHub Pages. Keep the directory hierarchy intact. The public site loads `data/zacut-corpus.json` and `data/site-content.json`. To update the corpus, replace the JSON file in Git and redeploy. No API token is needed.

The separate `zacut-machine-v13-preview.html` in the download message is a self-contained local preview with the current corpus embedded. Replacing the JSON in the deployment does not change that snapshot.

## Changes in version 13

- Fixed About → Project: partner logos occur once rather than both in the page body and the footer.
- Research network traversal: choose a node, move to its connected entries, or jump directly from an entry to another by shared annotated entities. A clickable path allows returning to prior entries and entities.
- The local-network inspector shows how many tagged entities two entries share; these are co-occurrences, **not** evidence of historical influence or textual dependency.
- Added official profile links for remaining scholars while retaining portraits only where a direct portrait URL is supplied or previously verified.

## Image status

External portrait image URLs already specified in `data/site-content.json` include Gerold Necker, Eliezer Baumgarten and Hadar Miller. Images may be blocked by a browser or by the source domain. The institutional pages for Yuval Harari, Uri Safrai, Maximilian de Molière and Vladislav Slepoy contain portrait/profile listings, but reliable direct image file URLs could not be retrieved in this environment; the design retains a typographic fallback rather than displaying a mismatched face. For reliable public deployment, copy licensed/authorized verified photographs into `assets/people/` and enter those paths as `portrait_url` in `data/site-content.json`.

## QA

Tested at 1440px and 390px via headless Chromium using a self-contained preview: About logo count, local entry -> next entry -> entity -> next entry -> path rewind, team cards, horizontal overflow and JavaScript errors. `data/zacut-corpus.json` unchanged.
