#!/usr/bin/env python3
"""
My Craft Games – SEO / LLM build step.  Run from the repository root AFTER building the game pages:

    python3 tools/seo.py            # everything (needs Node.js and, for prerender + images, Playwright)
    python3 tools/seo.py --no-browser   # skip prerendering and image generation

What it does (idempotent – safe to run again and again):
  * game pages: SEO title, meta description, canonical, hreflang, Open Graph/Twitter tags, JSON-LD (VideoGame),
    a visible "About this game" section with internal links, and pre-rendered texts so that crawlers that do not
    run JavaScript see the right language
  * start page: JSON-LD (WebSite, Organization, ItemList), Open Graph/Twitter, hreflang and static game cards
  * legal pages: canonical + description
  * sitemap.xml, robots.txt, llms.txt, llms-full.txt, 404.html
  * Open Graph images (assets/og.png, games/<slug>/og.png)
"""
import datetime, html, json, os, re, subprocess, sys, threading, functools, http.server, socketserver

SITE = 'https://mycraftgames.com'
NAME = 'My Craft Games'
AUTHOR = 'Matheus'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.date.today().isoformat()
USE_BROWSER = '--no-browser' not in sys.argv
os.chdir(ROOT)

def esc(s): return html.escape(s, quote=True)
def read(p): return open(p, encoding='utf-8').read()
def write(p, s):
    os.makedirs(os.path.dirname(p) or '.', exist_ok=True)
    open(p, 'w', encoding='utf-8').write(s)

def block(s, name, content, anchor_re, after=True):
    """Insert or replace <!--seo:name-->…<!--/seo:name--> next to the first match of anchor_re."""
    b = f'<!--seo:{name}-->\n{content}\n<!--/seo:{name}-->'
    pat = re.compile(rf'<!--seo:{name}-->.*?<!--/seo:{name}-->', re.S)
    if pat.search(s): return pat.sub(lambda m: b, s, count=1)
    m = re.search(anchor_re, s)
    assert m, (name, anchor_re)
    i = m.end() if after else m.start()
    return s[:i] + ('\n' if after else '') + b + ('' if after else '\n') + s[i:]

games = json.loads(subprocess.check_output(['node', '-e',
    "const fs=require('fs');const w={};new Function('window',fs.readFileSync('assets/games.js','utf8'))(w);"
    "process.stdout.write(JSON.stringify(w.MW_GAMES))"]))

L = {
    'de': {'about': 'Über das Spiel', 'age': 'Altersempfehlung', 'free': 'Kostenlos im Browser spielen – auf PC, Tablet und Handy, ohne Anmeldung und ohne Download.',
           'more': 'Weitere Spiele', 'all': 'Alle Spiele bei My Craft Games', 'other': 'English version', 'play': 'Spielen',
           'how': 'So wird gespielt', 'tags': 'Stichworte', 'site_desc': 'Kostenlose 3D-Browserspiele für Kinder und Familien – auf Deutsch und Englisch, ohne Anmeldung, ohne Werbung, mit FSK-Altersempfehlung.'},
    'en': {'about': 'About this game', 'age': 'Age rating', 'free': 'Play free in your browser – on PC, tablet and phone, with no sign-up and no download.',
           'more': 'More games', 'all': 'All games on My Craft Games', 'other': 'Deutsche Version', 'play': 'Play',
           'how': 'How to play', 'tags': 'Tags', 'site_desc': 'Free 3D browser games for kids and families – in German and English, no sign-up, no ads, with FSK age ratings.'},
}

def page_url(slug, lang): return f'{SITE}/games/{slug}/{lang}/'
def short(text, n=158):
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) <= n: return text
    cut = text[:n].rsplit(' ', 1)[0].rstrip(',;:–-')
    return cut + '…'

