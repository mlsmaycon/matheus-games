# CLAUDE.md

All project instructions are in [AGENTS.md](AGENTS.md). Read it fully before making changes – it lists which files
must be updated together for every kind of change (games, start page, legal texts, analytics, SEO, domain).

Short version:
- Edit sources (`src/`, `assets/`, hand-written pages), never the generated files in `games/*/{de,en}/`, `sitemap.xml`,
  `llms*.txt`, `robots.txt`, `404.html` or inside `<!--seo:…-->` markers.
- Rebuild with `python3 tools/build_games.py` (runs `tools/seo.py` too) and test both languages before committing.
- Every game and every text in German **and** English; every game has an FSK rating; no outside requests except the
  opt-in Google Analytics; keep `privacy.html` (both languages) true.
- Reply to Matheus in German, kid-friendly.
