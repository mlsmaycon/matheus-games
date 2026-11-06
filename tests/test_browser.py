"""End-to-end checks in headless Chromium: age gate, every game in both languages, analytics consent, phone width."""
import pytest
from conftest import GAMES, SLUGS, LANGS
from helpers import german_leftovers, start_game

pytest.importorskip('playwright')


def test_start_page_asks_age_then_shows_all_games(page):
    pg = page.goto('index.html?lang=de')
    assert pg.is_visible('#gate')
    pg.fill('#gAge', '30'); pg.check('#gTos'); pg.check('#gPrivacy')
    pg.click('#gateForm .play'); pg.wait_for_timeout(600)
    titles = [h.inner_text() for h in pg.query_selector_all('#games .card h3')]
    assert titles == [g['title']['de'] for g in GAMES]
    pg.click('.lang button[data-lang="en"]'); pg.wait_for_timeout(300)
    assert [h.inner_text() for h in pg.query_selector_all('#games .card h3')] == [g['title']['en'] for g in GAMES]
    assert not page.errors and not page.external


def test_young_child_sees_older_games_locked(page):
    page.set_storage(age=5)
    pg = page.goto('index.html?lang=de', 800)
    locked = {c.query_selector('h3').inner_text() for c in pg.query_selector_all('#games .card.locked')}
    assert locked == {g['title']['de'] for g in GAMES if g['fsk'] > 5}


@pytest.mark.parametrize('slug,lang', [(s, l) for s in SLUGS for l in LANGS])
def test_game_runs(page, slug, lang):
    page.set_storage(age=30)
    pg = page.goto(f'games/{slug}/{lang}/index.html', 1500)
    assert pg.query_selector('.mw-gate') is None
    start_game(pg)
    pg.wait_for_timeout(2500)
    assert not page.errors, page.errors
    assert not page.external, f'requests to other hosts: {page.external}'
    if lang == 'en':
        left = german_leftovers(pg.evaluate('document.body.innerText'))
        assert not left, f'German words on the English page while playing: {left}'


@pytest.mark.parametrize('slug', SLUGS)
def test_game_page_without_age_shows_notice_instead_of_redirect(page, slug):
    pg = page.goto(f'games/{slug}/en/index.html')
    assert pg.url.endswith(f'games/{slug}/en/index.html')
    assert pg.is_visible('.mw-gate a')
    assert 'index.html?next=' + slug in pg.get_attribute('.mw-gate a', 'href')


def test_too_young_for_game_gets_age_notice(page):
    g = next(x for x in GAMES if x['fsk'] >= 6)
    page.set_storage(age=4)
    pg = page.goto(f'games/{g["slug"]}/de/index.html')
    assert str(g['fsk']) in pg.inner_text('.mw-gate')


def test_analytics_only_after_consent(page):
    pg = page.goto('index.html')
    pg.fill('#gAge', '30'); pg.check('#gTos'); pg.check('#gPrivacy')
    pg.click('#gateForm .play'); pg.wait_for_timeout(1500)
    assert pg.is_visible('.mcg-cc'), 'consent notice should appear after the age question'
    assert not page.external, 'nothing may be loaded from other hosts before consent'
    pg.click('.mcg-cc .yes'); pg.wait_for_timeout(800)
    assert any('googletagmanager.com' in u for u in page.external)
    pg = page.goto(f'games/{SLUGS[0]}/de/index.html')
    assert pg.evaluate("(window.dataLayer||[]).some(a => a[0]==='event' && a[1]==='play_game')")


def test_declining_analytics_loads_nothing(page):
    pg = page.goto('index.html')
    pg.fill('#gAge', '12'); pg.check('#gTos'); pg.check('#gPrivacy')
    parent = pg.query_selector('#gParent')
    if parent and parent.is_visible():
        parent.check()
    pg.click('#gateForm .play'); pg.wait_for_timeout(1500)
    assert pg.inner_text('.mcg-cc .yes') in ('A parent agrees', 'Ein Elternteil stimmt zu'), 'under-16s need a parent'
    pg.click('.mcg-cc .no'); pg.wait_for_timeout(500)
    page.goto(f'games/{SLUGS[-1]}/de/index.html')
    assert not page.external


@pytest.mark.parametrize('path', ['index.html'] + [f'games/{s}/de/index.html' for s in SLUGS])
def test_phone_width_no_horizontal_scroll(phone, path):
    phone.set_storage(age=30)
    pg = phone.goto(path, 1200)
    assert pg.evaluate('document.documentElement.scrollWidth') <= 402


@pytest.mark.parametrize('lang', LANGS)
def test_star_unicorn_shop_buys_and_saves(page, lang):
    """Sternen-Einhorn: the SHOP button opens the shop, buying spends coins, the purchase is worn and saved."""
    page.set_storage(age=30)
    page.pg.evaluate("localStorage.setItem('sternen-einhorn-v1', JSON.stringify({coins: 100, owned: [], eq: {}}))")
    pg = page.goto(f'games/sternen-einhorn/{lang}/index.html', 1200)
    box = pg.query_selector('#su-canvas').bounding_box()
    pg.mouse.click(box['x'] + box['width'] * 95 / 960, box['y'] + box['height'] * 554 / 600)   # SHOP button (bottom left)
    pg.wait_for_timeout(300)
    assert pg.is_visible('#su-shop')
    if lang == 'en':
        left = german_leftovers(pg.inner_text('#su-shop'))
        assert not left, f'German words in the English shop: {left}'
    pg.click('.su-card >> nth=1')            # second colour: costs 25 coins
    pg.click('#su-act')
    pg.wait_for_timeout(200)
    saved = pg.evaluate("JSON.parse(localStorage.getItem('sternen-einhorn-v1'))")
    assert saved['coins'] == 75 and saved['eq']['color'] == 'pink' and 'color:pink' in saved['owned']
    pg.keyboard.press('Escape')
    pg.wait_for_timeout(200)
    assert not pg.is_visible('#su-shop')
    assert not page.errors, page.errors