# ---------------------------------------------------------------- local server + browser helpers
live = {}
def browser_pass():
    """Load every game page in a real browser (age already confirmed) and read the texts that JavaScript fills in."""
    from playwright.sync_api import sync_playwright
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
    handler.log_message = lambda *a: None
    srv = socketserver.TCPServer(('127.0.0.1', 0), handler); port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{port}/'
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--use-gl=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist'])
        pg = b.new_page(viewport={'width': 1280, 'height': 900})
        pg.goto(base + 'robots.txt' if os.path.exists('robots.txt') else base + 'LICENSE.txt')
        pg.evaluate("""()=>{localStorage.setItem('mw-consent',JSON.stringify({v:1,age:30,at:Date.now(),tos:true,privacy:true}));
                         localStorage.setItem('mcg-analytics',JSON.stringify({v:1,choice:'denied',at:Date.now()}));}""")
        for g in games:
            for lang in ('de', 'en'):
                pg.goto(base + f'games/{g["slug"]}/{lang}/index.html'); pg.wait_for_timeout(1500)
                live[(g['slug'], lang)] = pg.evaluate("""()=>{const m={};
                    document.querySelectorAll('[data-t]').forEach(e=>{const k=e.getAttribute('data-t');if(!(k in m))m[k]=e.innerHTML.trim();});
                    const h1=document.querySelector('h1');const help=document.querySelector('.help');
                    return {t:m,h1:h1?h1.innerHTML.trim():'',help:help?help.innerText.trim():''};}""")
        # Open Graph images
        def shot(html_doc, out):
            pg.set_viewport_size({'width': 1200, 'height': 630})
            pg.goto(base + 'LICENSE.txt'); pg.set_content(html_doc, wait_until='load'); pg.wait_for_timeout(300)
            pg.screenshot(path=out, type='png')
        css = ("body{margin:0;width:1200px;height:630px;overflow:hidden;background:#0e1430;font-family:system-ui,-apple-system,'Segoe UI',sans-serif}"
               ".t{position:absolute;left:0;right:0;bottom:0;padding:40px 56px 44px;background:linear-gradient(transparent,#0e1430f2 45%)}"
               "h1{margin:0;color:#fff;font-size:76px;line-height:1.05}p{margin:10px 0 0;color:#ffb347;font-size:34px;font-weight:700}"
               ".b{position:absolute;top:28px;right:36px;background:#ffd400;color:#111;font-weight:900;font-size:30px;padding:8px 18px;border-radius:14px}"
               ".s{position:absolute;top:30px;left:40px;color:#fff;font-weight:800;font-size:30px;background:#0e1430cc;padding:8px 16px;border-radius:14px}")
        for g in games:
            svg = read(f'games/{g["slug"]}/cover.svg')
            col = {0: '#ffffff', 6: '#ffd400', 12: '#2fb34a', 16: '#2f8fe0', 18: '#e2312c'}[g['fsk']]
            doc = (f'<!doctype html><meta charset="utf-8"><style>{css}.cv svg{{position:absolute;left:0;top:-60px;width:1200px;height:750px}}</style>'
                   f'<div class="cv">{svg}</div><div class="s">{NAME}</div><div class="b" style="background:{col}">FSK {g["fsk"]}</div>'
                   f'<div class="t"><h1>{esc(g["title"]["de"])} · {esc(g["title"]["en"])}</h1><p>{esc(g["tagline"]["de"])}</p></div>')
            shot(doc, f'games/{g["slug"]}/og.png')
        sized = '<svg width="400" height="315" preserveAspectRatio="xMidYMid slice" '
        tiles = ''.join('<div style="width:400px;height:315px;overflow:hidden">' + read('games/' + g['slug'] + '/cover.svg').replace('<svg ', sized, 1) + '</div>' for g in games[:5])
        brand = ('<div style="width:400px;height:315px;display:flex;flex-direction:column;justify-content:center;padding:0 34px;box-sizing:border-box;background:#0e1430">'
                 f'<h1 style="font-size:58px">My Craft<br><span style="color:#ff9f2e">Games</span></h1>'
                 '<p style="font-size:26px;color:#cfd6ff">Kostenlose 3D-Spiele<br>Free 3D browser games</p></div>')
        doc = (f'<!doctype html><meta charset="utf-8"><style>{css}</style><div style="display:flex;flex-wrap:wrap;width:1200px">{tiles}{brand}</div>')
        shot(doc, 'assets/og.png')
        b.close()
    srv.shutdown()

