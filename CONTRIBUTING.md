# Contributing to My Craft Games

The full instructions – rules, repository map, what the build generates and a step-by-step list of **which files to
update for each kind of change** – are in [AGENTS.md](AGENTS.md). They apply to people and AI agents alike.

## Quick checklist for a new game

- [ ] Source `src/<slug>.html` with German and English texts (`TXT.de` / `TXT.en`, `window.MW_LANG`).
- [ ] Line in `GAMES` in `tools/build.py` (slug, FSK, titles, `'i18n'`).
- [ ] Cover `site/games/<slug>/cover.svg` (640×400).
- [ ] Entry in `site/assets/games.js` (`slug`, `fsk`, `added`, `cover`, and `title`, `tagline`, `desc`, `tags`,
      `fskReason` in `de` and `en`). FSK = 0, 6, 12, 16 or 18, using the [FSK criteria](https://www.fsk.de/?seitid=70&tid=70).
- [ ] New `localStorage` keys in `KEYS` (`site/assets/site.js`) and in the storage table of `site/privacy.html` (both languages).
- [ ] Row in the games table in `README.md`.
- [ ] `python3 tools/build.py && python3 -m pytest -q tests` – all green.
- [ ] Commit the sources (never `dist/`). CI builds, tests and publishes.

The build adds the age notice, the navigation bar, opt-in analytics, the copyright line and all SEO data, and removes
outside requests (CDN three.js → local copy, Google Fonts → system fonts). Don’t add those by hand.
