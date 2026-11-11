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
    a trench or a hideout hole keeps you safe, upgrades cost money and have no limit, brainrots in the base can be sold (press twice), progress is saved, computer players only fill their own bases,
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
        T.S.money = 1e30; for (let i = 0; i < 30; i++) { T.buySpeed(); T.buyCarry(); }
        out.noLimit = T.S.spd === 31 && T.S.cap === 32;
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
    assert r['noLimit'], r
    assert not page.errors, page.errors


@pytest.mark.parametrize('lang', LANGS)
def test_farm_buy_feed_collect_sell_and_improve(page, lang):
    """Mein Bauernhof: buy chickens, fill the trough, animals produce, items are collected and sold at the farm shop, happy animals drop coins,
    pens can be built, the farm can be improved (shop level raises prices), the shop panel opens, progress is saved."""
    page.set_storage(age=30)
    pg = page.goto(f'games/bauernhof/{lang}/index.html', 1200)
    start_game(pg)
    pg.wait_for_timeout(500)
    r = pg.evaluate("""() => {
        const B = window.__bh, S = B.S, o = {};
        o.bought = B.buyAnimal('chicken') && B.buyAnimal('chicken');
        o.poor = !B.buyAnimal('chicken');
        S.water = 10; o.filled = B.fillTrough('chicken');
        B.tick(20); o.items = B.items.length;
        for (const it of B.items.slice()) { B.player.x = it.x; B.player.z = it.z; B.tick(0.1); }
        o.basket = B.basket.length;
        const before = S.coins; B.player.x = B.STAND.x; B.player.z = B.STAND.z + 1.5; B.tick(0.1);
        o.earned = S.coins - before; o.basketAfter = B.basket.length;
        S.water = 10; B.fillTrough('chicken'); const a0 = B.penObj.chicken.animals[0]; if (a0.coin) a0.coin = null; a0.ct = 0; B.tick(0.1);
        const coin = B.items.find(x => x.type === 'coin'); o.coinDropped = !!coin;
        if (coin) { const c1 = S.coins; B.player.x = coin.x; B.player.z = coin.z; B.tick(0.1); o.coinValue = S.coins - c1; }
        S.coins = 10000;
        o.pen = B.buildPen('sheep') && B.buyAnimal('sheep');
        o.improved = B.upgradeFarm('stand') && B.upgradeFarm('house') && B.upgradeFarm('field') && B.upgradeFarm('tap');
        B.player.x = B.STAND.x; B.player.z = B.STAND.z + 1.5;
        B.basket.push({type: 'egg', value: 4}); const c0 = S.coins; B.tick(0.1); o.boosted = S.coins - c0;
        B.player.x = B.SHOP.x; B.player.z = B.SHOP.z + 1.5; B.tick(0.1); B.use(); o.shop = B.shopOpen && !!document.querySelector('#shopList button');
        B.closeShop();
        const saved = JSON.parse(localStorage.getItem('bauernhof-v1'));
        o.saved = saved.pens.chicken.n === 2 && saved.pens.sheep.open && saved.standLv === 1;
        return o;
    }""")
    assert r['bought'] and r['poor'] and r['filled'], r
    assert r['items'] >= 2 and r['basket'] >= 2, r
    assert r['earned'] >= 8 and r['basketAfter'] == 0, r
    assert r['coinDropped'] and r['coinValue'] >= 2, r
    assert r['pen'] and r['improved'] and r['boosted'] == 5, r
    assert r['shop'] and r['saved'], r
    assert not page.errors, page.errors


@pytest.mark.parametrize('lang', LANGS)
def test_farm_visitors_look_and_pay(page, lang):
    """Mein Bauernhof: visitors walk in through the gate, look at pens with animals and pay when they leave."""
    page.set_storage(age=30)
    pg = page.goto(f'games/bauernhof/{lang}/index.html', 1200)
    start_game(pg)
    pg.wait_for_timeout(500)
    r = pg.evaluate("""() => {
        const B = window.__bh, S = B.S, o = {};
        B.buyAnimal('chicken'); S.water = 10; B.fillTrough('chicken');
        o.none = B.visitors.length;
        const v = B.spawnVisitor(); o.spawned = !!v && B.visitors.length === 1;
        const c0 = S.coins; B.player.x = -25; B.player.z = -18;
        for (let i = 0; i < 60 && B.visitors.includes(v); i++) B.tick(1);
        o.left = !B.visitors.includes(v); o.paid = S.coins - c0;
        return o;
    }""")
    assert r['spawned'] and r['left'], r
    assert r['paid'] >= 5, r
    assert not page.errors, page.errors