if USE_BROWSER:
    try:
        browser_pass()
    except Exception as e:  # Playwright missing etc.
        print('browser step skipped:', e); USE_BROWSER = False

# ---------------------------------------------------------------- game pages
TAG_RE = r'<(h1|h2|h3|p|span|b|button|small|li|label|a|div|strong|em)([^>]*\bdata-t="([^"]+)"[^>]*)>([^<]*)</\1>'
for g in games:
    slug = g['slug']
    for lang in ('de', 'en'):
        other = 'en' if lang == 'de' else 'de'
        p = f'games/{slug}/{lang}/index.html'
        s = read(p)
        T = L[lang]
        title, tagline, desc = g['title'][lang], g['tagline'][lang], g['desc'][lang]
        url = page_url(slug, lang)
        img = f'{SITE}/games/{slug}/og.png'
        meta_desc = short(f'{tagline} {desc}')
        seo_title = f'{title} – {tagline.rstrip(".!")} | {NAME}'
        s = re.sub(r'<title>.*?</title>', f'<title>{esc(seo_title)}</title>', s, count=1)
        ld = {
            '@context': 'https://schema.org', '@type': 'VideoGame', 'name': title, 'alternateName': g['title'][other],
            'description': desc, 'url': url, 'image': img, 'inLanguage': lang, 'genre': g['tags'][lang],
            'gamePlatform': ['Web browser', 'PC', 'Mobile'], 'applicationCategory': 'Game', 'operatingSystem': 'Any (web browser)',
            'isAccessibleForFree': True, 'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'EUR'},
            'contentRating': f'FSK {g["fsk"]}', 'typicalAgeRange': f'{max(g["fsk"], 4)}-', 'datePublished': g.get('added', TODAY),
            'author': {'@type': 'Person', 'name': AUTHOR}, 'publisher': {'@type': 'Organization', 'name': NAME, 'url': SITE + '/'},
            'playMode': 'MultiPlayer' if any('2' in t for t in g['tags']['en']) else 'SinglePlayer',
            'isPartOf': {'@type': 'WebSite', 'name': NAME, 'url': SITE + '/'},
        }
        crumbs = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': NAME, 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': title, 'item': url}]}
        head = '\n'.join([
            f'<meta name="description" content="{esc(meta_desc)}">',
            '<meta name="robots" content="index, follow, max-image-preview:large">',
            f'<link rel="canonical" href="{url}">',
            f'<link rel="alternate" hreflang="{lang}" href="{url}">',
            f'<link rel="alternate" hreflang="{other}" href="{page_url(slug, other)}">',
            f'<link rel="alternate" hreflang="x-default" href="{page_url(slug, "de")}">',
            '<link rel="icon" href="../../../assets/icon.svg" type="image/svg+xml">',
            '<meta name="theme-color" content="#0e1430">',
            f'<meta property="og:type" content="website"><meta property="og:site_name" content="{NAME}">',
            f'<meta property="og:title" content="{esc(title + " – " + tagline)}">',
            f'<meta property="og:description" content="{esc(meta_desc)}">',
            f'<meta property="og:url" content="{url}"><meta property="og:image" content="{img}">',
            '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',
            f'<meta property="og:locale" content="{"de_DE" if lang == "de" else "en_GB"}">',
            '<meta name="twitter:card" content="summary_large_image">',
            '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>',
            '<script type="application/ld+json">' + json.dumps(crumbs, ensure_ascii=False) + '</script>',
        ])
        s = block(s, 'head', head, r'<title>.*?</title>')
        # prerendered texts for crawlers without JavaScript
        lv = live.get((slug, lang))
        if lv:
            def fill(m):
                key = m.group(3)
                val = lv['t'].get(key)
                if val is None or val == m.group(4).strip(): return m.group(0)
                return f'<{m.group(1)}{m.group(2)}>{val}</{m.group(1)}>'
            s = re.sub(TAG_RE, fill, s)
            # empty data-html elements (e.g. the help line)
            s = re.sub(r'<(p|li|div|span)([^>]*\bdata-t="([^"]+)"[^>]*\bdata-html="1"[^>]*)></\1>',
                       lambda m: f'<{m.group(1)}{m.group(2)}>{lv["t"].get(m.group(3), "")}</{m.group(1)}>', s)
            m = re.search(r'<h1([^>]*)>([\s\S]*?)</h1>', s)
            if m and lv['h1'] and m.group(2).strip() != lv['h1']:
                s = s[:m.start()] + f'<h1{m.group(1)}>{lv["h1"]}</h1>' + s[m.end():]
        # visible "About this game" section
        others = [x for x in games if x['slug'] != slug]
        about = (
            '<style>.mw-about{max-width:1100px;margin:22px auto 0;padding:0 12px;font:15px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif;opacity:.92}'
            '.mw-about h2{font-size:20px;margin:0 0 6px}.mw-about h3{font-size:16px;margin:14px 0 4px}.mw-about ul{margin:4px 0;padding-left:20px}'
            '.mw-about a{color:inherit}</style>\n'
            f'<section class="mw-about" aria-labelledby="mw-about-h"><h2 id="mw-about-h">{T["about"]}: {esc(title)}</h2>'
            f'<p><strong>{esc(tagline)}</strong> {esc(desc)}</p><p>{T["free"]}</p>'
            f'<ul><li>{T["age"]}: FSK {g["fsk"]} – {esc(g["fskReason"][lang])}</li><li>{T["tags"]}: {esc(", ".join(g["tags"][lang]))}</li></ul>'
            f'<h3>{T["more"]}</h3><ul>' + ''.join(
                f'<li><a href="../../{x["slug"]}/{lang}/index.html">{esc(x["title"][lang])}</a> – {esc(x["tagline"][lang])}</li>' for x in others) +
            f'</ul><p><a href="../../../index.html">{T["all"]}</a> · <a href="../{other}/index.html" hreflang="{other}" lang="{other}">{T["other"]}</a></p></section>')
        s = block(s, 'about', about, r'<p class="mw-copy">', after=False)
        write(p, s)
    print('game pages:', slug)

