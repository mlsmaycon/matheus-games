#!/usr/bin/env python3
"""
My Craft Games – build the whole website into dist/ (this folder is what GitHub Pages serves; it is not committed).

    python3 tools/build.py              # copy site/, build every game (German + English), run tools/seo.py
    python3 tools/build.py nachtburg    # same, but rebuild only this game's pages (others are kept from the last build)
    python3 tools/build.py --no-seo     # skip the SEO step
    python3 tools/build.py --no-browser # SEO step without Playwright (no pre-rendering, no preview images)

Each source in src/<slug>.html is a standalone game (three.js from a CDN, Google Fonts allowed).
The build makes dist/games/<slug>/de/index.html and dist/games/<slug>/en/index.html:
  * removes outside requests (CDN three.js -> assets/vendor, Google Fonts -> system fonts)
  * adds the age gate (assets/gate.js), opt-in analytics (assets/analytics.js), the top navigation
    (back link, FSK badge, language switch) and the copyright line
  * English version: either the source has a TXT.de/TXT.en dictionary and reads window.MW_LANG
    (mode 'i18n' – preferred for new games), or a list of German->English text replacements (mode 'replace')
"""
import re, sys, json, os, subprocess

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(REPO, 'dist')
ROOT = '../../../'

NAV_CSS = """
.mw-nav{max-width:1100px;margin:0 auto 4px;display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;font-family:system-ui,-apple-system,"Segoe UI",sans-serif;font-weight:700;font-size:14px}
.mw-nav a{color:inherit;opacity:.85;text-decoration:none;padding:6px 10px;border-radius:999px;background:#ffffff14}
.mw-nav a:hover,.mw-nav a:focus-visible{opacity:1;background:#ffffff26;outline:none}
.mw-nav .mw-right{display:flex;gap:8px;align-items:center}
.mw-copy{max-width:1100px;margin:14px auto 6px;padding:0 12px;text-align:center;font:12px/1.4 system-ui,sans-serif;opacity:.6}
.mw-copy a{color:inherit}
.mw-fsk{display:inline-flex;align-items:center;gap:4px;padding:4px 10px;border-radius:8px;font-weight:900;color:#111;background:var(--mw-fsk,#fff)}
"""

FSK_COL = {0: '#ffffff', 6: '#ffd400', 12: '#2fb34a', 16: '#2f8fe0', 18: '#e2312c'}


def page(src_path, slug, fsk, lang, title, replacements, fonts_fallback):
    s = open(src_path, encoding='utf-8').read()
    # third-party requests out: Google Fonts and CDN three.js
    s = re.sub(r'<link rel="preconnect" href="https://fonts.googleapis.com">\n', '', s)
    s = re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis.com/[^"]*">\n', '', s)
    s = s.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>',
                  f'<script src="{ROOT}assets/vendor/three.r128.min.js"></script>')
    assert 'googleapis' not in s and 'cdnjs' not in s, 'external request left'
    for a, b in fonts_fallback:
        assert a in s, ('font', a)
        s = s.replace(a, b)
    s = s.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
    if lang == 'en':
        for a, b in replacements:
            n = s.count(a)
            if n == 0:
                print('MISSING:', a[:90]); sys.exit(1)
            s = s.replace(a, b)
    other = 'en' if lang == 'de' else 'de'
    back = 'My Craft Games'
    switch = 'English' if lang == 'de' else 'Deutsch'
    fsk_lbl = f'FSK {fsk}'
    nav = (f'<nav class="mw-nav" aria-label="My Craft Games">'
           f'<a href="{ROOT}index.html">← {back}</a>'
           f'<span class="mw-right"><span class="mw-fsk" style="--mw-fsk:{FSK_COL[fsk]}" title="{"Altersempfehlung" if lang=="de" else "Age rating"}">{fsk_lbl}</span>'
           f'<a href="../{other}/index.html" hreflang="{other}" lang="{other}">{switch}</a></span></nav>\n')
    head, body = s.split('<div class="app">', 1)
    head = head.replace('<style>', '<style>\n*{box-sizing:border-box}\nbody{margin:0}\n[hidden]{display:none!important}' + NAV_CSS, 1)
    title_tag = re.search(r'<title>.*?</title>', head).group(0)
    head = head.replace(title_tag, f'<title>{title} · My Craft Games</title>')
    copy = ('© 2026 My Craft Games. ' + ('Alle Rechte vorbehalten.' if lang == 'de' else 'All rights reserved.')
            + f' 3D: <a href="{ROOT}assets/vendor/three.LICENSE.txt">three.js</a> (MIT)')
    out = (f'<!doctype html>\n<!-- © 2026 My Craft Games. All rights reserved. three.js © three.js authors, MIT licence. -->\n<html lang="{lang}">\n<head>\n<meta charset="utf-8">\n'
           f'<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
           f'<script src="{ROOT}assets/gate.js" data-fsk="{fsk}" data-game="{slug}"></script>\n'
           f'<script src="{ROOT}assets/analytics.js?v=10" defer></script>\n'
           + head + '</head>\n<body>\n' + nav + '<div class="app">' + body.rstrip() + f'\n<p class="mw-copy">{copy}</p>\n</body>\n</html>\n')
    return out


