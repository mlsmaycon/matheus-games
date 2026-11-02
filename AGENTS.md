# Instructions for AI agents (and humans) working on My Craft Games

My Craft Games (https://mycraftgames.com) is a static website with free 3D browser games made by Matheus,
a German-speaking child, together with AI assistants. Plain HTML, CSS and JavaScript, three.js r128 for 3D.
The repository holds **sources only**. GitHub Actions builds the website into `dist/`, runs the tests and – for
pushes to `main` – publishes `dist/` to GitHub Pages (custom domain `mycraftgames.com`).

**Read this whole file before changing anything.** Most mistakes on this project come from updating one file
and forgetting the others that depend on it. Section 5 lists, per kind of change, every file to touch.

---

## 1. Rules that always apply

1. **Every game exists in German and English.** German is the main language (Matheus writes his requests in German).
   Every visible text, button, toast, label, hint and help line needs both versions. No German may remain on English pages.
2. **Every game has an FSK age rating** (0, 6, 12, 16 or 18) with a one-sentence reason in both languages.
   Keep content suitable for the rating: cartoon violence only, no blood, no realistic weapons (a request for a
   “pistol” became a magic *crystal blaster*), farm animals and pets can never be attacked.
3. **No outside requests.** No CDN scripts, no Google Fonts, no tracking pixels in the published site. Libraries live in
   `site/assets/vendor/`. The only exception is Google Analytics in `site/assets/analytics.js`, which loads **only after
   opt-in consent**. (Sources in `src/` may use the CDN – the build replaces it.)
4. **Never commit `dist/`.** It is generated. Change sources, run the build, run the tests.
5. **Privacy and legal texts must stay true.** If you store new data, add cookies, add a service or change what is
   collected, update `site/privacy.html` in **both** languages in the same change.
6. **Phone and PC:** touch controls, no horizontal scrolling at 400 px width (tested).
7. **Copyright:** © 2026 My Craft Games, all rights reserved (`LICENSE.txt`). Keep the notices and the
   three.js MIT credit.
8. **Tests must pass** (`python3 -m pytest tests`). Add or update tests when you add features (section 4).
9. **Answer Matheus in German**, short, friendly and kid-friendly. Say what changed and how to try it.

---

## 2. Repository map

```
src/<slug>.html          SOURCE of each game (standalone page; may use CDN three.js and Google Fonts)
site/                    hand-written website, copied 1:1 into dist/
  index.html             start page (age question, game cards drawn from assets/games.js)
  terms.html privacy.html imprint.html   legal pages, German (.l-de) + English (.l-en) in one file
  assets/games.js        game registry: titles, taglines, descriptions, tags, FSK + reasons, cover (DE + EN)
  assets/site.js         start page + legal pages logic and texts (DE + EN), KEYS for “Delete my data”, CONSENT_VERSION
  assets/site.css        start page + legal pages styles
  assets/gate.js         age notice on game pages (CONSENT_VERSION – keep equal to site.js)
  assets/analytics.js    opt-in Google Analytics, consent banner, “Cookie settings” (KEY mcg-analytics, VER)
  assets/vendor/         three.js r128 + licence
  assets/qr-site.png     QR code to the site (made with tools/qr.py)
  games/<slug>/cover.svg card image, 640×400
  CNAME, .nojekyll
tools/build.py           builds the site into dist/ (copies site/, builds games/<slug>/{de,en}/, runs seo.py)
tools/seo.py             SEO + AI step on dist/ (titles, meta, JSON-LD, preview images, static cards, sitemap,
                         robots.txt, llms.txt, llms-full.txt, 404.html, pre-rendered texts)
tools/qr.py              QR code generator
tests/                   pytest + Playwright test suite (structure, built site, browser end-to-end)
.github/workflows/pages.yml   CI: build → test → deploy (deploy only on main)
requirements-dev.txt     pytest, playwright
LICENSE.txt README.md CONTRIBUTING.md AGENTS.md CLAUDE.md
dist/                    GENERATED, git-ignored – this is exactly what goes online
```

## 3. What the build generates (never edit these, never commit `dist/`)

- `dist/games/<slug>/de/index.html`, `dist/games/<slug>/en/index.html` – game pages with age notice, navigation,
  analytics, copyright, SEO head, “About this game” section, pre-rendered texts.
- `dist/games/<slug>/og.png`, `dist/assets/og.png` – social preview images.
- `dist/index.html` and legal pages: `site/` copies plus SEO blocks between `<!--seo:NAME-->` markers
  (static game cards, JSON-LD, canonical/hreflang, Open Graph). **Never put these markers into `site/`** (a test checks).
- `dist/sitemap.xml`, `robots.txt`, `llms.txt`, `llms-full.txt`, `404.html`.

## 4. Build and test

```
pip install -r requirements-dev.txt && python3 -m playwright install chromium   # once
python3 tools/build.py                 # whole site into dist/ (needs Node.js for reading games.js)
python3 tools/build.py nachtburg       # rebuild one game’s pages (+ SEO step)
python3 -m pytest -q tests             # all tests (~3 min); builds dist/ first if it is missing
python3 -m pytest -q tests/test_structure.py   # fast checks only (no browser)
cd dist && python3 -m http.server 8000 # play locally at http://localhost:8000
```

The tests check, among other things: registry entries complete in both languages; `tools/build.py` and
`site/assets/games.js` list the same games and FSK; every `localStorage` key is in `KEYS` and in the privacy table
(DE + EN); start-page texts exist in both languages; cache versions are equal; every game page has the age gate, SEO
head, valid JSON-LD and preview image; no German on English pages (with and without JavaScript); sitemap/robots/llms;
no sources in `dist/`; every game starts in both languages without errors or outside requests; the age notice instead
of a redirect; analytics only after consent and “A parent agrees” for under-16s; no horizontal scrolling at 400 px.

When you add a feature, add a test for it in the matching file (`tests/test_structure.py`, `tests/test_built_site.py`
or `tests/test_browser.py`). Allowed German-looking names on English pages (creature names etc.) go into `ALLOWED` in
`tests/helpers.py`.

## 5. What to update – by task

### A. Change an existing game
1. Edit `src/<slug>.html`. Every new text goes into **both** `TXT.de` and `TXT.en` (games in `i18n` mode). For the two
   older `replace`-mode games (`brainrot-raub`, `versteck-alarm`), add the German→English pair to `BR_EN` / `VA_EN` in
   `tools/build.py` (the build stops if a replacement is not found).
2. New `localStorage` key → `KEYS` in `site/assets/site.js` and a row in the storage table of `site/privacy.html`
   (German **and** English).
3. Features changed noticeably → `desc` (maybe `tags`, `fskReason`) in `site/assets/games.js` (both languages) and the
   game text in `README.md`.
4. Age suitability changed → `fsk` in `site/assets/games.js` **and** in `GAMES` in `tools/build.py`, plus `fskReason`.
5. Build, test, commit the sources.

### B. Add a new game
1. `src/<slug>.html` with `TXT = {de:{…}, en:{…}}`, `t(key)`, `data-t="key"` on static elements and
   `<script>window.MW_LANG='de';</script>` in the head; root element `<div class="app">` (copy the pattern from
   `src/nachtburg.html`).
2. `tools/build.py` → line in `GAMES`: `('src/<slug>.html', '<slug>', FSK, {'de': '…', 'en': '…'}, 'i18n', [])`.
3. `site/games/<slug>/cover.svg` (640×400).
4. `site/assets/games.js` → entry with `slug`, `fsk`, `added` (YYYY-MM-DD), `cover`, and `title`, `tagline`, `desc`,
   `tags`, `fskReason` in `de` and `en`.
5. Storage key(s) → `KEYS` in `site/assets/site.js` + rows in `site/privacy.html` (both languages).
6. `README.md` → games table row and a short description.
7. Build (sitemap, `llms*.txt`, cards, JSON-LD and preview image update automatically), test, commit.

### C. Change the start page or legal pages
- Start-page texts live in `site/assets/site.js` (`de` and `en`) **and** as German defaults in `site/index.html`
  (`data-i18n` elements). Change both.
- Legal pages: change the German (`.l-de`) and English (`.l-en`) section. Substantial change → raise the version/date
  line at the top. If users must agree again → bump `CONSENT_VERSION` in **both** `site/assets/site.js` and
  `site/assets/gate.js`.
- Changed `site.css`, `site.js`, `games.js` or `analytics.js` → raise the cache version `?v=N` in all four pages
  (`site/index.html`, `terms.html`, `privacy.html`, `imprint.html`); for `analytics.js` also in `tools/build.py`.

### D. Analytics / consent
- Code: `site/assets/analytics.js` (GA ID `G-0QMCMFM2YN`). Nothing may load before consent (tested).
- Any change in what is collected (events, parameters, services) → section 3 of `site/privacy.html` in both languages
  and the analytics notes in `README.md`. Purpose changed → raise `VER` in `analytics.js` so everyone is asked again.
- Under-16s: the accept button stays “A parent agrees” / “Ein Elternteil stimmt zu” (tested).

### E. SEO / AI texts
- Edit `tools/seo.py` (wording of the “About” section, `llms.txt`, titles, structured data). Game-specific texts come
  from `site/assets/games.js`.

### F. Domain, name or branding
- Domain: `site/CNAME`, `SITE` in `tools/seo.py`, the address in `site/index.html` (“Play on your phone”), the QR code
  (`python3 tools/qr.py "https://NEW/" site/assets/qr-site.png`), `README.md`, the Pages settings on GitHub, and the
  `SITE` constant in `tests/test_built_site.py`.
- Site name: `site/index.html`, legal pages, `site/assets/site.js`, `analytics.js`, `gate.js`, `tools/build.py`
  (navigation + titles), `tools/seo.py` (`NAME`), `LICENSE.txt`, `README.md`, this file.

## 6. Git and deployment
- Pushing to `main` publishes the site after the tests pass. Use a branch + pull request for bigger changes; CI runs
  the tests on every pull request.
- Commit messages in English. `git pull --rebase` before pushing – the owner sometimes commits on GitHub directly.
- If the deploy fails, the old site stays online; fix the tests or the build and push again.
