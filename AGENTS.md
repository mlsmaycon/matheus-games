# Instructions for AI agents (and humans) working on My Craft Games

My Craft Games (https://mycraftgames.com) is a static website with free 3D browser games made by Matheus,
a German-speaking child, together with AI assistants. It is hosted on GitHub Pages from `main` (custom domain in `CNAME`).
There is no server and no package manager: plain HTML, CSS and JavaScript, three.js r128 for 3D.

**Read this whole file before changing anything.** Most mistakes on this project come from updating one file
and forgetting the others that depend on it. Every section below ends with the list of files to touch.

---

## 1. Rules that always apply

1. **Every game exists in German and English.** German is the main language (Matheus writes his requests in German).
   Every visible text, button, toast, label, hint and help line needs both versions. No German may remain on English pages.
2. **Every game has an FSK age rating** (0, 6, 12, 16 or 18) with a one-sentence reason in both languages.
   Keep content suitable for the rating: cartoon violence only, no blood, no realistic weapons (e.g. a request for a
   “pistol” became a magic *crystal blaster*), farm animals and pets can never be attacked.
3. **No outside requests.** No CDN scripts, no Google Fonts, no tracking pixels. Libraries live in `assets/vendor/`.
   The only exception is Google Analytics in `assets/analytics.js`, which loads **only after opt-in consent**.
4. **Never hand-edit generated files** (see section 3). Change the source, then rebuild.
5. **Privacy and legal texts must stay true.** If you store new data, add cookies, add a service or change what is
   collected, update `privacy.html` in **both** languages in the same change.
6. **Keep it working on phone and PC:** touch controls, no horizontal scrolling at 400 px width.
7. **Copyright:** © 2026 Matheus · My Craft Games, all rights reserved (`LICENSE.txt`). Keep the notices; keep the
   three.js MIT credit.
8. **Answer Matheus in German**, short and friendly, in kid-friendly words. Explain what you changed and how to try it.

---

## 2. Repository map

```
src/<slug>.html            SOURCE of each game (standalone file, may use CDN three.js and Google Fonts;
                           also served by GitHub Pages, so robots.txt keeps search engines out of /src/)
tools/build_games.py       builds games/<slug>/{de,en}/index.html from src/, then runs tools/seo.py
tools/seo.py               SEO + AI step (titles, meta, JSON-LD, OG images, sitemap, robots, llms.txt, 404)
tools/qr.py                QR code generator for assets/qr-site.png
assets/games.js            game registry (titles, taglines, descriptions, tags, FSK + reasons, cover) – DE + EN
assets/site.js             start page + legal pages logic, all start-page texts (DE + EN), KEYS for "Delete my data"
assets/site.css            start page + legal pages styles
assets/gate.js             age/consent notice on game pages (CONSENT_VERSION)
assets/analytics.js        opt-in Google Analytics + consent banner + "Cookie settings" (KEY mcg-analytics, VER)
assets/vendor/             three.js r128 + licence
assets/qr-site.png, og.png generated images (QR code, social preview of the site)
index.html                 start page (static game cards + JSON-LD are generated between <!--seo:…--> markers)
terms.html, privacy.html, imprint.html   legal pages, German + English in one file
LICENSE.txt, README.md, CONTRIBUTING.md, AGENTS.md, CLAUDE.md, CNAME
games/<slug>/cover.svg     card image (hand-made, 640×400)
games/<slug>/og.png        GENERATED social preview image
games/<slug>/{de,en}/index.html   GENERATED game pages
sitemap.xml, robots.txt, llms.txt, llms-full.txt, 404.html          GENERATED
```

## 3. Generated files – do not edit by hand

| File | Made by |
|---|---|
| `games/<slug>/de/index.html`, `games/<slug>/en/index.html` | `tools/build_games.py` (+ `tools/seo.py`) |
| `games/<slug>/og.png`, `assets/og.png` | `tools/seo.py` |
| `sitemap.xml`, `robots.txt`, `llms.txt`, `llms-full.txt`, `404.html` | `tools/seo.py` |
| Everything between `<!--seo:NAME-->` and `<!--/seo:NAME-->` in `index.html`, `terms.html`, `privacy.html`, `imprint.html` | `tools/seo.py` |
| `assets/qr-site.png` | `tools/qr.py` |

Edits outside the markers in `index.html` and the legal pages are fine – they are hand-written.

## 4. Build and test

```
python3 tools/build_games.py              # all games, then the SEO step
python3 tools/build_games.py nachtburg    # one game, then the SEO step
python3 tools/seo.py                      # SEO step only (after changing assets/games.js or the site pages)
python3 -m http.server 8000               # then open http://localhost:8000
```

Requirements: Python 3, Node.js (reads `assets/games.js`), Playwright with Chromium (pre-renders texts and makes the
OG images; `--no-browser` skips that, but then English pages may show German before JavaScript runs – avoid committing that).

Before every commit, check in a browser (or headless Chromium with `--use-gl=swiftshader`):
- [ ] Start page: age question → cards appear → each game opens; no console errors.
- [ ] Every changed game in **both** languages: starts, plays, no console errors, **no German text on the English page**.
- [ ] Game page without a saved age shows the age notice (it must not redirect).
- [ ] No request to any other host before analytics consent; after “Accept” only `googletagmanager.com` / `google-analytics.com`.
- [ ] 400 px wide viewport: no horizontal scrolling.
- [ ] `git status`: generated files were rebuilt and are committed together with their sources.

## 5. What to update – by task

### A. Change an existing game
1. Edit `src/<slug>.html`. Add every new text to **both** `TXT.de` and `TXT.en` (games in `i18n` mode), or – for the
   older `replace`-mode games (`brainrot-raub`, `versteck-alarm`) – add the German→English pair to `BR_EN` / `VA_EN`
   in `tools/build_games.py` (the build fails if a replacement is not found).
2. If the game now stores something new in `localStorage`: new key → `KEYS` in `assets/site.js` and a row in the
   storage table in `privacy.html` (German **and** English section).
3. If the game’s features changed noticeably: update its `desc` (and maybe `tags`, `fskReason`) in `assets/games.js`
   in both languages, and the game paragraph in `README.md`.
4. If the content changed the age suitability: update `fsk` in `assets/games.js` **and** in the `GAMES` list in
   `tools/build_games.py`, plus `fskReason`.
5. `python3 tools/build_games.py <slug>` → test → commit sources and generated files together.

### B. Add a new game
1. `src/<slug>.html` – standalone page with a `TXT = {de:{…}, en:{…}}` dictionary, `t(key)` lookups, `data-t="key"`
   attributes on static elements, and `<script>window.MW_LANG='de';</script>` in the head (copy the pattern from
   `src/nachtburg.html`). Root element `<div class="app">` is required by the build.
2. `tools/build_games.py` → add a line to `GAMES`: `('src/<slug>.html', '<slug>', FSK, {'de': '…', 'en': '…'}, 'i18n', [])`.
3. `games/<slug>/cover.svg` (640×400, no text needed).
4. `assets/games.js` → new entry: `slug`, `fsk`, `added` (YYYY-MM-DD), `cover`, and `title`, `tagline`, `desc`, `tags`,
   `fskReason` in `de` and `en`.
5. Storage key(s): `KEYS` in `assets/site.js` + rows in `privacy.html` (both languages).
6. `README.md` → games table row and a short description.
7. `python3 tools/build_games.py` – this also refreshes the sitemap, `llms.txt`, `llms-full.txt`, the start-page cards,
   the JSON-LD and the OG image for the new game.
8. Test (section 4) → commit everything in one commit.

### C. Change the start page or legal pages
- Texts on the start page live in `assets/site.js` (`de` and `en` dictionaries) **and** as German defaults in
  `index.html` (`data-i18n` elements). Change both.
- Legal pages contain German (`.l-de`) and English (`.l-en`) sections – change both. When `privacy.html` or
  `terms.html` changes in substance, raise the version/date line at the top of the page. If users must agree again,
  bump `CONSENT_VERSION` in **both** `assets/site.js` and `assets/gate.js`.
- After changing `assets/site.css`, `site.js`, `games.js` or `analytics.js`: raise the cache version `?v=N` in all four
  pages (`index.html`, `terms.html`, `privacy.html`, `imprint.html`), and for `analytics.js` also in
  `tools/build_games.py` (then rebuild), so browsers don’t keep old copies.
- Run `python3 tools/seo.py` afterwards.

### D. Analytics / consent
- Code: `assets/analytics.js` (GA ID `G-0QMCMFM2YN`). Nothing may load before consent.
- Any change in what is collected (new events, new parameters, new service) → update section 3 of `privacy.html` in
  both languages and the README analytics notes. If the purpose changes, raise `VER` in `analytics.js` so everyone is
  asked again.
- Under-16s: the accept button must stay “A parent agrees” / “Ein Elternteil stimmt zu”.

### E. Domain, name or branding
- Domain: `CNAME`, `SITE` in `tools/seo.py`, the address shown in `index.html` (“Play on your phone”), the QR code
  (`python3 tools/qr.py "https://NEW/" assets/qr-site.png`), `README.md`. Then run `tools/seo.py`.
- Site name: `index.html`, legal pages, `assets/site.js`, `assets/analytics.js`, `assets/gate.js` comments,
  `tools/build_games.py` (navigation + titles), `tools/seo.py` (`NAME`), `LICENSE.txt`, `README.md`, this file. Rebuild.

## 6. Git
- Work on `main` only if the owner asked for it; otherwise use a branch.
- Commit sources and their generated files together. Clear commit messages in English.
- `git pull --rebase` before pushing – the owner sometimes commits directly on GitHub (e.g. `CNAME`).