BR_FONTS = [('--display:"Lilita One","Arial Rounded MT Bold","Trebuchet MS",sans-serif;',
             '--display:"Arial Rounded MT Bold","SF Pro Rounded",ui-rounded,"Trebuchet MS",system-ui,sans-serif;'),
            ('--body:"Nunito",system-ui,', '--body:ui-rounded,system-ui,')]
VA_FONTS = [('--display:"Fredoka","Arial Rounded MT Bold","Trebuchet MS",sans-serif;',
             '--display:"Arial Rounded MT Bold","SF Pro Rounded",ui-rounded,"Trebuchet MS",system-ui,sans-serif;'),
            ('--body:"Nunito",system-ui,', '--body:ui-rounded,system-ui,')]

BR_EN = [
    ('<h1>Brainrot-Raub<small>Kaufen, kassieren, klauen. Schütz deine Basis.</small></h1>',
     '<h1>Brainrot Heist<small>Buy, cash in, steal. Protect your base.</small></h1>'),
    ('<span>Geld</span>', '<span>Money</span>'),
    ('<span>pro Sek.</span>', '<span>per sec.</span>'),
    ('Lade 3D-Welt …', 'Loading 3D world …'),
    ('Aktion · E', 'Action · E'),
    ('Verkaufen · Q', 'Sell · Q'),
    ('<strong>Turbo-Schuhe</strong>', '<strong>Turbo Shoes</strong>'),
    ('<strong>Basis-Ausbau</strong>', '<strong>Base Upgrade</strong>'),
    ('<strong>Laserschild</strong>', '<strong>Laser Shield</strong>'),
    ('<b>Bewegen:</b> WASD / Pfeiltasten oder im Spielfeld ziehen. <b>Mausrad</b> zoomt. <b>E</b> kauft Figuren vom Band oder klaut sie aus fremden Basen. Bring sie in deine gelbe Basis und lauf über die Felder, um Geld einzusammeln. Die <b>rote Platte</b> schaltet dein Laserschild ein. Diebe kannst du anrempeln, um deine Figur zurückzuholen.',
     '<b>Move:</b> WASD / arrow keys or drag on the playfield. <b>Mouse wheel</b> zooms. <b>E</b> buys creatures from the belt or steals them from other bases. Bring them to your yellow base and walk over the pads to collect money. The <b>red plate</b> turns on your laser shield. Bump into thieves to get your creature back.'),
    ('>Neu starten<', '>Restart<'),
    ("'3D konnte nicht geladen werden.'", "'3D could not be loaded.'"),
    ("name:'Gewöhnlich'", "name:'Common'"), ("name:'Selten'", "name:'Rare'"), ("name:'Episch'", "name:'Epic'"),
    ("name:'Legendär'", "name:'Legendary'"), ("name:'Mythisch'", "name:'Mythic'"), ("name:'Geheim'", "name:'Secret'"),
    ("name:'Deine Basis'", "name:'Your Base'"), ("name:'Kalles Basis'", "name:\"Kalle's Base\""),
    ("name:'Ronjas Basis'", "name:\"Ronja's Base\""), ("name:'Bodos Basis'", "name:\"Bodo's Base\""),
    ("${t.n} ist auf dem Band!", "${t.n} is on the belt!"),
    ("'Deine Basis ist voll. Verkauf etwas oder bau aus.'", "'Your base is full. Sell something or upgrade.'"),
    ("`Zu wenig Geld: ${fmt(it.t.cost)} nötig.`", "`Not enough money: you need ${fmt(it.t.cost)}.`"),
    ("'Die Basis ist geschützt.'", "'That base is shielded.'"),
    ("`Geklaut: ${player.carry.t.n}! Lauf nach Hause!`", "`Stolen: ${player.carry.t.n}! Run home!`"),
    ("`${bot.name} klaut deinen ${s.c.n}! Hinterher!`", "`${bot.name} is stealing your ${s.c.n}! After them!`"),
    ("`${bot.name} hat dich erwischt!`", "`${bot.name} caught you!`"),
    ("`${t.n} gehört jetzt dir!`", "`${t.n} is yours now!`"),
    ("`Neu im Index: ${t.n}`", "`New in your index: ${t.n}`"),
    ("`Laserschild an: ${shieldDur()} Sekunden`", "`Laser shield on: ${shieldDur()} seconds`"),
    ("`Zurückerobert: ${bot.carry.t.n}`", "`Recovered: ${bot.carry.t.n}`"),
    ("'Betäubt …'", "'Stunned …'"),
    ("'Basis voll – verkauf etwas (Q)'", "'Base full – sell something (Q)'"),
    ("'Ab nach Hause!'", "'Head home!'"),
    ("'Geschützt'", "'Shielded'"),
    ("`[E] ${rs.s.c.n} klauen`", "`[E] Steal ${rs.s.c.n}`"),
    ("[Q] verkaufen · ", "[Q] Sell · "),
    ("`Schild bereit in ${Math.ceil(pb.cd)}s`:'Schild-Platte'", "`Shield ready in ${Math.ceil(pb.cd)}s`:'Shield plate'"),
    ("lab(`Schild ${Math.ceil(b.shield)}s`", "lab(`Shield ${Math.ceil(b.shield)}s`"),
    ("`Stufe ${up.speed}/${SPEED_MAX} · +12 % Tempo`", "`Level ${up.speed}/${SPEED_MAX} · +12% speed`"),
    ("'Maximal'", "'Maxed'"),
    ("`${playerBase.unlocked} von 10 Plätzen`", "`${playerBase.unlocked} of 10 slots`"),
    ("`+2 Plätze · ${fmt(slotCost())}`", "`+2 slots · ${fmt(slotCost())}`"),
    ("`Schild hält ${shieldDur()} s`", "`Shield lasts ${shieldDur()} s`"),
    ("'Schneller unterwegs!'", "'Faster on your feet!'"),
    ("'Zwei neue Plätze frei!'", "'Two new slots unlocked!'"),
    ("'Schild hält länger!'", "'Shield lasts longer!'"),
    ("'Wirklich? Nochmal klicken'", "'Sure? Click again'"),
    ("b.textContent='Neu starten'", "b.textContent='Restart'"),
    ("'Neues Spiel gestartet'", "'New game started'"),
    ("'Lauf zum Band und kauf deine erste Figur mit E!'", "'Walk to the belt and buy your first creature with E!'"),
]

