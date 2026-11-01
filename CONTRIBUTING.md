# Adding a game to My Craft Games

Every game on My Craft Games follows the same rules. A game is not done until every box below is ticked.

## Checklist

- [ ] **Two languages.** The game exists as `games/<slug>/de/index.html` (German) and `games/<slug>/en/index.html` (English). Both versions have the same gameplay; only the text differs. `<html lang="de">` / `<html lang="en">` is set correctly.
- [ ] **FSK rating.** Pick one of `0`, `6`, `12`, `16`, `18` using the [FSK criteria](https://www.fsk.de/?seitid=70&tid=70) and write a one-sentence reason in both languages. Ratings are our own assessment; the site says so.
- [ ] **Age gate.** The first thing in `<head>` is
  ```html
  <script src="../../../assets/gate.js" data-fsk="6" data-game="<slug>"></script>
  ```
  with the same FSK number as in the registry.
- [ ] **Navigation bar.** Right after `<body>`, a `<nav class="mw-nav">` with a link back to `../../../index.html`, the FSK badge and a link to the other language (`../en/index.html` or `../de/index.html`). Copy it from an existing game.
- [ ] **No outside requests.** No CDN scripts, no Google Fonts, no analytics. Libraries go in `assets/vendor/` (three.js r128 is already there: `../../../assets/vendor/three.r128.min.js`). Use system font stacks.
- [ ] **Cover image.** `games/<slug>/cover.svg` (or `.png`/`.webp`), 16:10, no text needed.
- [ ] **Registry entry.** Add the game to `assets/games.js` with `slug`, `fsk`, `cover`, and `title`, `tagline`, `desc`, `tags`, `fskReason` in `de` and `en`.
- [ ] **Privacy.** If the game stores anything in `localStorage`, add the key to the table in `privacy.html` (both languages) and to `KEYS` in `assets/site.js` so “Delete my data” clears it.
- [ ] **Works on phone and PC.** Touch controls, no horizontal scrolling at 400 px width.

## Folder layout

```
index.html              start page (game list, age & consent gate, DE/EN)
terms.html              Terms of Use (DE + EN)
privacy.html            Privacy Policy (DE + EN)
imprint.html            Legal notice / Impressum (DE + EN)
assets/
  site.css, site.js     start page and legal pages
  games.js              game registry
  gate.js               age & consent guard for game pages
  vendor/               third-party libraries served locally
games/<slug>/
  de/index.html
  en/index.html
  cover.svg
```

## When the Terms or Privacy Policy change

Bump `CONSENT_VERSION` in both `assets/site.js` and `assets/gate.js`. Everyone is then asked to agree again on their next visit.
