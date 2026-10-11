"""Optional, dependency-free editorial tool. Generated HTML is committed and deploys as-is."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT/'assets/data'
STRINGS = json.loads((DATA/'translations.json').read_text(encoding='utf-8'))
MEDIA = json.loads((DATA/'media.json').read_text(encoding='utf-8'))
QUIZZES = json.loads((DATA/'quizzes.json').read_text(encoding='utf-8'))
CONTENT = []
for filename, kind, folder in [('destinations','destinations','places'),('foods','foods','dishes'),('culture','cultures','stories')]:
    for item in json.loads((DATA/f'{filename}.json').read_text(encoding='utf-8')):
        CONTENT.append(dict(item, kind=kind, href=f"{folder}/{item['id']}.html"))
BY_ID = {item['id']:item for item in CONTENT}
esc = lambda value: html.escape(str(value), quote=True)
T = lambda key: esc(STRINGS[key]['ar'])

ICONS = {
 'arch':'<path d="M4 21V10a8 8 0 0 1 16 0v11M8 21V10a4 4 0 0 1 8 0v11M2 21h20"/>',
 'pin':'<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/>',
 'plate':'<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="5"/><path d="M1 3v6m2-6v6M1 9h2v12M23 3v18"/>',
 'spark':'<path d="m12 2 2.5 7.5L22 12l-7.5 2.5L12 22l-2.5-7.5L2 12l7.5-2.5Z"/>',
 'heart':'<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8Z"/>',
 'search':'<circle cx="10.5" cy="10.5" r="7"/><path d="m16 16 5 5"/>',
 'arrow':'<path d="M4 12h16m-6-6 6 6-6 6"/>',
 'down':'<path d="M12 3v18m-6-6 6 6 6-6"/>',
 'menu':'<path d="M3 6h18M3 12h18M3 18h18"/>',
 'close':'<path d="m5 5 14 14M5 19 19 5"/>',
 'moon':'<path d="M21 13a9 9 0 0 1-10-10 9 9 0 1 0 10 10Z"/>',
 'sun':'<circle cx="12" cy="12" r="4"/><path d="M12 1v2m0 18v2M1 12h2m18 0h2M4 4l1.5 1.5m13 13L20 20M4 20l1.5-1.5m13-13L20 4"/>'
}
def icon(name, extra=''):
    return f'<svg class="icon {extra}" aria-hidden="true" viewBox="0 0 24 24"><use href="#icon-{name}"></use></svg>'
def symbols():
    return '<svg class="symbols" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">'+''.join(f'<symbol id="icon-{name}" viewBox="0 0 24 24">{paths}</symbol>' for name,paths in ICONS.items())+'</svg>'
def text(key, tag='span', cls=''):
    return f'<{tag} class="{cls}" data-i18n="{key}">{T(key)}</{tag}>'
def field(item, key, tag='p', cls='', index=None):
    value = item[key]['ar'] if index is None else item[key]['ar'][index]
    path = f"{item['id']}.{key}" + (f'.{index}' if index is not None else '')
    return f'<{tag} class="{cls}" data-content="{path}">{esc(value)}</{tag}>'
def photo(item, prefix='', large=False, eager=False, cls=''):
    asset = MEDIA.get(item.get('photo',item['id']))
    file = asset['large' if large else 'file'] if asset else f"assets/images/{item['id']}.svg"
    sizes = '(max-width: 700px) calc(100vw - 32px), 640px' if large else '(max-width: 480px) calc(100vw - 34px), (max-width: 999px) calc((100vw - 74px) / 2), 400px'
    srcset = f' srcset="{prefix}{asset["file"]} 640w, {prefix}{asset["large"]} 1600w" sizes="{sizes}"' if asset else ''
    return f'<img class="{cls}" src="{prefix}{esc(file)}"{srcset} alt="{esc(item["name"]["ar"])}" data-alt-content="{item["id"]}" data-fallback-alt="{T("imageUnavailable")}" width="640" height="440" loading="{"eager" if eager else "lazy"}">'
def card(item, prefix='', heading='h2'):
    return f'''<article class="card" data-id="{item['id']}" data-category="{item['category']}" data-kind="{item['kind']}">
      <div class="card-image">{photo(item,prefix)}<button class="favorite-button js-only" type="button" data-favorite="{item['id']}" aria-label="{T('save')}: {esc(item['name']['ar'])}" aria-pressed="false">{icon('heart')}</button></div>
      <div class="card-content">{text(item['category'],'p','eyebrow')}<{heading} class="card-title"><a href="{prefix}{item['href']}" data-content="{item['id']}.name">{esc(item['name']['ar'])}</a></{heading}>
      {field(item,'description','p','card-description')}<div class="card-actions"><a class="text-link" href="{prefix}{item['href']}">{text('read')}{icon('arrow')}</a><button class="quick-button" type="button" data-preview="{item['id']}" data-i18n="quickView">{T('quickView')}</button></div></div></article>'''
NAV = [('index.html','home'),('explore.html','explore'),('food.html','food'),('culture.html','culture'),('quiz.html','quiz')]
def brand(prefix=''):
    return f'<a class="brand" href="{prefix}index.html"><svg class="brand-mark icon" aria-hidden="true" viewBox="0 0 24 24"><use href="#icon-arch"></use></svg><span><b class="brand-name">syria<span>.fun</span></b>{text("brandLine","small","brand-tag")}</span></a>'
def header(page, prefix):
    links = ''.join(f'<a href="{prefix}{path}" data-i18n="{key}"'+(' aria-current="page"' if key==page else '')+f'>{T(key)}</a>' for path,key in NAV)
    return f'''<header class="site-header"><div class="container header-inner">{brand(prefix)}<nav id="main-navigation" class="main-navigation" aria-label="{T('navigation')}" data-i18n-aria-label="navigation">{links}<a class="mobile-only" href="{prefix}search.html" data-i18n="search">{T('search')}</a><a class="mobile-only" href="{prefix}about.html" data-i18n="about">{T('about')}</a></nav>
    <div class="header-actions"><a class="icon-button header-search" href="{prefix}search.html" aria-label="{T('search')}" data-i18n-aria-label="search">{icon('search')}</a>
    <a class="icon-button favorite-link" href="{prefix}favorites.html" aria-label="{T('favorites')}" data-i18n-aria-label="favorites">{icon('heart')}<span class="count-badge js-only" data-favorites-count>٠</span></a>
    <button class="language-toggle js-only" id="language-toggle" type="button" aria-label="Switch to English" lang="en">EN</button>
    <button class="icon-button js-only" id="theme-toggle" type="button" aria-label="{T('theme')}" aria-pressed="false">{icon('moon','moon')}{icon('sun','sun')}</button>
    <button class="icon-button menu-toggle js-only" id="menu-toggle" type="button" aria-label="{T('menu')}" aria-controls="main-navigation" aria-expanded="false">{icon('menu')}</button></div></div></header>'''
def footer(prefix):
    return f'''<footer class="site-footer"><div class="container"><div class="footer-grid"><div class="footer-brand">{brand(prefix)}{text('footerIntro','p')}</div><div class="footer-column">{text('footerExplore','h2')}{''.join(f'<a href="{prefix}{path}" data-i18n="{key}">{T(key)}</a>' for path,key in NAV[1:])}</div><div class="footer-column">{text('footerProject','h2')}<a href="{prefix}about.html" data-i18n="about">{T('about')}</a><a href="{prefix}favorites.html" data-i18n="favorites">{T('favorites')}</a><a href="{prefix}credits.html" data-i18n="photoCredits">{T('photoCredits')}</a><a href="https://github.com/abderlahmanalhnedi/syria.fun">GitHub ↗</a></div></div><div class="footer-bottom">{text('footerNote','span')}<span dir="ltr">© 2026 Syria.fun</span></div></div></footer>'''
def page_heading(title, intro, eyebrow='eyebrow'):
    return f'<div class="page-heading">{text(eyebrow,"p","eyebrow")}{text(title,"h1")}{text(intro,"p","lead")}</div>'
def document(path, page, title_key, desc_key, body, item=None, noindex=False):
    prefix = '../' if '/' in path else ''
    title = (item['name']['ar'] if item else STRINGS[title_key]['ar'])+' | Syria.fun'
    desc = item['description']['ar'] if item else STRINGS[desc_key]['ar']
    canonical = 'https://syria.fun/'+('' if path=='index.html' else path)
    schema = {'@context':'https://schema.org','@type':'WebPage','name':title,'description':desc,'url':canonical,'inLanguage':'ar','isPartOf':{'@type':'WebSite','name':'Syria.fun','url':'https://syria.fun/'}}
    if path=='index.html': schema={'@context':'https://schema.org','@type':'WebSite','name':'Syria.fun','url':canonical,'inLanguage':['ar','en'],'description':desc}
    schema_json = json.dumps(schema,ensure_ascii=False).replace('<', '\\u003c')
    html_doc = f'''<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}"><link rel="canonical" href="{canonical}">
<meta name="color-scheme" content="light dark"><meta name="theme-color" content="#126b67">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canonical}"><meta property="og:locale" content="ar_SY"><meta property="og:site_name" content="Syria.fun"><meta property="og:image" content="https://syria.fun/assets/images/share.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="https://syria.fun/assets/images/share.jpg">
{'<meta name="robots" content="noindex, follow">' if noindex else ''}<link rel="icon" href="{prefix}assets/icons/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="{prefix}assets/icons/apple-touch-icon.png">
<link rel="preload" href="{prefix}assets/fonts/font-0.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="{prefix}assets/fonts/font-2.woff2" as="font" type="font/woff2" crossorigin><script src="{prefix}assets/js/boot.js"></script><link rel="stylesheet" href="{prefix}assets/css/site.css">
<script type="application/ld+json">{schema_json}</script><script type="module" src="{prefix}assets/js/main.js"></script></head>
<body data-page="{page}" data-title="{title_key}" data-description="{desc_key}"{f' data-item="{item["id"]}"' if item else ''}>
<a class="skip-link" href="#main-content" data-i18n="skip">{T('skip')}</a>{symbols()}{header(page,prefix)}
<noscript><p class="noscript">{T('noScript')}</p></noscript><div id="app-error" class="error-banner container" hidden role="alert">{text('loadError')} <button id="retry-load" type="button" class="text-button" data-i18n="retry">{T('retry')}</button></div>
<main id="main-content" tabindex="-1">{body}</main>{footer(prefix)}
<dialog id="detail-dialog" aria-labelledby="dialog-title"><div class="dialog-inner"><button class="icon-button dialog-close" type="button" data-close-dialog aria-label="{T('close')}" data-i18n-aria-label="close" autofocus>{icon('close')}</button><div id="dialog-content"></div></div></dialog>
<div id="live-status" class="live-status" role="status" aria-live="polite" aria-atomic="true"></div></body></html>'''
    destination=ROOT/path
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(html_doc+'\n',encoding='utf-8')

def home():
    journey=''
    for key,label,count,ico in [('explore','explore','placesCount','pin'),('food','food','foodsCount','plate'),('culture','culture','cultureCount','arch'),('quiz','quiz','quizCount','spark')]:
        journey+=f'<a class="journey-link" href="{key}.html"><span class="journey-icon">{icon(ico)}</span><span>{text(label,"strong")}{text(count,"small")}</span></a>'
    body=f'''<div class="hero-wrap"><section class="hero" aria-labelledby="hero-title"><picture><source media="(max-width: 700px)" srcset="assets/images/damascus-hero-mobile.webp"><img class="hero-image" src="assets/images/damascus-1600.webp" alt="{T('heroAlt')}" data-i18n-alt="heroAlt" data-fallback-alt="{T("imageUnavailable")}" width="1600" height="1200" fetchpriority="high"></picture><div class="container"><div class="hero-content">{text('eyebrow','p','eyebrow')}<h1 id="hero-title" data-i18n="homeTitle">{T('homeTitle')}</h1>{text('homeIntro','p','lead')}<div class="button-row"><a class="button primary" href="explore.html">{text('start')}{icon('arrow','arrow')}</a><a class="button secondary" href="quiz.html">{text('quiz')}</a></div></div></div><a class="hero-scroll" href="#discover">{icon('down')}{text('scroll')}</a><div class="hero-caption">{text('heroPlace')}{text('heroDate')}</div></section></div>
    <div class="container"><nav class="discovery-strip" aria-label="{T('journey')}" data-i18n-aria-label="journey">{journey}</nav>
    <form class="home-search" action="search.html" method="get"><label><span class="search-label" data-i18n="search">{T('search')}</span><span class="search-field">{icon('search')}<input name="q" type="search" placeholder="{T('searchHint')}" data-i18n-placeholder="searchHint" aria-label="{T('search')}" data-i18n-aria-label="search"></span></label><button class="button secondary" type="submit">{text('search')}</button></form></div>
    <section id="discover" class="container section"><div class="section-heading"><div>{text('featuredLabel','p','eyebrow')}{text('featuredTitle','h2')}{text('featuredIntro','p')}</div><a class="text-link" href="explore.html">{text('allPlaces')}{icon('arrow')}</a></div><div class="grid">{''.join(card(BY_ID[id],heading='h3') for id in ['damascus','aleppo','hama'])}</div></section>
    <section class="surface-section section"><div class="container food-feature"><div class="food-feature-image">{photo(BY_ID['kibbeh'],large=True)}<a class="food-feature-label" href="dishes/kibbeh.html" data-content="kibbeh.name">{esc(BY_ID['kibbeh']['name']['ar'])}</a></div><div>{text('tableLabel','p','eyebrow')}{text('tableTitle','h2')}{text('tableIntro','p','lead')}<div class="food-preview">{''.join(f'<a href="dishes/{id}.html" data-content="{id}.name">{esc(BY_ID[id]["name"]["ar"])}</a>' for id in ['fattoush','halawet-el-jibn','maarouk'])}</div><div class="button-row"><a class="button primary" href="food.html">{text('allFood')}{icon('arrow','arrow')}</a></div></div></div></section>
    <section class="container section"><div class="section-heading"><div>{text('cultureLabel','p','eyebrow')}{text('cultureTitle','h2')}{text('cultureIntro','p')}</div><a class="text-link" href="culture.html">{text('allCulture')}{icon('arrow')}</a></div><div class="grid culture-grid">{''.join(card(BY_ID[id],heading='h3') for id in ['crafts','music-dabke'])}</div></section>
    <section class="container challenge"><div>{text('challengeLabel','p','eyebrow')}{text('challengeTitle','h2')}{text('challengeIntro','p')}</div><a class="button" href="quiz.html?quiz=cities">{text('tryQuiz')}{icon('arrow','arrow')}</a><span class="challenge-decoration" aria-hidden="true"></span></section>
    <section class="container section"><div class="section-heading">{text('factsTitle','h2')}</div><div class="facts-grid">{''.join(f'<article class="fact-item"><span class="fact-number" dir="ltr">0{n}</span>{text(f"fact{n}","p")}<a class="text-link" href="{href}">{text(label)}{icon("arrow")}</a></article>' for n,href,label in [(1,'places/hama.html','explore'),(2,'places/bosra.html','explore'),(3,'stories/crafts.html','culture')])}</div></section>'''
    document('index.html','home','homeTitle','homeIntro',body)

def catalog(page, title, intro, kind, filters):
    items=CONTENT if kind is None else [item for item in CONTENT if item['kind']==kind]
    controls=f'''<section class="search-controls js-only" aria-label="{T('search')}"><label class="search-label" for="catalog-search" data-i18n="search">{T('search')}</label><div class="search-input-row"><div class="search-field">{icon('search')}<input id="catalog-search" type="search" placeholder="{T('searchHint')}" data-i18n-placeholder="searchHint" aria-controls="catalog-grid" autocomplete="off"></div><button class="button secondary" id="clear-search" type="button" data-i18n="clear">{T('clear')}</button></div><div class="filters" role="group" aria-label="{T('filter')}" data-i18n-aria-label="filter">{''.join(f'<button class="filter-button" type="button" data-filter="{key}" data-i18n="{key}" aria-pressed="{str(key=="all").lower()}">{T(key)}</button>' for key in ['all']+filters)}</div><output id="result-count" class="result-count" aria-live="polite" aria-atomic="true"></output></section>'''
    empty=f'<div id="no-results" class="no-results" hidden>{icon("search")}{text("noResults","h2")}{text("noResultsIntro","p")}</div>'
    cls=' culture-grid' if page=='culture' else ''
    note='foodNote' if page=='food' else 'photoNote'
    body=f'<div class="container">{page_heading(title,intro)}{controls}<section class="catalog-section" aria-label="{T(title)}" data-i18n-aria-label="{title}"><div id="catalog-grid" class="grid{cls}">{"".join(card(item) for item in items)}</div>{empty}{text(note,"p","note")}</section></div>'
    document(f'{page}.html',page,title,intro,body,noindex=page=='search')

def details():
    for item in CONTENT:
        parent={'destinations':'explore','foods':'food','cultures':'culture'}[item['kind']]
        asset=MEDIA.get(item.get('photo',item['id']))
        caption=(text('archival')+' · '+(esc(asset['date']) if asset['date'] else text('dateUnknown'))+' · '+esc(asset['author'])+f' · <a href="{esc(asset["source"])}">{T("photoCredits")}</a>') if asset else text('illustration')
        highlights=''.join(field(item,'highlights','li',index=i) for i in range(len(item['highlights']['ar'])))
        body=f'''<div class="container"><div class="detail-heading"><nav class="breadcrumb" aria-label="{T('back')}" data-i18n-aria-label="back"><a href="../{parent}.html" data-i18n="{parent}">{T(parent)}</a>{icon('arrow')}<span data-content="{item['id']}.name">{esc(item['name']['ar'])}</span></nav></div><article><div class="detail-layout"><figure class="detail-photo">{photo(item,'../',large=True,eager=True)}<figcaption>{caption}</figcaption></figure><div class="detail-summary">{text(item['category'],'p','eyebrow')}{field(item,'name','h1')}{field(item,'subtitle','p','lead')}{field(item,'description','p','lead')}<div class="button-row"><button class="button secondary detail-favorite js-only" type="button" data-favorite="{item['id']}" aria-pressed="false" aria-label="{T('save')}">{icon('heart')}{text('save')}</button></div></div></div><div class="detail-story"><div class="story-body">{field(item,'body')}{text('ingredients' if item['kind']=='foods' else 'highlights','h2')}<ul class="highlights">{highlights}</ul>{text('source','h2')}<div class="source-list"><a href="{esc(item['source'])}">{esc(urllib_host(item['source']))} ↗</a><a href="../credits.html" data-i18n="photoCredits">{T('photoCredits')}</a></div>{text('foodNote' if item['kind']=='foods' else 'photoNote','p','note')}</div><aside class="fact-box">{text('didYouKnow','h2')}{field(item,'fact')}</aside></div></article></div>'''
        document(item['href'],parent,'homeTitle','homeIntro',body,item=item)
def urllib_host(url):
    from urllib.parse import urlparse
    return urlparse(url).netloc

def favorites():
    body=f'''<div class="container">{page_heading('favoritesTitle','favoritesIntro')}<p class="note" data-i18n="localOnly">{T('localOnly')}</p><section class="section"><div id="favorites-grid" class="grid"></div><div id="favorites-empty" class="empty-state">{icon('heart')}{text('emptyFavorites','h2')}{text('emptyFavoritesIntro','p')}<div class="button-row"><a class="button primary" href="explore.html" data-i18n="start">{T('start')}</a></div></div></section></div>'''
    document('favorites.html','favorites','favoritesTitle','favoritesIntro',body,noindex=True)
def quiz():
    cards=''
    for item in QUIZZES:
        id=item['id']
        cards+=f'''<article class="quiz-card"><div class="journey-icon">{icon(item['icon'])}</div><h2 data-quiz-text="{id}.name">{esc(item['name']['ar'])}</h2><p data-quiz-text="{id}.description">{esc(item['description']['ar'])}</p><div class="quiz-stats">{text('questions')}<span data-best="{id}">{T('best')}: ٠ / ٥</span></div><button class="button primary js-only" type="button" data-start-quiz="{id}" data-i18n="startQuiz">{T('startQuiz')}</button></article>'''
    body=f'<div class="container">{page_heading("quizTitle","quizIntro")}<section id="quiz-selection" class="quiz-grid catalog-section">{cards}</section><section id="quiz-panel" class="quiz-panel" aria-label="{T("quiz")}" data-i18n-aria-label="quiz" hidden></section></div>'
    document('quiz.html','quiz','quizTitle','quizIntro',body)
def about():
    sections=''.join(text(title,'h2')+text(body,'p') for title,body in [('aboutMissionTitle','aboutMission'),('aboutHowTitle','aboutHow'),('aboutEditorialTitle','aboutEditorial')])
    body=f'''<div class="container">{page_heading('aboutTitle','aboutIntro')}<div class="about-layout catalog-section"><article class="about-content">{sections}<div class="button-row"><a class="button primary" href="https://github.com/abderlahmanalhnedi/syria.fun/issues" data-i18n="contribute">{T('contribute')}</a></div></article><aside class="about-visual"><img src="assets/images/about.svg" alt="{T('aboutAlt')}" data-i18n-alt="aboutAlt" data-fallback-alt="{T("imageUnavailable")}" width="640" height="440" loading="lazy">{text('privacyTitle','h2')}{text('privacy','p')}<p><a class="text-link" href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" data-i18n="githubPrivacy">{T('githubPrivacy')}</a></p></aside></div></div>'''
    document('about.html','about','aboutTitle','aboutIntro',body)
def credits():
    cards=''
    lines=['# Image credits / مصادر الصور','', 'Verified from Wikimedia Commons imageinfo metadata on 2026-10-11. Files are stored locally, resized, converted to WebP, and may be cropped by CSS. Archival dates are recorded; photos do not establish current conditions. No endorsement is implied.','', '| Local files (640 / 1600) | Creator | Source | License | Capture date |','| --- | --- | --- | --- | --- |']
    for id,asset in MEDIA.items():
        item=BY_ID[id]
        date=esc(asset['date']) if asset['date'] else text('dateUnknown')
        cards+=f'<article class="credit-card">{photo(item)}{field(item,"name","h2")}<p>{esc(asset["author"])} · {date}</p><p><a href="{esc(asset["source"])}" data-i18n="source">{T("source")}</a> · <a href="{esc(asset["license_url"])}">{esc(asset["license"])}</a></p></article>'
        lines.append(f'| `{id}-640.webp`, `{id}-1600.webp` | {asset["author"]} | [Original file]({asset["source"]}) | [{asset["license"]}]({asset["license_url"]}) | {asset["date"][:10] or "Not recorded"} |')
    lines+=['','`damascus-hero-mobile.webp` is a 720 × 1080 portrait crop of the same Vyacheslav Argenberg photograph credited in the Damascus row, under CC BY 4.0.','', 'All CC BY-SA derivatives remain under the license shown above. Other site code is MIT licensed; third-party assets are excluded from that grant.','', '## Original artwork','', 'The SVG illustrations, favicon, and share-image composition are original Syria.fun artwork (MIT). Food illustrations are interpretive, not photographs of a particular recipe. Culture illustrations are symbolic and do not claim to reproduce an actual monument.','', '## Fonts','', 'Cairo and Inter are self-hosted from Google Fonts. Both use the SIL Open Font License 1.1. License texts: `assets/fonts/cairo-OFL.txt` and `assets/fonts/inter-OFL.txt`.','', '## مصادر الصور','', 'الصور محفوظة محلياً مع أسماء أصحابها وروابط المصدر والترخيص أعلاه. جرى تصغيرها وتحويلها إلى WebP، وقد تُقص في العرض. الصور أرشيفية، والرسوم توضيحية أصلية. تبقى الصور المشتقة ذات ترخيص المشاركة بالمثل خاضعة للترخيص الأصلي.']
    (ROOT/'PHOTO_CREDITS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    body=f'<div class="container">{page_heading("creditsTitle","creditsIntro")}{text("creditsIllustrations","p","note")}<section class="section credit-list">{cards}</section></div>'
    document('credits.html','credits','creditsTitle','creditsIntro',body)
def illustrations():
    folder=ROOT/'assets/images'
    for item in CONTENT:
        if item.get('photo',item['id']) in MEDIA: continue
        id=item['id']
        bg='#ebe9df'; accent='#c79b5a'; dark='#2c6963'
        if item['kind']=='foods':
            art='<ellipse cx="320" cy="238" rx="190" ry="138" fill="#fffdf5" stroke="#d4d9cd" stroke-width="8"/><ellipse cx="320" cy="238" rx="157" ry="111" fill="#eee8d4"/>'
            if id in ('tabbouleh','molokhia'):
                for x,y in [(230,210),(290,180),(350,195),(400,220),(250,260),(320,270),(375,270),(310,230),(210,235)]:
                    art+=f'<ellipse cx="{x}" cy="{y}" rx="35" ry="22" fill="{dark}" transform="rotate({x%40} {x} {y})"/>'
                art+='<circle cx="280" cy="240" r="14" fill="#c4654d"/><circle cx="365" cy="240" r="14" fill="#c4654d"/><circle cx="390" cy="190" r="13" fill="#d8ae68"/>'
            elif id=='mahshi':
                for x,y,r in [(245,215,-25),(315,245,20),(385,220,-10)]:
                    art+=f'<rect x="{x-26}" y="{y-55}" width="52" height="110" rx="22" fill="#6d8955" transform="rotate({r} {x} {y})"/><ellipse cx="{x}" cy="{y-45}" rx="18" ry="8" fill="#e4c99d"/>'
            elif id=='maarouk':
                art+='<ellipse cx="320" cy="235" rx="130" ry="86" fill="#b6773e"/><ellipse cx="320" cy="225" rx="117" ry="74" fill="#d8ae68"/><path d="M250 190q70 55 145 0M225 228q95 65 190 0" stroke="#9a5e36" stroke-width="6" fill="none"/>'
                for x,y in [(260,210),(290,185),(335,200),(370,185),(350,250),(280,255),(390,235)]: art+=f'<ellipse cx="{x}" cy="{y}" rx="4" ry="8" fill="#fff0ce" transform="rotate(30 {x} {y})"/>'
            else:
                for x,y in [(215,190),(310,190),(405,190),(260,280),(355,280)]: art+=f'<path d="m{x} {y-45} 55 45-55 45-55-45Z" fill="#d8ae68" stroke="#a37639" stroke-width="3"/><path d="m{x-38} {y} 38 30 38-30" fill="none" stroke="#f5d99a" stroke-width="5"/><circle cx="{x}" cy="{y-4}" r="7" fill="#789057"/>'
        else:
            art='<circle cx="460" cy="115" r="54" fill="#d8ae68" opacity=".45"/><path d="M0 375Q145 260 310 345T640 320V440H0Z" fill="#cfdacf"/>'
            if id=='crafts': art+='<path d="M285 90h70v50q0 25 35 58c80 83 15 145-70 145s-150-62-70-145q35-33 35-58Z" fill="#126b67"/><path d="M291 180q-43 65-23 93" fill="none" stroke="#91b4a4" stroke-width="8"/><path d="M274 296q44 24 94 0" stroke="#d8ae68" stroke-width="7" fill="none"/>'
            elif id=='music-dabke': art+='<ellipse cx="290" cy="255" rx="89" ry="107" fill="#c79b5a" transform="rotate(-25 290 255)"/><path d="m323 184 84-116 20 13-80 130" fill="#7a553c"/><circle cx="290" cy="253" r="24" fill="#475541"/><path d="m250 305 170-229m-160 238L427 82m-158 237L435 88" stroke="#eadbb4" stroke-width="3"/>'
            elif id=='calligraphy': art+='<rect x="170" y="100" width="290" height="250" rx="8" fill="#fffdf5"/><path d="M224 238q52 83 82 4l-4-80m22 95q72 10 72-72m-59 17 42-50M224 305h176" fill="none" stroke="#126b67" stroke-width="10" stroke-linecap="round"/><path d="m465 85-90 155" stroke="#875a38" stroke-width="12"/><path d="m375 240-17 28 1-34" fill="#101c2c"/>'
            else: art+='<path d="M150 365V190a85 85 0 0 1 170 0v175M352 365V237a65 65 0 0 1 130 0v128" fill="#d8ae68"/><path d="M190 365V195a45 45 0 0 1 90 0v170M383 365V238a34 34 0 0 1 68 0v127" fill="#126b67"/><path d="M95 365h450M120 385h400" stroke="#78968a" stroke-width="8"/><path d="M520 350V190m0 60q-70-55-50-85m50 60q65-65 55-95" fill="none" stroke="#789057" stroke-width="10"/>'
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 440"><rect width="640" height="440" fill="{bg}"/>{art}</svg>'
        (folder/f'{id}.svg').write_text(svg,encoding='utf-8')
    (folder/'about.svg').write_text((folder/'hospitality.svg').read_text(encoding='utf-8'),encoding='utf-8')
    (folder/'fallback.svg').write_text((folder/'hospitality.svg').read_text(encoding='utf-8'),encoding='utf-8')
    icons=ROOT/'assets/icons';icons.mkdir(parents=True,exist_ok=True)
    (icons/'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#126b67"/><path d="M16 49V28a16 16 0 0 1 32 0v21M24 49V28a8 8 0 0 1 16 0v21M12 49h40" fill="none" stroke="#efd5a7" stroke-width="3"/></svg>',encoding='utf-8')

def build():
    css='\n'.join((ROOT/f'assets/css/{name}.css').read_text(encoding='utf-8') for name in ['fonts','main','components','responsive'])
    (ROOT/'assets/css/site.css').write_text(css,encoding='utf-8')
    illustrations()
    home()
    catalog('explore','exploreTitle','exploreIntro','destinations',['heritage','central','coast','river','mountain'])
    catalog('food','foodTitle','foodIntro','foods',['mains','salads','street','sweets'])
    catalog('culture','culturePageTitle','culturePageIntro','cultures',['everyday','craft','heritage','arts'])
    catalog('search','searchTitle','searchIntro',None,['destinations','foods','cultures'])
    details(); favorites(); quiz(); about(); credits()
    document('404.html','404','notFoundTitle','notFoundIntro',f'<div class="container section">{page_heading("notFoundTitle","notFoundIntro")}<a class="button primary" href="index.html" data-i18n="home">{T("home")}</a></div>',noindex=True)
    # Pages serves this file at the missing URL; absolute custom-domain assets avoid nested 404 breakage.
    missing=ROOT/'404.html'
    source=missing.read_text(encoding='utf-8').replace('<head>', '<head><base href="https://syria.fun/">')
    missing.write_text(source,encoding='utf-8')
    paths=['index.html','explore.html','food.html','culture.html','quiz.html','about.html','credits.html']+[item['href'] for item in CONTENT]
    urls=''.join(f'<url><loc>https://syria.fun/{"" if path=="index.html" else path}</loc></url>' for path in paths)
    (ROOT/'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n',encoding='utf-8')
    print(f'Generated {len(paths)+3} static pages, sitemap, illustrations, and image credits.')

if __name__=='__main__': build()