# ---------------------------------------------------------------- start page
s = read('index.html')
site_ld = [
    {'@context': 'https://schema.org', '@type': 'WebSite', 'name': NAME, 'url': SITE + '/', 'inLanguage': ['de', 'en'],
     'description': L['en']['site_desc']},
    {'@context': 'https://schema.org', '@type': 'Organization', 'name': NAME, 'url': SITE + '/', 'logo': SITE + '/assets/icon.svg'},
    {'@context': 'https://schema.org', '@type': 'ItemList', 'name': 'Games', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'url': page_url(g['slug'], 'de'), 'name': g['title']['de'] + ' / ' + g['title']['en']}
        for i, g in enumerate(games)]},
]
head = '\n'.join([
    '<meta name="robots" content="index, follow, max-image-preview:large">',
    f'<link rel="canonical" href="{SITE}/">',
    f'<link rel="alternate" hreflang="de" href="{SITE}/">',
    f'<link rel="alternate" hreflang="en" href="{SITE}/?lang=en">',
    f'<link rel="alternate" hreflang="x-default" href="{SITE}/">',
    f'<meta property="og:type" content="website"><meta property="og:site_name" content="{NAME}">',
    f'<meta property="og:title" content="{NAME} – Kostenlose 3D-Browserspiele · Free 3D browser games">',
    f'<meta property="og:description" content="{esc(L["de"]["site_desc"])}">',
    f'<meta property="og:url" content="{SITE}/"><meta property="og:image" content="{SITE}/assets/og.png">',
    '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',
    '<meta name="twitter:card" content="summary_large_image">',
    '<link rel="alternate" type="text/plain" title="LLM summary" href="llms.txt">',
] + ['<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + '</script>' for x in site_ld])
s = re.sub(r'<title>.*?</title>', f'<title>{NAME} – Kostenlose 3D-Browserspiele für Kinder · Free 3D browser games</title>', s, count=1)
s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{esc(L["de"]["site_desc"] + " " + L["en"]["site_desc"])}">', s, count=1)
s = block(s, 'head', head, r'<meta name="description" content="[^"]*">')
cards = '\n'.join(
    f'<article class="card"><div class="cover"><img src="{g["cover"]}" alt="{esc(g["title"]["de"])}" loading="lazy" width="640" height="400"></div>'
    f'<div class="body"><h3>{esc(g["title"]["de"])} <small lang="en">· {esc(g["title"]["en"])}</small></h3><p class="tagline">{esc(g["tagline"]["de"])}</p>'
    f'<p class="desc">{esc(g["desc"]["de"])}</p><p class="fskwhy">FSK {g["fsk"]}: {esc(g["fskReason"]["de"])}</p>'
    f'<div class="actions"><a class="play" href="games/{g["slug"]}/de/index.html">Spielen</a> '
    f'<a class="alt-lang" href="games/{g["slug"]}/en/index.html" hreflang="en" lang="en">English</a></div></div></article>'
    for g in games)
s = block(s, 'cards', cards, r'<div class="grid" id="games">')
write('index.html', s)
print('start page')

# ---------------------------------------------------------------- legal pages
LEGAL = {'terms.html': ('Nutzungsbedingungen · Terms of Use', 'Nutzungsbedingungen von My Craft Games. Terms of Use for My Craft Games.'),
         'privacy.html': ('Datenschutzerklärung · Privacy Policy', 'Datenschutzerklärung von My Craft Games. Privacy Policy for My Craft Games.'),
         'imprint.html': ('Impressum · Legal notice', 'Impressum von My Craft Games. Legal notice for My Craft Games.')}
for f, (t, d) in LEGAL.items():
    s = read(f)
    has_desc = re.search(r'<meta name="description"', s.split('<!--seo:head-->')[0]) is not None
    head = (f'<link rel="canonical" href="{SITE}/{f}">\n<link rel="icon" href="assets/icon.svg" type="image/svg+xml">\n'
            + ('' if has_desc else f'<meta name="description" content="{esc(d)}">\n') + '<meta name="robots" content="index, follow">')
    s = block(s, 'head', head, r'<title>.*?</title>')
    write(f, s)
print('legal pages')

# ---------------------------------------------------------------- sitemap, robots, 404
urls = [(SITE + '/', [('de', SITE + '/'), ('en', SITE + '/?lang=en'), ('x-default', SITE + '/')], '1.0')]
for g in games:
    alts = [('de', page_url(g['slug'], 'de')), ('en', page_url(g['slug'], 'en')), ('x-default', page_url(g['slug'], 'de'))]
    for lang in ('de', 'en'): urls.append((page_url(g['slug'], lang), alts, '0.9'))
for f in LEGAL: urls.append((f'{SITE}/{f}', [], '0.2'))
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
for u, alts, pr in urls:
    sm.append(f'  <url><loc>{esc(u)}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority>' +
              ''.join(f'<xhtml:link rel="alternate" hreflang="{h}" href="{esc(a)}"/>' for h, a in alts) + '</url>')
sm.append('</urlset>')
write('sitemap.xml', '\n'.join(sm) + '\n')
write('robots.txt', f"""# {NAME} – everyone is welcome to read and index this site,
# including search engines and AI assistants.
User-agent: *
Allow: /
# game sources and build tools are for developers, the real game pages are under /games/
Disallow: /src/
Disallow: /tools/

Sitemap: {SITE}/sitemap.xml
""")
nf = read('404.html') if os.path.exists('404.html') else ''
write('404.html', f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Seite nicht gefunden · Page not found | {NAME}</title>
<meta name="robots" content="noindex">
<link rel="icon" href="/assets/icon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<div class="wrap" style="padding:48px 16px;text-align:center">
  <h1>Hoppla! Diese Seite gibt es nicht.</h1>
  <p lang="en">Oops! This page doesn't exist.</p>
  <p><a class="play" href="/">Zu den Spielen · Go to the games</a></p>
  <ul style="list-style:none;padding:0">
{chr(10).join(f'    <li><a href="/games/{g["slug"]}/de/index.html">{esc(g["title"]["de"])}</a> · <a href="/games/{g["slug"]}/en/index.html" lang="en">{esc(g["title"]["en"])}</a></li>' for g in games)}
  </ul>
</div>
</body>
</html>
""")

# ---------------------------------------------------------------- llms.txt / llms-full.txt
def strip_tags(x): return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', html.unescape(x or ''))).strip()
lt = [f'# {NAME}', '',
      f'> {L["en"]["site_desc"]} Made by {AUTHOR}. Every game runs directly in the web browser (three.js), works on PC and phone, and exists in German and English.', '',
      'Key facts:',
      '- Free to play, no account, no ads, no download.',
      '- Age ratings follow the German FSK levels (own assessment, not an official FSK/USK review).',
      '- Visitors confirm their age on the start page; games above their age stay locked.',
      '- Google Analytics is used only after opt-in consent.', '',
      '## Games', '']
for g in games:
    lt.append(f'- [{g["title"]["en"]} (English)]({page_url(g["slug"], "en")}): {g["tagline"]["en"]} {g["desc"]["en"]} FSK {g["fsk"]}.')
    lt.append(f'- [{g["title"]["de"]} (Deutsch)]({page_url(g["slug"], "de")}): {g["tagline"]["de"]} {g["desc"]["de"]} FSK {g["fsk"]}.')
lt += ['', '## Site', '',
       f'- [Start page]({SITE}/): all games with descriptions and age ratings (German and English)',
       f'- [Full game guide for LLMs]({SITE}/llms-full.txt): how to play each game, controls and features',
       f'- [Terms of Use]({SITE}/terms.html)', f'- [Privacy Policy]({SITE}/privacy.html)', f'- [Legal notice]({SITE}/imprint.html)', '',
       '## Optional', '', f'- [Sitemap]({SITE}/sitemap.xml)', '']
write('llms.txt', '\n'.join(lt))
ft = [f'# {NAME} – full game guide', '', f'> {L["en"]["site_desc"]} Made by {AUTHOR}.', '',
      f'Website: {SITE}/ · Last updated: {TODAY}', '']
for g in games:
    ft += [f'## {g["title"]["en"]} / {g["title"]["de"]}', '',
           f'- English: {page_url(g["slug"], "en")}', f'- Deutsch: {page_url(g["slug"], "de")}',
           f'- Age rating: FSK {g["fsk"]} – {g["fskReason"]["en"]}', f'- Tags: {", ".join(g["tags"]["en"])}',
           f'- Added: {g.get("added", "")}', '', f'**{g["tagline"]["en"]}** {g["desc"]["en"]}', '']
    help_en = strip_tags((live.get((g['slug'], 'en')) or {}).get('help', ''))
    if help_en: ft += ['### How to play', '', help_en, '']
    ft += [f'**Deutsch – {g["tagline"]["de"]}** {g["desc"]["de"]}', '']
    help_de = strip_tags((live.get((g['slug'], 'de')) or {}).get('help', ''))
    if help_de: ft += ['### So wird gespielt', '', help_de, '']
write('llms-full.txt', '\n'.join(ft))
print('sitemap.xml, robots.txt, 404.html, llms.txt, llms-full.txt' + (', og images' if USE_BROWSER else ''))