@pytest.mark.parametrize('lang', LANGS)
def test_farm_more_animals_and_ten_per_pen(page, lang):
    """Mein Bauernhof: twelve kinds of animals, every pen can grow to 10 animals, new animals make their own goods."""
    page.set_storage(age=30)
    pg = page.goto(f'games/bauernhof/{lang}/index.html', 1200)
    start_game(pg)
    pg.wait_for_timeout(500)
    r = pg.evaluate("""() => {
        const B = window.__bh, S = B.S, o = {};
        o.kinds = Object.keys(B.penObj).length;
        S.coins = 1e6; B.buildPen('duck');
        for (let i = 0; i < 25; i++) { if (!B.buyAnimal('duck')) B.expandPen('duck'); }
        o.ducks = S.pens.duck.n; o.cap = S.pens.duck.cap;
        o.noMore = !B.expandPen('duck') && !B.buyAnimal('duck');
        S.feed = 50; S.water = 40; B.fillTrough('duck'); B.tick(20);
        o.duckEggs = B.items.some(i => i.type === 'duckegg');
        return o;
    }""")
    assert r['kinds'] == 12, r
    assert r['ducks'] == 10 and r['cap'] == 10 and r['noMore'], r
    assert r['duckEggs'], r
    assert not page.errors, page.errors


@pytest.mark.parametrize('lang', LANGS)
def test_farm_loads_old_save_without_new_animals(page, lang):
    """Mein Bauernhof: a save from before the new animals (only six pens) must still load instead of showing a black screen."""
    page.set_storage(age=30)
    page.pg.evaluate("""() => localStorage.setItem('bauernhof-v1', JSON.stringify({coins: 2875, feed: 0, water: 0, basketLv: 0, bucketLv: 0, pony: false,
        standLv: 0, fieldLv: 0, houseLv: 0, tap: false, time: 50, day: 1, tips: 2, plots: [{st: 0, t: 0}],
        pens: {chicken: {open: true, cap: 3, n: 1, food: 9, water: 9}, sheep: {open: true, cap: 3, n: 1, food: 0, water: 0},
               pig: {open: false, cap: 3, n: 0, food: 0, water: 0}, goat: {open: false, cap: 3, n: 0, food: 0, water: 0},
               cow: {open: false, cap: 3, n: 0, food: 0, water: 0}, unicorn: {open: false, cap: 3, n: 0, food: 0, water: 0}}}))""")
    pg = page.goto(f'games/bauernhof/{lang}/index.html', 1200)
    start_game(pg)
    pg.wait_for_timeout(500)
    r = pg.evaluate("() => ({coins: window.__bh.S.coins, sheep: window.__bh.S.pens.sheep.n, duck: window.__bh.S.pens.duck.n})")
    assert r == {'coins': 2875, 'sheep': 1, 'duck': 0}, r
    assert not page.errors, page.errors


@pytest.mark.parametrize('lang', LANGS)
def test_farm_animals_have_babies(page, lang):
    """Mein Bauernhof: two fed animals with free room get a baby, the baby is small, grows up and is saved; a full pen gets no babies."""
    page.set_storage(age=30)
    pg = page.goto(f'games/bauernhof/{lang}/index.html', 1200)
    start_game(pg)
    pg.wait_for_timeout(500)
    r = pg.evaluate("""() => {
        const B = window.__bh, S = B.S, o = {};
        S.coins = 100; B.buyAnimal('chicken'); B.buyAnimal('chicken'); S.water = 10; S.feed = 20; B.fillTrough('chicken');
        S.time = 60; B.penObj.chicken.breedT = 0.5; B.tick(1);
        o.n = S.pens.chicken.n; const baby = B.penObj.chicken.animals.find(a => a.baby > 0);
        o.small = !!baby && baby.mesh.scale.x < 0.7;
        B.tick(1); o.saved = JSON.parse(localStorage.getItem('bauernhof-v1') || '{}').pens?.chicken?.kids?.length ?? 'none';
        S.pens.chicken.food = 20; S.pens.chicken.water = 20; S.time = 60; B.penObj.chicken.breedT = 999; B.tick(B.GROW_UP + 1);
        o.grown = !!baby && !(baby.baby > 0) && baby.mesh.scale.x > 0.95;
        B.penObj.chicken.breedT = 0.1; S.pens.chicken.food = 20; S.pens.chicken.water = 20; S.time = 60; B.tick(0.5);
        o.full = S.pens.chicken.n;
        return o;
    }""")
    assert r['n'] == 3 and r['small'], r
    assert r['grown'] and r['full'] == 3, r
    assert not page.errors, page.errors


