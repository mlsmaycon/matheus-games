"""Checks on the built site in dist/ (no browser): pages, SEO data, sitemap, no outside requests."""
import json, os, re, xml.etree.ElementTree as ET
import pytest
from conftest import GAMES, SLUGS, LANGS
from helpers import german_leftovers, visible_static_text

SITE = 'https://mycraftgames.com'
PAGES = [(s, l) for s in SLUGS for l in LANGS]


def built(dist, *p):
    return open(os.path.join(dist, *p), encoding='utf-8').read()


@pytest.mark.parametrize('slug,lang', PAGES)
def test_game_page_basics(dist, slug, lang):
    g = next(x for x in GAMES if x['slug'] == slug)
    s = built(dist, 'games', slug, lang, 'index.html')
    assert f'<html lang="{lang}">' in s
    assert re.search(r'<title>[^<]*' + re.escape(g['title'][lang]), s)
    assert f'data-fsk="{g["fsk"]}"' in s and f'data-game="{slug}"' in s, 'age gate missing or wrong FSK'
    assert 'assets/analytics.js' in s and 'class="mw-copy"' in s and 'class="mw-nav"' in s
    assert f"window.MW_LANG='{lang}'" in s or slug in ('brainrot-raub', 'versteck-alarm')


@pytest.mark.parametrize('slug,lang', PAGES)
def test_no_outside_requests_in_markup(dist, slug, lang):
    s = built(dist, 'games', slug, lang, 'index.html')
    assert not re.search(r'<script[^>]+src="https?://', s), 'scripts must be served from this site'
    assert not re.search(r'<link[^>]+rel="stylesheet"[^>]+href="https?://', s), 'no outside stylesheets / Google Fonts'
    assert 'fonts.googleapis' not in s and 'cdnjs' not in s


@pytest.mark.parametrize('slug,lang', PAGES)
def test_seo_head(dist, slug, lang):
    s = built(dist, 'games', slug, lang, 'index.html')
    url = f'{SITE}/games/{slug}/{lang}/'
    assert f'<link rel="canonical" href="{url}">' in s
    for h in ('de', 'en', 'x-default'):
        assert f'hreflang="{h}"' in s
    assert re.search(r'<meta name="description" content="[^"]{40,}">', s)
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s):
        json.loads(block)
    img = re.search(r'<meta property="og:image" content="([^"]+)"', s).group(1)
    assert os.path.isfile(os.path.join(dist, img.replace(SITE + '/', ''))), 'preview image missing'
    assert 'class="mw-about"' in s


@pytest.mark.parametrize('slug', SLUGS)
def test_english_page_has_no_german_without_javascript(dist, slug):
    left = german_leftovers(visible_static_text(built(dist, 'games', slug, 'en', 'index.html')))
    assert not left, f'German words on the English page: {left}'


def test_start_page_static_cards_and_json_ld(dist):
    s = built(dist, 'index.html')
    assert s.count('<article class="card">') == len(GAMES)
    for g in GAMES:
        assert f'games/{g["slug"]}/de/index.html' in s and f'games/{g["slug"]}/en/index.html' in s
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s):
        json.loads(block)


def test_sitemap_lists_every_page(dist):
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    locs = {e.text for e in ET.parse(os.path.join(dist, 'sitemap.xml')).getroot().findall('s:url/s:loc', ns)}
    assert f'{SITE}/' in locs
    for slug, lang in PAGES:
        assert f'{SITE}/games/{slug}/{lang}/' in locs


def test_robots_llms_404(dist):
    assert f'Sitemap: {SITE}/sitemap.xml' in built(dist, 'robots.txt')
    llms, full = built(dist, 'llms.txt'), built(dist, 'llms-full.txt')
    for g in GAMES:
        assert g['title']['en'] in llms and g['title']['de'] in llms and g['title']['en'] in full
    assert 'noindex' in built(dist, '404.html')


def test_no_sources_or_tools_in_dist(dist):
    for bad in ('src', 'tools', 'tests', 'AGENTS.md', 'README.md'):
        assert not os.path.exists(os.path.join(dist, bad)), f'{bad} must not be published'