VA_EN = [
    ('<h1>Versteck-Alarm<small>Verstecken oder suchen – im ganzen Haus.</small></h1>',
     '<h1>Hide Alarm<small>Hide or seek – all over the house.</small></h1>'),
    ('<span>Überlebt</span>', '<span>Survived</span>'),
    ('<span>Beste Suche</span>', '<span>Best search</span>'),
    ('aria-label="Kichern hören">Kichern<b', 'aria-label="Hear a giggle">Giggle<b'),
    ('>Wähle einen Modus<', '>Choose a mode<'),
    ('Augen zu! Die Kinder verstecken sich …', 'Eyes closed! The kids are hiding …'),
    ('<h2>Versteck-Alarm</h2>', '<h2>Hide Alarm</h2>'),
    ('Ein Haus, ein Garten, eine Garage und jede Menge Verstecke. Willst du dich vor dem Sucher verstecken oder selbst suchen?',
     'A house, a garden, a garage and loads of hiding spots. Do you want to hide from the seeker or be the seeker?'),
    ('>Verstecken<small>Du + 3 Kinder gegen den Sucher</small>', '>Hide<small>You + 3 kids against the seeker</small>'),
    ('>Suchen<small>Finde 4 Kinder in 120 Sekunden</small>', '>Seek<small>Find 4 kids in 120 seconds</small>'),
    ('>Nochmal<', '>Play again<'),
    ('>Modus wählen<', '>Choose mode<'),
    ('Aktion · E', 'Action · E'),
    ('>Schleichen · Shift<', '>Sneak · Shift<'),
    ('>Kichern hören · H (3)<', '>Hear a giggle · H (3)<'),
    ('>Ton an · M<', '>Sound on · M<'),
    ('<b>Steuerung:</b> WASD / Pfeiltasten oder im Spielfeld ziehen, Mausrad zoomt, <b>E</b> versteckt dich oder durchsucht ein Versteck, <b>Shift</b> schleicht. <b>Verstecken:</b> Du und drei Kinder gegen den Sucher. Überlebe 100 Sekunden. <b>Suchen:</b> Finde alle vier Kinder in 120 Sekunden. <b>H</b> lässt das nächste Kind kichern (3× pro Runde, Ton an).',
     '<b>Controls:</b> WASD / arrow keys or drag on the playfield, mouse wheel zooms, <b>E</b> hides you or searches a hiding spot, <b>Shift</b> sneaks. <b>Hide:</b> You and three kids against the seeker. Survive 100 seconds. <b>Seek:</b> Find all four kids in 120 seconds. <b>H</b> makes the nearest kid giggle (3× per round, sound on).'),
    ("'3D konnte nicht geladen werden.'", "'3D could not be loaded.'"),
    ("{n:'Schlafzimmer'", "{n:'Bedroom'"), ("{n:'Bad'", "{n:'Bathroom'"), ("{n:'Garten'", "{n:'Garden'"),
    ("{n:'Wohnzimmer'", "{n:'Living room'"), ("{n:'Küche'", "{n:'Kitchen'"),
    ("kind==='Garten'", "kind==='Garden'"), ("kind==='Bad'||kind==='Küche'", "kind==='Bathroom'||kind==='Kitchen'"),
    ("{n:'Schrank',hide:1,sight:1,verb:'im Schrank'}", "{n:'wardrobe',hide:1,sight:1,verb:'in the wardrobe'}"),
    ("{n:'Bett',hide:1,sight:0,verb:'unter dem Bett'}", "{n:'bed',hide:1,sight:0,verb:'under the bed'}"),
    ("{n:'Kisten',hide:1,sight:1,verb:'hinter den Kisten'}", "{n:'boxes',hide:1,sight:1,verb:'behind the boxes'}"),
    ("{n:'Badewanne',hide:1,sight:0,verb:'in der Badewanne'}", "{n:'bathtub',hide:1,sight:0,verb:'in the bathtub'}"),
    ("{n:'Wäschekorb',hide:1,sight:0,verb:'im Wäschekorb'}", "{n:'laundry basket',hide:1,sight:0,verb:'in the laundry basket'}"),
    ("{n:'Busch',hide:1,sight:1,verb:'im Busch'}", "{n:'bush',hide:1,sight:1,verb:'in the bush'}"),
    ("{n:'Mülltonne',hide:1,sight:0,verb:'in der Mülltonne'}", "{n:'trash can',hide:1,sight:0,verb:'in the trash can'}"),
    ("{n:'Sofa',hide:1,sight:0,verb:'hinter dem Sofa'}", "{n:'sofa',hide:1,sight:0,verb:'behind the sofa'}"),
    ("{n:'Esstisch',hide:1,sight:0,verb:'unter dem Tisch'}", "{n:'dining table',hide:1,sight:0,verb:'under the table'}"),
    ("{n:'Auto',hide:1,sight:1,verb:'im Kofferraum'}", "{n:'car',hide:1,sight:1,verb:'in the car trunk'}"),
    ("{n:'Regal',", "{n:'shelf',"), ("{n:'Tisch',", "{n:'table',"), ("{n:'Kühlschrank',", "{n:'fridge',"),
    ("{n:'Küchenzeile',", "{n:'counter',"), ("{n:'Baum',", "{n:'tree',"),
    ("'Ton an · M':'Ton aus · M'", "'Sound on · M':'Sound off · M'"),
    ("'Der Sucher zählt bis 12.'", "'The seeker is counting to 12.'"),
    ("?'ihn':'sie'", "?'him':'her'"),
    ("`Kichern hören · H (${hints})`", "`Hear a giggle · H (${hints})`"),
    ("'Da ist kein Platz.'", "'No room in there.'"),
    ("'Oh nein, er hat gesehen, wo du hin bist!'", "'Oh no, he saw where you went!'"),
    ("`Versteckt ${s.K.verb}. Psst!`", "`Hidden ${s.K.verb}. Shh!`"),
    ("'leer'", "'empty'"),
    ("`${msg} Du hast ${survived.toFixed(0)} von 100 Sekunden durchgehalten. ${left?`${left} ${left===1?'Kind ist':'Kinder sind'} noch versteckt.`:'Alle anderen hatte er schon vor dir.'}`",
     "`${msg} You lasted ${survived.toFixed(0)} of 100 seconds. ${left?`${left} ${left===1?'kid is':'kids are'} still hidden.`:'He had already found everyone else.'}`"),
    ("'Erwischt!'", "'Caught!'"),
    ("toast('Entdeckt!'", "toast('Spotted!'"),
    ("`Der Sucher hat ${tgt.name} entdeckt und rennt hinterher!`", "`The seeker spotted ${tgt.name} and is giving chase!`"),
    ("`Der Sucher hat dich ${s.goalSpot.K.verb} gefunden.`", "`The seeker found you ${s.goalSpot.K.verb}.`"),
    ("'Der Sucher hat dich geschnappt.'", "'The seeker grabbed you.'"),
    ("'auf der Flucht'", "'on the run'"),
    ("'Er hat dich gehört!'", "'He heard you!'"),
    ("`${h.name} flitzt davon! Fang ${pron(h)}!`", "`${h.name} dashes off! Catch ${pron(h)}!`"),
    ("`${h.name} springt aus dem Versteck und rennt!`", "`${h.name} jumps out and runs!`"),
    ("'Gefunden!'", "'Found!'"),
    ("`Der Sucher hat ${h.name} ${how} gefunden! ${left?`Noch ${left} + du versteckt.`:'Jetzt bist nur noch du übrig!'}`",
     "`The seeker found ${h.name} ${how}! ${left?`${left} + you still hidden.`:'Now it is just you left!'}`"),
    ("`${h.name} gefunden! (${n}/4)`", "`Found ${h.name}! (${n}/4)`"),
    ("'Alle gefunden!'", "'Found them all!'"),
    ("`Du hast alle vier Kinder in ${t.toFixed(1)} Sekunden gefunden.${rec.bestSeek===t?' Neuer Rekord!':''}`",
     "`You found all four kids in ${t.toFixed(1)} seconds.${rec.bestSeek===t?' New record!':''}`"),
    ("'Fertig oder nicht, ich komme!'", "'Ready or not, here I come!'"),
    ("toast('Ich komme!'", "toast('Here I come!'"),
    ("'Geschafft!'", "'You made it!'"),
    ("`Der Sucher hat dich 100 Sekunden lang nicht gefunden. ${f?`Von den anderen hat er ${f} erwischt, ${left} ${left===1?'hat':'haben'} wie du durchgehalten.`:'Und auch kein anderes Kind. Alle haben gewonnen!'}`",
     "`The seeker didn't find you for 100 seconds. ${f?`He caught ${f} of the others, ${left} made it like you.`:'And no other kid either. Everyone wins!'}`"),
    ("'Zeit um!'", "'Time is up!'"),
    ("`Du hast ${n} von 4 Kindern gefunden.`", "`You found ${n} of 4 kids.`"),
    ("lab('Sucher',", "lab('Seeker',"),
    ("`Versteckt ${player.spot.K.verb} · [E] raus`", "`Hidden ${player.spot.K.verb} · [E] get out`"),
    ("{t:'Besetzt',", "{t:'Taken',"),
    ("`[E] Verstecken: ${s.K.verb}`", "`[E] Hide ${s.K.verb}`"),
    ("`[E] ${s.K.n} durchsuchen`", "`[E] Search the ${s.K.n}`"),
    ("st.textContent='Wähle einen Modus'", "st.textContent='Choose a mode'"),
    ("`Sucher zählt … ${Math.ceil(countT)}`", "`Seeker counting … ${Math.ceil(countT)}`"),
    ("'Er hat dich gesehen!'", "'He has seen you!'"),
    ("'Puls: RASEND':d<7?'Puls: schneller':'Puls: ruhig'", "'Heartbeat: RACING':d<7?'Heartbeat: faster':'Heartbeat: calm'"),
    ("'Du schleichst':'Unterwegs'", "'Sneaking':'On the move'"),
    ("` · Andere: ${left}/${hiders.length}`", "` · Others: ${left}/${hiders.length}`"),
    ("'Augen zu …':`Gefunden: ${n}/4`", "'Eyes closed …':`Found: ${n}/4`"),
]