@pytest.mark.parametrize('lang', LANGS)
def test_pixel_blaster_shoot_wave_shop(page, lang):
    """Pixel-Blaster: a shot hurts the monster it aims at, defeated monsters give coins, a cleared wave opens the shop,
    weapons can be bought and equipped, the next wave starts, getting hit lowers health
    (200 at the start) and you slowly heal after 4 seconds without being hit."""
    page.set_storage(age=30)
    pg = page.goto(f'games/pixel-blaster/{lang}/index.html', 1200)
    start_game(pg)
    pg.wait_for_timeout(500)
    r = pg.evaluate("""async () => {
        const B = window.__pb, o = {}, wait = ms => new Promise(r => setTimeout(r, ms));
        o.fight = B.state === 'fight';
        B.clearQueue(); B.killAll();
        B.player.x = 4; B.player.z = 28; B.player.y = 0;
        const e = B.spawn('robot'); e.x = 4; e.z = 18; B.aimAt(e);
        const hp0 = e.hp, a0 = B.ammo.pistol; B.fire(); o.hit = e.hp < hp0; o.ammoUsed = a0 - B.ammo.pistol;
        const c0 = B.S.coins; B.killAll(); o.coins = B.S.coins > c0;
        B.tick(0.2); await wait(1300); o.shop = B.state === 'shop' && !document.getElementById('shop').hidden;
        B.S.coins = 1000; o.bought = B.buyWeapon('shotgun'); o.cur = B.S.cur;
        document.getElementById('nextWave').click(); o.wave2 = B.state === 'fight' && B.wave === 2;
        const hp = B.player.hp; B.hurt(10); o.hurt = B.player.hp === hp - 10;
        o.maxHp = B.player.hp + 10; B.clearQueue(); B.killAll(); const far = B.spawn('slime'); far.x = -30; far.z = -30; const h1 = B.player.hp; B.tick(6); o.healed = B.state === 'fight' && B.player.hp > h1;
        o.saved = JSON.parse(localStorage.getItem('pixel-blaster-v1')).owned.includes('shotgun');
        return o;
    }""")
    assert r['fight'] and r['hit'] and r['ammoUsed'] == 1 and r['coins'], r
    assert r['shop'] and r['bought'] and r['cur'] == 'shotgun' and r['wave2'], r
    assert r['hurt'] and r['saved'], r
    assert r['maxHp'] == 200 and r['healed'], r
    assert not page.errors, page.errors


@pytest.mark.parametrize('lang', LANGS)
def test_bad_cat_swats_a_cup_off_the_table(page, lang):
    """Böse Katze (3D): start, run to the coffee table, swat – something falls, breaks and scores points."""
    page.set_storage(age=30)
    pg = page.goto(f'games/boese-katze/{lang}/index.html', 1200)
    data = lambda k: pg.evaluate(f"document.getElementById('stage').dataset.{k}")
    pg.click('#go')
    pg.wait_for_timeout(400)
    assert data('state') == 'play'
    pg.keyboard.down('ArrowUp')
    for _ in range(200):
        if float(data('catz')) <= 3.3:
            break
        pg.wait_for_timeout(20)
    pg.keyboard.up('ArrowUp')
    assert float(data('catz')) <= 3.3, 'the cat did not run'
    pg.keyboard.press('e')
    pg.wait_for_timeout(1200)
    assert int(data('knocked')) >= 1 and int(data('score')) > 0
    assert not page.errors, page.errors
