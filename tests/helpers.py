import html, re

# Words that give away German text on an English page. Kept short on purpose: common words only.
GERMAN = re.compile(r"[äöüßÄÖÜ]|\b(und|oder|nicht|der|die|das|dem|den|mit|ist|du|dein|deine|dich|Spiel|Spiele|Spieler|"
                    r"Haus|Nacht|Holz|Stein|Zurück|Nochmal|Truhe|Essen|Steuerung|Jahren|Alter|weiter|Los geht)\b")
# Names and words that are allowed on English pages (creature names, the link to the German version …)
ALLOWED = ['Deutsch', 'Deutsche Version', 'Säge', 'Brezel', 'Wolkonzo', 'Sockosaurus', 'Kuhmelon', 'Gurkelino',
           'Toastino', 'Banano', 'Pinguino', 'Kaktusso', 'Spaghettor', 'Hamsterino', 'Kaffeekanne', 'Radieschen', 'Brumm']


def german_leftovers(text):
    for a in ALLOWED:
        text = text.replace(a, '')
    return sorted({m.group(0) for m in GERMAN.finditer(text)})


def visible_static_text(page_html):
    """Text a crawler without JavaScript sees: body without scripts, styles and links to the German version."""
    body = page_html.split('<body', 1)[-1]
    body = re.sub(r'<script[\s\S]*?</script>|<style[\s\S]*?</style>', ' ', body)
    body = re.sub(r'<a [^>]*hreflang="de"[^>]*>[\s\S]*?</a>', ' ', body)
    return html.unescape(re.sub(r'<[^>]+>', ' ', body))


def start_game(pg):
    """Press the start button of whatever game is open (games differ a little)."""
    for sel in ['#go', '[data-mode="hide"]', 'button.go']:
        el = pg.query_selector(sel)
        if el and el.is_visible():
            el.click()
            return sel
    return None
