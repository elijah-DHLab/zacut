#!/usr/bin/env python3
"""Generate additive SEO artifacts for ZACUT, leaving v15.1 app unchanged."""
from pathlib import Path
import html, json, re, zipfile, hashlib, base64, copy
from urllib.parse import quote
from xml.etree.ElementTree import Element, SubElement, tostring

ROOT=Path('/mnt/data/zacut-machine-v15-2')
BASE=Path('/mnt/data/zacut-machine-v15-1-preview.html')
SITE_URL='https://elijah-dhlab.github.io/zacut/'
DATA=json.loads((ROOT/'data/zacut-corpus.json').read_text(encoding='utf-8'))
CONTENT=json.loads((ROOT/'data/site-content.json').read_text(encoding='utf-8'))
for member in CONTENT['team']:
    if member['id'] in {'maximilian','vladislav'}:
        member['position']['he']='ד״ר · אוניברסיטת האלה־ויטנברג'
        member['position']['en']='Dr. · Martin Luther University Halle-Wittenberg'
assert next(t for t in CONTENT['team'] if t['id']=='chen')['position']['he'].startswith('ד״ר')
(ROOT/'data/site-content.json').write_text(json.dumps(CONTENT,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def esc(x):return html.escape(str(x or ''),quote=True)
def link(path):return SITE_URL+path

def head(title,desc,url,css_path,lang='he',jsonld=None):
    out=['<!doctype html>','<html lang="'+lang+'" dir="rtl">','<head>','<meta charset="utf-8">',
     '<meta name="viewport" content="width=device-width, initial-scale=1">',
     '<meta name="theme-color" content="#f5f2ec">',
     '<meta name="robots" content="index,follow">',
     '<title>'+esc(title)+'</title>',
     '<meta name="description" content="'+esc(desc[:155])+'">',
     '<link rel="canonical" href="'+esc(url)+'">',
     '<link rel="stylesheet" href="'+esc(css_path)+'">']
    if jsonld:
        out.append('<script type="application/ld+json">'+json.dumps(jsonld,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+'</script>')
    out+=['</head>','<body>']
    return '\n'.join(out)+'\n'

def shell_open(depth=0):
    prefix='../'*depth
    return ('<header class="seo-header"><div class="seo-brand"><a href="'+prefix+'">ZACUT <small>ANATOMY OF A NAME</small></a></div>'
         '<nav aria-label="ניווט">'
         '<a href="'+prefix+'">האתר האינטראקטיבי</a>'
         '<a href="'+prefix+'catalog.html">מפתח הערכים</a>'
         '<a href="'+prefix+'project.html">הפרויקט</a>'
         '<a href="'+prefix+'people.html">חוקרים</a>'
         '<a href="'+prefix+'publications.html">פרסומים</a>'
         '</nav></header>\n<main class="seo-container">\n')

def shell_close(depth=0):
    prefix='../'*depth
    return ('</main><footer class="seo-footer">Kabbalah Editions · '
     '<a href="'+prefix+'">המהדורה הדיגיטלית של זכות</a> · '
     '<a href="'+prefix+'catalog.html">מפתח הערכים</a></footer></body></html>\n')

def paragraph(v):return '<p>'+esc(v)+'</p>\n'

def make_page(name,title,desc,body,structured=None):
    (ROOT/name).write_text(head(title,desc,link(name),'assets/search-index.css',jsonld=structured)+shell_open()+body+shell_close(),encoding='utf-8')

# Publish a plain text catalog with real anchor URLs and a per-edition grouping.
entries=DATA['entries']
assert len(entries)==469 and len({e['key'] for e in entries})==469
catalog_body='<div class="eyebrow">THE INDEX · מפתח הערכים</div>\n<h1>מפתח ערכי השמות</h1>\n'
catalog_body+='<p>מפתח קריא ונגיש למנועי חיפוש של כל 469 הערכים בשני חיבוריו של ר׳ משה זכות. לחיפוש, תיוגים והשוואה פתחו כל ערך במהדורה האינטראקטיבית.</p>\n'
for code,title,subtitle in [('SH','אלפא ביתא של השמות','Alphabet of the Names'),('CFN','פירוש קצת שמות','Commentary on a Few Names')]:
    group=[e for e in entries if e['edition']['code']==code]
    catalog_body+=f'<section class="catalog-section"><h2>{esc(title)} <small lang="en">{esc(subtitle)}</small></h2><p>{len(group)} ערכים</p>\n<ol class="entry-index">\n'
    for e in group:
        catalog_body+=('<li><a href="entries/'+quote(e['key'])+'.html">'+esc(e['headword'])+'</a>'+
                       ' <small dir="ltr">'+esc(e['key'])+'</small></li>\n')
    catalog_body+='</ol></section>\n'
make_page('catalog.html','מפתח הערכים | זכות: האנטומיה של השם',
          'מפתח 469 ערכי השמות מתוך אלפא ביתא של השמות ופירוש קצת שמות של ר׳ משה זכות.',catalog_body)

# Minimal, crawlable text pages. Do not duplicate JS, source CSS, or JSON corpus on each page.
entriesdir=ROOT/'entries';entriesdir.mkdir(exist_ok=True)
for e in entries:
    key=e['key'];name=e.get('headword') or key; edition=e['edition']['code']
    work='אלפא ביתא של השמות' if edition=='SH' else 'פירוש קצת שמות'
    title=f'{name} | {work} | זכות'
    desc=f'הערך {name} מתוך {work} של ר׳ משה זכות. נוסח הערך וקישור למהדורה הדיגיטלית המתויגת.'
    route='#/edition?key='+quote(key)
    schema={'@context':'https://schema.org','@type':'CreativeWork', 'name':name,
            'inLanguage':'he','identifier':key,'isPartOf':{'@type':'CreativeWork','name':work},
            'author':{'@type':'Person','name':'ר׳ משה זכות'},'url':link('entries/'+key+'.html')}
    body='<nav class="breadcrumb"><a href="../catalog.html">כל הערכים</a> / '+esc(work)+'</nav>\n'
    body+='<div class="eyebrow">'+esc(key)+'</div>\n<h1>'+esc(name)+'</h1>\n'
    body+='<p class="entry-work">'+esc(work)+'</p>\n'
    body+='<article class="scholarly-text" lang="he" dir="rtl">'+esc(e['text'])+'</article>\n'
    body+=('<p class="read-cta"><a href="../'+route+'">פתיחת הערך במהדורה הדיגיטלית, עם תיוגים וכלי מחקר ←</a></p>\n')
    body+='<p class="seo-note">נוסח הערך מוצג לקריאה ולעיון. תיוגים, זיהויי ישויות, השוואה וחיפוש זמינים במהדורה האינטראקטיבית.</p>\n'
    (entriesdir/(key+'.html')).write_text(head(title,desc,link('entries/'+key+'.html'),'../assets/search-index.css',jsonld=schema)+shell_open(1)+body+shell_close(1),encoding='utf-8')

project=CONTENT['project']
body='<div class="eyebrow">PROJECT · הפרויקט</div><h1>'+esc(project['he']['lead'])+'</h1>\n'
for key in ('overview','second'):
    body+=paragraph(project['he'][key])
body+='<section lang="en" dir="ltr" class="en-section"><h2>'+esc(project['en']['lead'])+'</h2>\n'
for key in ('overview','second'):
    body+=paragraph(project['en'][key])
body+='</section>\n<p><a href="catalog.html">למפתח 469 הערכים ←</a></p>\n'
make_page('project.html','הפרויקט | זכות: האנטומיה של השם',project['he']['overview'],body,{
 '@context':'https://schema.org','@type':'ResearchProject','name':project['he']['lead'],'description':project['en']['overview'],'url':link('project.html')})

body='<div class="eyebrow">RESEARCH TEAM · צוות המחקר</div><h1>החוקרים וצוות הפרויקט</h1>\n'
body+='<div class="researchers">\n'
for person in CONTENT['team']:
    body+='<article class="researcher"><h2>'+esc(person['he'])+'</h2><div lang="en" dir="ltr">'+esc(person['en'])+'</div>\n'
    body+='<p>'+esc(person['position']['he'])+'</p><p lang="en" dir="ltr">'+esc(person['position']['en'])+'</p><p>'+esc(person['desc']['he'])+'</p>\n'
    if person.get('profile'):
        body+='<p><a href="'+esc(person['profile'])+'" rel="noopener noreferrer">פרופיל חיצוני</a></p>\n'
    body+='</article>\n'
body+='</div>\n'
make_page('people.html','החוקרים | זכות: האנטומיה של השם','צוות המחקר של המהדורה הדיגיטלית לחיבורי השמות של ר׳ משה זכות.',body)

body='<div class="eyebrow">PUBLICATIONS · מחקרים ופרסומים</div><h1>מחקרים ופרסומים</h1>\n'
for cat,label in [('project','פרסומי הפרויקט'),('related','מחקרים קשורים')]:
    papers=[p for p in CONTENT['papers'] if p['category']==cat]
    body+='<section class="publications-section"><h2>'+label+'</h2><ol class="paper-list">\n'
    for paper in papers:
        body+='<li><article><h3>'+esc(paper['he'])+'</h3>'
        body+='<p>'+esc(paper.get('authors_he',''))+' · '+esc(paper.get('year',''))+'</p>'
        body+='<p>'+esc(paper.get('journal',''))+'</p>'
        if paper.get('url'):
            body+='<p><a href="'+esc(paper['url'])+'" rel="noopener noreferrer">רשומת הפרסום / מקור מאומת ↗</a></p>'
        body+='</article></li>\n'
    body+='</ol></section>\n'
make_page('publications.html','פרסומים ומחקרים | זכות: האנטומיה של השם',
          'ספרים ומאמרים על ר׳ משה זכות, חיבורי השמות וקבלה לוריאנית, מתוך פרסומי הפרויקט ומחקרים קשורים.',body)

# Small, standalone stylesheet for added search entry points. App stylesheet unchanged.
css='''/* Search-only documents. Original interactive app assets remain untouched. */
:root{--paper:#f5f2ec;--ink:#112a3b;--faint:#69737a;--accent:#af5448;--rule:#ded7cc}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.85 "Noto Sans Hebrew",Arial,sans-serif;direction:rtl}a{color:var(--ink);text-underline-offset:4px}a:hover{color:var(--accent)}.seo-header{border-bottom:1px solid var(--rule);padding:18px max(24px,calc((100vw - 1130px)/2));display:flex;gap:24px;align-items:center;justify-content:space-between;flex-wrap:wrap}.seo-brand a{text-decoration:none;font:bold 21px Georgia,serif;letter-spacing:.09em}.seo-brand small{display:block;font:9px Arial,sans-serif;letter-spacing:.24em}.seo-header nav{display:flex;gap:16px;flex-wrap:wrap;font-size:13px}.seo-container{max-width:990px;margin:0 auto;padding:60px 26px 100px}.eyebrow{font:700 11px Arial,sans-serif;letter-spacing:.17em;color:var(--accent);margin-bottom:18px}h1,h2,h3{font-family:"Noto Serif Hebrew",David,serif;font-weight:500;line-height:1.4}h1{font-size:clamp(34px,5vw,58px);margin:.1em 0 .45em}h2{font-size:30px}h3{font-size:21px;margin:.1em 0}h2 small{display:block;font:400 14px Arial;color:var(--faint);margin-top:4px}p{max-width:800px}.breadcrumb{font-size:13px;color:var(--faint);margin-bottom:28px}.entry-work{color:var(--faint)}.scholarly-text{padding:30px 28px;margin:35px 0 30px;background:#fffcf6;border-right:3px solid var(--accent);box-shadow:0 12px 34px rgba(25,40,46,.04);white-space:pre-wrap;overflow-wrap:anywhere;font:23px/2.15 "Noto Serif Hebrew",David,serif}.read-cta{padding:12px 0;font-weight:600}.seo-note{color:var(--faint);font-size:13px}.catalog-section{border-top:1px solid var(--rule);padding-top:22px;margin-top:52px}.entry-index{columns:3;column-gap:32px;padding-inline-start:24px}.entry-index li{break-inside:avoid;padding:2px 0 4px;overflow-wrap:anywhere}.entry-index small{color:var(--faint);font:11px Arial,sans-serif;white-space:nowrap}.researchers{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px}.researcher{border-top:1px solid var(--rule);padding:15px 0}.researcher p{margin:6px 0}.en-section{border-top:1px solid var(--rule);padding:25px 0;margin-top:30px}.paper-list{padding-inline-start:23px}.paper-list li{margin:12px 0 28px;padding-inline-start:12px;border-bottom:1px solid var(--rule)}.paper-list p{margin:5px 0}.publications-section{padding-top:15px}.seo-footer{border-top:1px solid var(--rule);padding:22px;text-align:center;color:var(--faint);font-size:12px}@media(max-width:700px){.seo-container{padding:30px 20px 65px}.seo-header{padding:14px 20px}.seo-header nav{gap:10px}.entry-index{columns:2}.researchers{grid-template-columns:1fr}.scholarly-text{font-size:21px;padding:18px 14px}}@media(max-width:440px){.entry-index{columns:1}}
'''
(ROOT/'assets/search-index.css').write_text(css,encoding='utf-8')

# Index SEO metadata additions only; preserve original visual elements and JS loading.
index=(ROOT/'index.html').read_text(encoding='utf-8')
index=index.replace('<title>ZACUT · Anatomy of a Name</title>',
 '<title>זכות: האנטומיה של השם | מהדורה דיגיטלית וסביבת מחקר</title>\n'
 '<link rel="canonical" href="'+SITE_URL+'">\n'
 '<meta name="robots" content="index,follow">\n'
 '<link rel="sitemap" type="application/xml" href="sitemap.xml">')
index=index.replace('</body>', '<noscript><p>לגישה לטקסטים ללא JavaScript: <a href="catalog.html">מפתח כל ערכי השמות</a>. '
 '<a href="project.html">הפרויקט</a> · <a href="publications.html">פרסומים</a>.</p></noscript>\n</body>')
(ROOT/'index.html').write_text(index,encoding='utf-8')

# XML sitemap: only crawlable HTTP URLs, not SPA hash routes.
NS='http://www.sitemaps.org/schemas/sitemap/0.9'
urlset=Element('urlset',xmlns=NS)
urls=['','catalog.html','project.html','people.html','publications.html']+['entries/'+e['key']+'.html' for e in entries]
for rel in urls:
    SubElement(SubElement(urlset,'url'),'loc').text=link(rel)
(ROOT/'sitemap.xml').write_bytes(b'<?xml version="1.0" encoding="UTF-8"?>\n'+tostring(urlset,encoding='utf-8')+b'\n')
# A robots.txt at /zacut/ is not the hostname robots policy, which must be at the origin root.
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /zacut/\n\nSitemap: '+link('sitemap.xml')+'\n',encoding='utf-8')

readme='''# ZACUT 15.2 | Google discoverability and degree titles

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
'''
(ROOT/'README.md').write_text(readme,encoding='utf-8')

# Construct a compact preview with updated team content but original runtime, styles, and corpus.
old_preview=BASE.read_text(encoding='utf-8')
preview_content=copy.deepcopy(CONTENT)
for person in preview_content['team']:
    if person['id']=='chen':
        person['portrait_url']='data:image/jpeg;base64,'+base64.b64encode((ROOT/'assets/people/chen-avizohar-hagay.jpg').read_bytes()).decode('ascii')
inline_site=json.dumps(preview_content,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
pattern=r'(window\.__ZACUT_SITE__=).*?(;window\.__ZACUT_DATA__=)'
new_preview,n=re.subn(pattern,lambda m:m.group(1)+inline_site+m.group(2),old_preview,count=1,flags=re.S)
assert n==1
new_preview=new_preview.replace('<title>ZACUT · Anatomy of a Name</title>',
  '<title>זכות: האנטומיה של השם | גרסה 15.2</title>')
(Path('/mnt/data/zacut-machine-v15-2-preview.html')).write_text(new_preview,encoding='utf-8')

# Artifact used for reproduction, optional if the site content changes later.
# Copy this generator to the release so its added search pages can be recreated.
tools=ROOT/'tools';tools.mkdir(exist_ok=True)
(tools/'build-release-v15-2.py').write_bytes(Path(__file__).read_bytes())

out=Path('/mnt/data/zacut-machine-v15-2-github.zip')
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for f in sorted(ROOT.rglob('*')):
        if f.is_file():z.write(f, f.relative_to(ROOT).as_posix())
print('generated',len(urls),'sitemap URLs,',len(list(entriesdir.glob('*.html'))),'entry HTML, ZIP',out.stat().st_size,'preview',len(new_preview))