GAMES = [
    # (source, slug, FSK, titles, English replacements or 'i18n', font fallbacks)
    ('src/brainrot-raub.html', 'brainrot-raub', 6, {'de': 'Brainrot-Raub', 'en': 'Brainrot Heist'}, BR_EN, BR_FONTS),
    ('src/versteck-alarm.html', 'versteck-alarm', 0, {'de': 'Versteck-Alarm', 'en': 'Hide Alarm'}, VA_EN, VA_FONTS),
    ('src/kuerbisnacht.html', 'kuerbisnacht', 6, {'de': 'Kürbisnacht', 'en': 'Pumpkin Night'}, 'i18n', []),
    ('src/huehnerchaos.html', 'huehnerchaos', 0, {'de': 'Hühnerchaos', 'en': 'Chicken Chaos'}, 'i18n', []),
    ('src/nachtburg.html', 'nachtburg', 6, {'de': 'Nachtburg', 'en': 'Night Fort'}, 'i18n', []),
    ('src/sternen-einhorn.html', 'sternen-einhorn', 0, {'de': 'Sternen-Einhorn', 'en': 'Star Unicorn'}, 'i18n', []),
]

GERMAN = re.compile(r"[äöüÄÖÜß]|\b(und|oder|nicht|der|die|das|dich|deine?|Basis|Kinder?|Sucher|Versteck\w*|Geld|Schild|nochmal|gefunden|klauen|Spiel)\b")

