"""Fast checks without a browser: registry, sources, privacy texts and the built files belong together."""
import os, re, datetime
import pytest
from conftest import REPO, GAMES, SLUGS, LANGS

FSK = {0, 6, 12, 16, 18}
TEXT_FIELDS = ['title', 'tagline', 'desc', 'tags', 'fskReason']


def read(*p):
    return open(os.path.join(REPO, *p), encoding='utf-8').read()


@pytest.mark.parametrize('g', GAMES, ids=SLUGS)
def test_registry_entry_complete(g):
    assert re.fullmatch(r'[a-z0-9-]+', g['slug'])
    assert g['fsk'] in FSK
    datetime.date.fromisoformat(g['added'])
    for f in TEXT_FIELDS:
        for lang in LANGS:
            assert g[f][lang], f'{g["slug"]}: {f}.{lang} is empty'
    assert len(g['tags']['de']) == len(g['tags']['en'])
    assert g['cover'] == f'games/{g["slug"]}/cover.svg'


@pytest.mark.parametrize('slug', SLUGS)
def test_source_and_cover_exist(slug):
    assert os.path.isfile(os.path.join(REPO, 'src', f'{slug}.html'))
    assert os.path.isfile(os.path.join(REPO, 'site', 'games', slug, 'cover.svg'))


def test_build_list_matches_registry():
    build = read('tools', 'build.py')
    listed = {m.group(2): int(m.group(3)) for m in re.finditer(r"\('src/([a-z0-9-]+)\.html', '([a-z0-9-]+)', (\d+),", build)}
    assert listed == {g['slug']: g['fsk'] for g in GAMES}, 'GAMES in tools/build.py and site/assets/games.js disagree'


def storage_keys(slug):
    src = read('src', f'{slug}.html')
    keys = set(re.findall(r"localStorage\.(?:get|set)Item\(['\"]([^'\"]+)['\"]", src))
    keys |= set(re.findall(r"KEY\s*=\s*['\"]([^'\"]+)['\"]", src))
    return keys


@pytest.mark.parametrize('slug', SLUGS)
def test_storage_keys_documented_and_deletable(slug):
    site_js, privacy = read('site', 'assets', 'site.js'), read('site', 'privacy.html')
    keys = storage_keys(slug)
    assert keys, f'{slug}: no localStorage key found – update this test if the game stores nothing'
    for k in keys:
        assert f"'{k}'" in site_js, f'{k} missing in KEYS (site/assets/site.js) – "Delete my data" would not clear it'
        assert privacy.count(f'<code>{k}</code>') >= 2, f'{k} missing in the privacy table (German and English)'


@pytest.mark.parametrize('f', ['index.html', 'terms.html', 'privacy.html', 'imprint.html'])
def test_site_pages_have_both_languages_and_no_generated_blocks(f):
    s = read('site', f)
    assert '<!--seo:' not in s, 'generated SEO blocks must not be committed – they are added in dist/ by tools/seo.py'
    if f != 'index.html':
        assert 'class="l-de"' in s and 'class="l-en"' in s


def test_site_js_texts_exist_in_both_languages():
    js = read('site', 'assets', 'site.js')
    de = js.split("en: {", 1)[0]
    en = js.split("en: {", 1)[1]
    de_keys = set(re.findall(r"'([a-z0-9.]+)':", de))
    en_keys = set(re.findall(r"'([a-z0-9.]+)':", en))
    assert de_keys - en_keys == set(), f'missing English texts: {sorted(de_keys - en_keys)}'
    assert en_keys - de_keys == set(), f'missing German texts: {sorted(en_keys - de_keys)}'


def test_cache_versions_consistent():
    vs = set()
    for f in ['index.html', 'terms.html', 'privacy.html', 'imprint.html']:
        vs |= set(re.findall(r'\?v=(\d+)"', read('site', f)))
    assert len(vs) == 1, f'different ?v= cache versions in the site pages: {vs}'
