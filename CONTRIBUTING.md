# Contributing to My Craft Games

The full instructions – rules, repository map, generated files and a step-by-step list of **which files to update
for each kind of change** – are in [AGENTS.md](AGENTS.md). They apply to people and AI agents alike.

## Quick checklist for a new game

- [ ] Source in `src/<slug>.html` with German and English texts (`TXT.de` / `TXT.en`, `window.MW_LANG`).
- [ ] Line in `GAMES` in `tools/build_games.py` (slug, FSK, titles, `'i18n'`).
- [ ] Cover `games/<slug>/cover.svg` (640×400).
- [ ] Registry entry in `assets/games.js` (`slug`, `fsk`, `added`, `cover`, and `title`, `tagline`, `desc`, `tags`,
      `fskReason` in `de` and `en`). FSK = 0, 6, 12, 16 or 18, using the [FSK criteria](https://www.fsk.de/?seitid=70&tid=70).
- [ ] New `localStorage` keys in `KEYS` (`assets/site.js`) and in the storage table of `privacy.html` (both languages).
- [ ] Row in the games table in `README.md`.
- [ ] `python3 tools/build_games.py` (builds both languages, adds age notice, navigation, analytics, copyright, then
      runs the SEO step: sitemap, `llms.txt`, start-page cards, JSON-LD, preview image).
- [ ] Tested in both languages on PC and phone width, no German on the English page, no console errors.
- [ ] Sources and generated files committed together.

The build takes care of the age gate, the navigation bar, removing outside requests (CDN three.js → `assets/vendor/`,
Google Fonts → system fonts), opt-in analytics and the copyright line – don’t add those by hand.