only = [a for a in sys.argv[1:] if not a.startswith('--')]
# 1) copy the hand-written site (start page, legal pages, assets, covers) and the licence into dist/
import shutil
if not only and os.path.isdir(DIST):
    shutil.rmtree(DIST)
shutil.copytree(os.path.join(REPO, 'site'), DIST, dirs_exist_ok=True)
shutil.copy(os.path.join(REPO, 'LICENSE.txt'), os.path.join(DIST, 'LICENSE.txt'))
# 2) build the game pages
for src, slug, fsk, titles, rep, fonts in GAMES:
    if only and slug not in only:
        continue
    for lang in ('de', 'en'):
        if rep == 'i18n':
            out = page(os.path.join(REPO, src), slug, fsk, lang, titles[lang], [], fonts)
            assert "window.MW_LANG='de';" in out, f'{src}: needs <script>window.MW_LANG=\'de\';</script> for i18n mode'
            out = out.replace("window.MW_LANG='de';", f"window.MW_LANG='{lang}';")
        else:
            out = page(os.path.join(REPO, src), slug, fsk, lang, titles[lang], rep, fonts)
        os.makedirs(f'{DIST}/games/{slug}/{lang}', exist_ok=True)
        path = f'{DIST}/games/{slug}/{lang}/index.html'
        open(path, 'w', encoding='utf-8').write(out)
        if lang == 'en' and rep != 'i18n':
            # report German-looking leftovers in visible strings (skip creature/kid names and code identifiers)
            for i, line in enumerate(out.split('\n'), 1):
                for m in re.finditer(r"'[^'\n]*'|`[^`\n]*`|>[^<>\n]{2,}<", line):
                    t = m.group(0)
                    if GERMAN.search(t) and not re.search(r"Brumm|Säge|Toastino|Brezel|Wolkonzo|Sockosaurus|Kuhmelon|Banano|Gurkelino|Kaffeekanne|Radieschen|Pinguino|Kaktusso|Spaghettor|Hamsterino|brainrot-raub|versteck-alarm|Matheus", t):
                        print(f'{slug}/en:{i}: {t[:120]}')
        print('wrote', path, len(out))

if '--no-seo' not in sys.argv:
    subprocess.run([sys.executable, os.path.join(REPO, 'tools', 'seo.py'), '--out', DIST] + (['--no-browser'] if '--no-browser' in sys.argv else []), check=True)
