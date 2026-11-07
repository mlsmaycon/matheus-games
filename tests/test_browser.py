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


@pytest.mark.parametrize('lang', LANGS)
def test_tsunami_escape_grab_deliver_wave_and_trench(page, lang):
    """Tsunami-Flucht: grab a brainrot, deliver it to the base (earns money), a wave washes away what you carry,
    a trench or a hideout hole keeps you safe, upgrades cost money, brainrots in the base can be sold (press twice), progress is saved, computer players only fill their own bases,
    and sometimes a second wave hides right behind the first one."""
    page.set_storage(age=30)
    pg = page.goto(f'games/tsunami-flucht/{lang}/index.html', 1200)
    start_game(pg)
    pg.wait_for_timeout(600)
    r = pg.evaluate("""async () => {
        const T = window.__tf, pl = T.player, out = {}, wait = ms => new Promise(r => setTimeout(r, ms));
        T.setNext(999);
        let f = T.field.find(x => x.r === 'common'); pl.x = f.x; pl.z = f.z; T.grab();
        out.carried = pl.carry.length;
        pl.x = 0; pl.z = 3; await wait(300);
        out.ped = T.S.ped.length; out.afterDeliver = pl.carry.length;
        const m0 = T.S.money; await wait(1200); out.earned = T.S.money > m0;
        f = T.field.find(x => x.r === 'rare'); pl.x = f.x; pl.z = f.z; T.grab();
        T.startWave(4); T.waves[T.waves.length - 1].z = pl.z - 2; await wait(400);
        out.lostCarry = pl.carry.length; out.backHome = pl.z > 0;
        const tz = -T.TRENCHES[1]; pl.x = 0; pl.z = tz; await wait(600);
        T.startWave(2); T.waves[T.waves.length - 1].z = tz - 3; await wait(1500);
        out.inTrench = pl.z === tz;
        const h = T.HOLES[2]; pl.x = h.x; pl.z = -h.d; await wait(600);
        T.startWave(3); T.waves[T.waves.length - 1].z = pl.z - 3; await wait(1500);
        out.inHole = pl.z === -h.d && pl.y < -2;
        T.S.money = 1000; T.buySpeed(); T.buyCarry();
        out.spd = T.S.spd; out.cap = T.S.cap; out.money = Math.round(T.S.money);
        const b = T.bots[0]; b.state = 'home'; b.wait = 0; T.waves.length = 0;
        f = T.spawn('common'); b.carry = {ty: f.ty, mesh: f.mesh}; b.state = 'back'; b.z = 16; await wait(1500);
        out.botPed = b.ped.length; out.playerPed = T.S.ped.length;
        out.saved = JSON.parse(localStorage.getItem('tsunami-flucht-v1')).ped.length;
        T.S.ped.push(T.S.ped[0]); const pp = {x: -5.6, z: 3.5}; pl.x = pp.x; pl.z = pp.z + 0.5; await wait(100);
        const before = T.S.money, n0 = T.S.ped.length; T.grab(); out.sellAsked = T.S.ped.length === n0;
        T.grab(); out.sold = T.S.ped.length === n0 - 1 && T.S.money > before;
        T.waves.length = 0; T.follow(0.3); await wait(800);
        out.followWave = T.waves.length;
        out.botsMoved = T.bots.some(x => x.state !== 'home' || x.ped.length > 0);
        return out;
    }""")
    assert r['carried'] == 1 and r['afterDeliver'] == 0 and r['ped'] == 1 and r['earned'], r
    assert r['lostCarry'] == 0 and r['backHome'], r
    assert r['inTrench'] and r['inHole'], r
    assert r['spd'] == 1 and r['cap'] == 2 and r['money'] == 1000 - 25 - 120, r
    assert r['botPed'] >= 1 and r['playerPed'] == 1, r
    assert r['saved'] == 1, r
    assert r['followWave'] == 1 and r['botsMoved'], r
    assert r['sellAsked'] and r['sold'], r
    assert not page.errors, page.errors
