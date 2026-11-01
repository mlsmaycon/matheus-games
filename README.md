# Matheus World

Free 3D browser games by Matheus, in German and English. A static website that runs on GitHub Pages: no build step, no server, no outside requests.

**Live (once GitHub Pages is on):** https://mlsmaycon.github.io/matheus-games/

## Games

| Game | German | English | FSK |
|---|---|---|---|
| Brainrot-Raub / Brainrot Heist | [`games/brainrot-raub/de`](games/brainrot-raub/de/index.html) | [`games/brainrot-raub/en`](games/brainrot-raub/en/index.html) | 6 |
| Versteck-Alarm / Hide Alarm | [`games/versteck-alarm/de`](games/versteck-alarm/de/index.html) | [`games/versteck-alarm/en`](games/versteck-alarm/en/index.html) | 0 |
| Kürbisnacht / Pumpkin Night | [`games/kuerbisnacht/de`](games/kuerbisnacht/de/index.html) | [`games/kuerbisnacht/en`](games/kuerbisnacht/en/index.html) | 6 |
| Hühnerchaos / Chicken Chaos | [`games/huehnerchaos/de`](games/huehnerchaos/de/index.html) | [`games/huehnerchaos/en`](games/huehnerchaos/en/index.html) | 0 |
| Nachtburg / Night Fort | [`games/nachtburg/de`](games/nachtburg/de/index.html) | [`games/nachtburg/en`](games/nachtburg/en/index.html) | 6 |

**Brainrot-Raub:** buy creatures off a conveyor belt, collect the money they earn, steal from three rival bases and defend yours with a laser shield.

**Versteck-Alarm:** hide-and-seek in a house with garden and garage. Hide with three AI kids from a seeker with a flashlight, or seek four kids yourself using only giggle sounds as hints.

**Kürbisnacht:** Halloween trick-or-treating in a spooky neighbourhood. Choose a costume, ring at lit doors for candy (or a trick), avoid the ghosts, and stay safe in the light of the street lamps until midnight.

**Hühnerchaos:** catch escaped chickens on a farm and stack them on your head. Bigger stacks score more but wobble more, and sharp turns, mud or an angry goose send them flying.

**Nachtburg:** gather wood and stone, build your house first (foundation, walls, roof), walk inside to furnish it (bed needs wool from sheep; table, fireplace, chest with full inventory, rug, and an arcade machine with two mini-games), gather food (berries, apples, eggs) to restore hearts, befriend Bello the dog with a bone and build him a dog house, hunt rabbits and boars for meat, sleep in the bed, add a second floor with a ladder, upgrade weapons with monster loot (slime, crystals), then build walls, torches and arrow towers around your house, then defend it at night against slimes, grumbles and wall-flying bats with a hammer, sword or bow. Bello the dog helps fight once you befriend him, and hens lay eggs that heal you. Monsters find the weakest path with a flow field and break through walls. Local co-op: press P for a second player (arrow keys + Enter). Three computer players (Lena, Tom, Ali) walk on their own with grid pathfinding: by day they gather wood, stone and food, at night they fight monsters (toggle with C). A travelling merchant sometimes visits by day with random trade offers. Campfires (fuelled with sticks or coal) cook meat and eggs into better food; felled trees drop saplings you can plant; big rocks need a pickaxe; a cave in the forest holds stone, coal, gold and crystals (refilled each day), used for gold armour (+2 hearts) and gold weapon level 4. An old castle (bottom right) has a separate hall with ghost and armour guards; once they are defeated the treasure chests open (refilled each day).

## How the site works

- **Age and consent:** on the first visit the start page asks for the player’s age and agreement to the Terms of Use and Privacy Policy (plus a parent’s confirmation under 16). Games rated above the player’s age are locked. Game pages check this with `assets/gate.js` and send visitors back to the start page if needed.
- **FSK ratings:** every game has an FSK level (0/6/12/16/18). They are our own assessment, not an official FSK/USK review, and the site says so.
- **Languages:** the start page and legal pages switch between German and English. Every game exists in both languages (see [CONTRIBUTING.md](CONTRIBUTING.md) – this is the rule for all new games).
- **Privacy:** everything is stored in the browser’s localStorage only. No cookies, no tracking, no CDNs or web fonts; three.js r128 is served from `assets/vendor/`.

## Turn on GitHub Pages

1. Repository **Settings → Pages**.
2. Source: **Deploy from a branch**, branch `main`, folder `/ (root)`.
3. The site appears at `https://mlsmaycon.github.io/matheus-games/` after a minute or two.

GitHub Pages for a **private** repository needs a paid GitHub plan (Pro, Team or Enterprise). On a free plan, make the repository public or keep it private and host elsewhere.

## Before going public

Fill in the placeholders marked `[ … ]` in `imprint.html` and `privacy.html` (name, address, email). The legal texts are a starting point, not legal advice.

## Run locally

Any static file server works, for example:

```
python3 -m http.server 8000
```

then open http://localhost:8000/.

## Licences

Games and artwork © Matheus. three.js © three.js authors, MIT licence (`assets/vendor/three.LICENSE.txt`).
