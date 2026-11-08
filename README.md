# My Craft Games

Free 3D browser games by Matheus, in German and English. A static website on GitHub Pages: no server, and no outside requests unless a visitor opts in to Google Analytics. This repository holds the sources; GitHub Actions builds, tests and publishes the site.

**Live:** https://mycraftgames.com/

> **Working on this project (people or AI agents)?** Read [AGENTS.md](AGENTS.md) first – it lists which files to update together for every kind of change.

## Project layout

| Folder | What it is |
|---|---|
| `src/` | Game sources (one HTML file per game) |
| `site/` | Hand-written website: start page, legal pages, assets, covers, `CNAME` |
| `tools/` | `build.py` (builds everything into `dist/`), `seo.py` (SEO + AI files), `qr.py` |
| `tests/` | pytest + Playwright tests |
| `.github/workflows/pages.yml` | CI: build → test → deploy to GitHub Pages (deploy only from `main`) |
| `dist/` | Generated site (git-ignored) – exactly what is published |

```
pip install -r requirements-dev.txt && python3 -m playwright install chromium   # once
python3 tools/build.py                    # build the site into dist/
python3 -m pytest -q tests                # run all tests
cd dist && python3 -m http.server 8000    # play at http://localhost:8000
```

## Games

| Game | German | English | FSK |
|---|---|---|---|
| Brainrot-Raub / Brainrot Heist | [de](https://mycraftgames.com/games/brainrot-raub/de/) | [en](https://mycraftgames.com/games/brainrot-raub/en/) | 6 |
| Versteck-Alarm / Hide Alarm | [de](https://mycraftgames.com/games/versteck-alarm/de/) | [en](https://mycraftgames.com/games/versteck-alarm/en/) | 0 |
| Kürbisnacht / Pumpkin Night | [de](https://mycraftgames.com/games/kuerbisnacht/de/) | [en](https://mycraftgames.com/games/kuerbisnacht/en/) | 6 |
| Hühnerchaos / Chicken Chaos | [de](https://mycraftgames.com/games/huehnerchaos/de/) | [en](https://mycraftgames.com/games/huehnerchaos/en/) | 0 |
| Nachtburg / Night Fort | [de](https://mycraftgames.com/games/nachtburg/de/) | [en](https://mycraftgames.com/games/nachtburg/en/) | 6 |
| Sternen-Einhorn / Star Unicorn | [de](https://mycraftgames.com/games/sternen-einhorn/de/) | [en](https://mycraftgames.com/games/sternen-einhorn/en/) | 0 |
| Tsunami-Flucht / Tsunami Escape | [de](https://mycraftgames.com/games/tsunami-flucht/de/) | [en](https://mycraftgames.com/games/tsunami-flucht/en/) | 6 |

**Brainrot-Raub:** buy creatures off a conveyor belt, collect the money they earn, steal from three rival bases and defend yours with a laser shield.

**Versteck-Alarm:** hide-and-seek in a house with garden and garage. Hide with three AI kids from a seeker with a flashlight, or seek four kids yourself using only giggle sounds as hints.

**Kürbisnacht:** Halloween trick-or-treating in a spooky neighbourhood. Choose a costume, ring at lit doors for candy (or a trick), avoid the ghosts, and stay safe in the light of the street lamps until midnight.

**Hühnerchaos:** catch escaped chickens on a farm and stack them on your head. Bigger stacks score more but wobble more, and sharp turns, mud or an angry goose send them flying.

**Nachtburg:** gather wood and stone, build your house first (foundation, walls, roof), walk inside to furnish it (bed needs wool from sheep; table, fireplace, chest with full inventory, rug, and an arcade machine with two mini-games), gather food (berries, apples, eggs) to restore hearts, befriend Bello the dog with a bone and build him a dog house, hunt rabbits and boars for meat, sleep in the bed, add a second floor with a ladder, upgrade weapons with monster loot (slime, crystals), then build walls, torches and arrow towers around your house, then defend it at night against slimes, grumbles and wall-flying bats with a hammer, sword or bow. Bello the dog helps fight once you befriend him, and hens lay eggs that heal you. Monsters find the weakest path with a flow field and break through walls. Local co-op: press P for a second player (arrow keys + Enter). Three computer players (Lena, Tom, Ali) walk on their own with grid pathfinding: by day they gather wood, stone and food, at night they fight monsters (toggle with C). A travelling merchant sometimes visits by day with random trade offers. Campfires (fuelled with sticks or coal) cook meat and eggs into better food; felled trees drop saplings you can plant; big rocks need a pickaxe; a cave in the forest holds stone, coal, gold and crystals (refilled each day), used for gold armour (+2 hearts) and gold weapon level 4. An old castle (bottom right) has a separate hall with ghost and armour guards; once they are defeated the treasure chests open (refilled each day). The house can grow to three floors (second ladder on floor 2); floor 2 has a kitchen where Chef Karl cooks stew and all raw food for 1 wool, floor 3 has beds for the computer players (+1 heart, faster respawn, and they wake up in their own bed after being knocked down). A crystal blaster (magic ranged weapon, 6 crystals + 2 gold) and a backpack (5 gold + 2 wool: more loot per harvest, faster walking) are available. Top right: a broken shop (repair with 10 wood + 6 stone) and a restaurant; both swap 1 gold for 5 coins, the shop sells food and materials, the restaurant serves burger, pizza (all hearts for everyone), ice cream (speed boost) and stew to go. Press G ("Follow me") and the computer players follow you, also into the cave and the castle, where they fight the guards. Days get longer the more nights you survive (up to 3 minutes). The world is 64×48 tiles; the cave and the castle sit in far corners. The castle has three floors (stairs open once a floor's guards are defeated) with a boss knight and five treasure chests in the tower room. A fenced farm next to the house holds hens, ducks, sheep, pigs and cows: about a third of night monsters go for the farm animals, which run away when hurt and return next morning; animals still on the farm at dawn give eggs, milk and carrots. Cows can be milked and pigs dig up carrots. Farmer Ben walks around the farm, gives you a gift once per day and fights monsters that come near the farm with his pitchfork. Computer players sometimes shear sheep or hunt wild animals. Chef Karl gets a bed on floor 2 and cooks a stew every morning.

**Sternen-Einhorn:** a 2D canvas game (no three.js). Fly a unicorn through space with mouse, finger or arrow keys, catch stars and coins and dodge meteors (a hit only knocks two stars away). With enough stars the unicorn flies home and the rainbow grows one band; seven trips complete it. Coins buy dress-up items in the Unicorn Shop (8 tabs: body colours, manes, horns, wings, outfits including tutu and dresses, hats, shoes including roller blades, and stuffed-animal buddies that ride on the unicorn's back), with a try-on preview. Coins and items are saved in `sternen-einhorn-v1`.

**Tsunami-Flucht:** inspired by "Escape Tsunami for Brainrots". Run down a 1400 m beach runway with 13 rarity zones (common to infinity; the last zone only spawns a brainrot now and then), grab brainrots and carry them back to your base, where each one earns money per second (also while away, at half rate for up to 2 hours). Waves of five speeds roll in regularly after a siren; hide in the trenches every 36 m or get washed back to base and lose what you carry. Money buys speed and carrying capacity, with no upper limit. Brainrots in the base can be sold (press E twice next to the pedestal). Hideout holes between the trenches also protect you, and sometimes a second wave follows the first without a siren. The base has a shield: nobody can steal your brainrots. Two computer players (Lena and Tom) collect for their own bases. Saved in `tsunami-flucht-v1`.

## How the site works

- **Age and consent:** on the first visit the start page asks for the player’s age and agreement to the Terms of Use and Privacy Policy (plus a parent’s confirmation under 16). Games rated above the player’s age are locked. Game pages check this with `site/assets/gate.js` and show a notice that links to the age question (no redirect, so search engines can read the pages).
- **FSK ratings:** every game has an FSK level (0/6/12/16/18). They are our own assessment, not an official FSK/USK review, and the site says so.
- **Languages:** the start page and legal pages switch between German and English. Every game exists in both languages (see [CONTRIBUTING.md](CONTRIBUTING.md) – this is the rule for all new games).
- **Privacy:** game data is stored in the browser’s localStorage only. No CDNs or web fonts; three.js r128 is served from `site/assets/vendor/`.
- **Analytics (opt-in only):** `site/assets/analytics.js` shows a consent notice at the bottom of the page (after the age question on the start page). Google Analytics 4 (`G-0QMCMFM2YN`) is loaded **only after “Accept”**; before that nothing goes to Google and no cookies are set. For under-16s the button reads “A parent agrees”. The choice lives in `mcg-analytics` and can be changed via “Cookie settings” in every footer. Events: page views, `play_game` (game page opened, with `game_slug`, `game_language`) and `select_game` (card clicked on the start page). Ads, Google signals and ad personalisation are off.

- **SEO & AI assistants:** `tools/seo.py` adds titles, descriptions, canonical and hreflang links, Open Graph images, JSON-LD (VideoGame, WebSite, ItemList, BreadcrumbList), static game cards on the start page, a visible “About this game” section on every game page, and pre-rendered texts for crawlers without JavaScript. It also writes `sitemap.xml`, `robots.txt` (all crawlers welcome, incl. AI assistants), `llms.txt` / `llms-full.txt` and `404.html` into `dist/`.

### Google Analytics settings to check (in the GA admin)

- **Data retention:** Admin → Data collection and modification → Data retention → set event data to **2 months** (the privacy policy promises at most 14).
- **Google signals:** Admin → Data collection → keep **off**.
- **Data sharing:** Admin → Account settings → turn off sharing with Google products and services, benchmarking and technical support.
- **Custom dimensions (optional, for nicer reports):** Admin → Custom definitions → create event-scoped dimensions `game_slug` and `game_language`. Then *Reports → Engagement → Events → play_game* shows which games are played.

## GitHub Pages (deployed by GitHub Actions)

1. Repository **Settings → Pages → Build and deployment → Source: GitHub Actions**.
2. Custom domain: `mycraftgames.com` (set in the same Pages settings; `site/CNAME` keeps it in the build).
3. Every push to `main` runs `.github/workflows/pages.yml`: build → tests → deploy. If the tests fail, nothing is
   published and the previous version stays online. Pull requests are built and tested but not published.

GitHub Pages for a **private** repository needs a paid GitHub plan (Pro, Team or Enterprise). On a free plan, make the repository public or keep it private and host elsewhere.

## Before going public

Fill in the placeholders marked `[ … ]` in `site/imprint.html` and `site/privacy.html` (name, address, email). The legal texts are a starting point, not legal advice.

## Run locally

Build first (`python3 tools/build.py`), then serve `dist/` with any static file server:

```
cd dist && python3 -m http.server 8000
```

then open http://localhost:8000/.

## Licences

© 2026 My Craft Games. All rights reserved: the games, artwork and code may be played and linked to, but not copied, changed or republished without permission (see `LICENSE.txt`). three.js © three.js authors, MIT licence (`site/assets/vendor/three.LICENSE.txt`).
