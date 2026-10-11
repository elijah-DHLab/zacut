# Quality assurance report: ZACUT v12

## Scope

Review of the complete static UI (eight routes plus About subsections), in Hebrew and English, in headless Chromium at viewport widths 1440, 1024, 768, 390 and 320 pixels. Additional interaction checks were performed for the main reading and research workflows.

## Confirmed improvements

1. **Distant-reading anatomy:** 17 original annotation features remain selectable. The horizontal scroller has been replaced with a tidy, collapsible responsive grid; the entire grid fits its container in desktop and mobile views. Filtering, entry ordering, and loading another 100 entries work.
2. **Ontological search:** fixed the grid's min-content overflow. The form fits within the screen from 320 to 1440 px without document-wide horizontal scrolling.
3. **Edition mobile navigation:** the entry sequence now scrolls vertically in a height-limited, multi-column area. The selected entry is kept in view, rather than displaying entry 001 when reading entry 140.
4. **Mobile headings:** subdued the decorative letter-engine in small internal-page intros to stop overprinting the editorial heading.
5. **Mobile About and older network components:** tightened responsive layout and removed unnecessary sideways scrolling.

## Test matrix

| Area | Checks | Result |
| --- | --- | --- |
| Route rendering | Home, edition, dictionary, search, structure, lab, comparison, About | No JavaScript page errors |
| Responsive layout | 1440/1024/768/390/320 px; Hebrew | No document-wide horizontal overflow |
| Responsive layout | 1440/768/390/320 px; English with LTR direction | No document-wide horizontal overflow |
| Edition | ZacutSH-140; 39 annotations; nine feature types; selection of an annotation | Passed |
| Textual fidelity | Displayed content of ZacutSH-140 compared character by character with JSON | 747/747 characters match |
| Manuscript navigation | Entry chooser, search for entry key, switch to second work | Passed |
| Dictionary | Alphabetical filtering, select entry, jump from entity to search | Passed |
| Search | Free text, structured query with AND, create research set, CSV export | Passed |
| Comparison | Match two entries and save them to a research set | Passed |
| Anatomy | Toggle palette; filter exact feature; sort; load 200 entries | Passed |
| Atlas | Enable two entity types; zoom controls | Passed |
| Atlas + structure | Select pair of entity types, convert to research set, enter anatomy | Passed |
| Data laboratory | Switch to statistical chart view | Passed |
| About | Project, manuscripts, team, publications, research method | Pages render |
| Language | EN/LTR and Hebrew/RTL | Passed |
| Mobile menu | Open mobile menu, navigate to anatomy, expand palette | Passed |
| JS syntax | `node --check` on `assets/app.js` | Passed |
| Data files | JSON parsing and required sections | Passed |

## Known dependencies and boundaries

- **External visual assets:** some partner logos and personnel photos point to external websites. Requests to these services are blocked in this testing environment. The UI provides label/typographic fallbacks. Save vetted images locally for production stability.
- **Deployment browser test:** loopback navigation in Chromium is blocked by the execution environment (`ERR_BLOCKED_BY_ADMINISTRATOR`). The self-contained HTML preview was tested. The published multi-file version has been checked for valid paths and assets but needs a smoke test on the actual GitHub Pages URL.
- **Other browsers:** automated checks were in Chromium, not Safari or Firefox.
- **Research limits:** no manuscript scan integration or complete SPARQL implementation yet. Graph positions are layout artefacts, and co-occurrence is not a semantically attested relation.
