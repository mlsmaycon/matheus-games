/*
  My Craft Games – game registry.
  Every game MUST have:
    - games/<slug>/de/index.html and games/<slug>/en/index.html
    - an FSK age rating (0, 6, 12, 16 or 18) with a short reason in both languages
    - a cover image at games/<slug>/cover.svg (or .png/.webp)
  See CONTRIBUTING.md for the full checklist.
*/
window.MW_GAMES = [
  {
    slug: 'brainrot-raub',
    fsk: 6,
    added: '2026-10-31',
    cover: 'games/brainrot-raub/cover.svg',
    title: { de: 'Brainrot-Raub', en: 'Brainrot Heist' },
    tagline: { de: 'Kaufen, kassieren, klauen.', en: 'Buy, cash in, steal.' },
    desc: {
      de: 'Kauf verrückte Figuren vom Fließband, lass sie Geld verdienen und schnapp dir die besten aus den Basen deiner Rivalen. Aber pass auf: Die klauen zurück.',
      en: 'Buy wacky creatures off the conveyor belt, let them earn money and grab the best ones from your rivals’ bases. But watch out: they steal back.'
    },
    tags: { de: ['3D', 'Sammeln', 'Handy & PC'], en: ['3D', 'Collecting', 'Phone & PC'] },
    fskReason: {
      de: 'Comic-Figuren klauen sich gegenseitig Sachen. Keine Gewalt, kein Blut.',
      en: 'Cartoon characters steal things from each other. No violence, no blood.'
    }
  },
  {
    slug: 'versteck-alarm',
    fsk: 0,
    added: '2026-10-31',
    cover: 'games/versteck-alarm/cover.svg',
    title: { de: 'Versteck-Alarm', en: 'Hide Alarm' },
    tagline: { de: 'Verstecken oder suchen – im ganzen Haus.', en: 'Hide or seek – all over the house.' },
    desc: {
      de: 'Versteck dich mit drei Kindern vor dem Sucher mit Taschenlampe oder such sie selbst. 22 Verstecke in Haus, Garten und Garage.',
      en: 'Hide from the seeker and his flashlight together with three kids, or be the seeker yourself. 22 hiding spots across house, garden and garage.'
    },
    tags: { de: ['3D', 'Verstecken', 'Ton an'], en: ['3D', 'Hide & seek', 'Sound on'] },
    fskReason: {
      de: 'Ein klassisches Versteckspiel mit etwas Spannung beim Gesucht-Werden.',
      en: 'A classic hide-and-seek game with a little tension while being searched for.'
    }
  },
  {
    slug: 'kuerbisnacht',
    fsk: 6,
    added: '2026-10-31',
    cover: 'games/kuerbisnacht/cover.svg',
    title: { de: 'Kürbisnacht', en: 'Pumpkin Night' },
    tagline: { de: 'Süßes oder Saures – bis Mitternacht!', en: 'Trick or treat – until midnight!' },
    desc: {
      de: 'Zieh im Kostüm durch die Nachbarschaft, klingel an beleuchteten Türen und sammle Süßigkeiten, bevor es Mitternacht schlägt. Geister geistern durch die Straßen, nur unter den Laternen bist du sicher.',
      en: 'Roam the neighbourhood in costume, ring at lit doors and collect candy before the clock strikes midnight. Ghosts haunt the streets, and you are only safe under the street lamps.'
    },
    tags: { de: ['3D', 'Halloween', 'Ton an'], en: ['3D', 'Halloween', 'Sound on'] },
    fskReason: {
      de: 'Freundliche Geister und kleine Schreckmomente (Spinne, Glibber). Nichts Gruseliges im Detail.',
      en: 'Friendly ghosts and small scares (a spider, slime). Nothing frightening in detail.'
    }
  },
  {
    slug: 'huehnerchaos',
    fsk: 0,
    added: '2026-11-01',
    cover: 'games/huehnerchaos/cover.svg',
    title: { de: 'Hühnerchaos', en: 'Chicken Chaos' },
    tagline: { de: 'Fang die Hühner – aber pass auf den Stapel auf!', en: 'Catch the chickens – but mind the stack!' },
    desc: {
      de: 'Die Hühner sind ausgebüxt! Fang sie ein, stapel sie auf deinem Kopf und bring sie in den Stall. Je höher der Turm, desto mehr Punkte – aber in scharfen Kurven fliegen sie gackernd davon. Und die Gans ist sauer.',
      en: 'The chickens have escaped! Catch them, stack them on your head and bring them back to the coop. The higher the tower, the more points – but sharp turns send them flying. And the goose is angry.'
    },
    tags: { de: ['3D', 'Lustig', 'Ton an'], en: ['3D', 'Funny', 'Sound on'] },
    fskReason: {
      de: 'Lustiger Bauernhof-Spaß ohne Gewalt. Die Gans schubst dich nur um.',
      en: 'Funny farmyard fun without violence. The goose only knocks you over.'
    }
  },
  {
    slug: 'nachtburg',
    fsk: 6,
    added: '2026-11-01',
    cover: 'games/nachtburg/cover.svg',
    title: { de: 'Nachtburg', en: 'Night Fort' },
    tagline: { de: 'Bau tagsüber, verteidige nachts.', en: 'Build by day, defend by night.' },
    desc: {
      de: 'Sammle Holz und Stein, bau dein Haus bis zu drei Etagen hoch und richte es ein. Beschütz nachts Haus und Farm vor Monstern, zusammen mit Hund Bello, Bauer Ben und den Computer-Spielern Lena, Tom und Ali. Entdecke die Höhle mit Gold und die große Burg mit dem Schatz im Turm. Zu zweit an einer Tastatur spielbar.',
      en: 'Gather wood and stone, build your house up to three floors and furnish it. At night, protect your house and farm from monsters together with Bello the dog, Farmer Ben and the computer players Lena, Tom and Ali. Explore the cave full of gold and the big castle with treasure at the top of the tower. Two players can share one keyboard.'
    },
    tags: { de: ['3D', 'Bauen', 'Farm', '2 Spieler', 'Computer-Spieler'], en: ['3D', 'Building', 'Farm', '2 players', 'Computer players'] },
    fskReason: {
      de: 'Comic-Monster und Wildtiere werden mit Hammer, Schwert oder Bogen besiegt und verschwinden in einer Rauchwolke. Kein Blut. Die eigenen Haus- und Farmtiere kann man nicht angreifen.',
      en: 'Cartoon monsters and wild animals are defeated with a hammer, sword or bow and vanish in a puff of smoke. No blood. Your own pets and farm animals can’t be attacked.'
    }
  },
  {
    slug: 'sternen-einhorn',
    fsk: 0,
    added: '2026-11-06',
    cover: 'games/sternen-einhorn/cover.svg',
    title: { de: 'Sternen-Einhorn', en: 'Star Unicorn' },
    tagline: { de: 'Sterne fangen, Regenbogen wachsen lassen!', en: 'Catch the stars, grow the rainbow!' },
    desc: {
      de: 'Flieg mit deinem Einhorn durchs Weltall, fang Sterne und Münzen und weich den Meteoren aus. Mit genug Sternen fliegt es nach Hause und der Regenbogen bekommt eine neue Farbe – nach sieben Flügen ist er fertig. Im Einhorn-Laden kaufst du Farben, Mähnen, Hörner, Flügel, Kleider, Hüte, Schuhe, Inlineskates und Kuscheltiere, die mitfliegen.',
      en: 'Fly your unicorn through space, catch stars and coins and dodge the meteors. With enough stars it flies home and the rainbow gets a new colour – after seven trips it is complete. In the Unicorn Shop you buy colours, manes, horns, wings, dresses, hats, shoes, roller blades and cuddly buddies that ride along.'
    },
    tags: { de: ['2D', 'Einhorn', 'Anziehen', 'Ton an'], en: ['2D', 'Unicorn', 'Dress-up', 'Sound on'] },
    fskReason: {
      de: 'Fröhliches Sammelspiel ohne Gewalt. Meteore stoßen nur ein paar Sterne weg.',
      en: 'Cheerful collecting game without violence. Meteors only knock a few stars away.'
    }
  },
  {
    slug: 'tsunami-flucht',
    fsk: 6,
    added: '2026-11-07',
    cover: 'games/tsunami-flucht/cover.svg',
    title: { de: 'Tsunami-Flucht', en: 'Tsunami Escape' },
    tagline: { de: 'Schnapp dir Brainrots – bevor die Welle kommt!', en: 'Grab the brainrots – before the wave hits!' },
    desc: {
      de: 'Lauf eine lange Strandbahn entlang, schnapp dir Brainrots und bring sie in deine Basis, wo sie jede Sekunde Geld verdienen. Je weiter weg, desto seltener: 138 Zonen von gewöhnlich bis ultimativ. Immer wieder rollt eine riesige Welle heran – versteck dich in einem Graben oder renn zurück. Deine Basis hat einen Schutzschild, niemand kann dir etwas stehlen. Mit dem Geld kaufst du mehr Tempo und mehr Tragen.',
      en: 'Run along a long beach runway, grab brainrots and bring them to your base, where they earn money every second. The farther out, the rarer they are: 138 zones from common to ultimate. Again and again a giant wave rolls in – hide in a trench or run back. Your base has a shield, so nobody can steal from you. Spend your money on more speed and more carrying.'
    },
    tags: { de: ['3D', 'Brainrot', 'Sammeln', 'Ton an'], en: ['3D', 'Brainrot', 'Collecting', 'Sound on'] },
    fskReason: {
      de: 'Spannende Wellen mit Warnsirene, aber keine Gewalt. Wer von der Welle erwischt wird, landet nur wieder in seiner Basis.',
      en: 'Exciting waves with a warning siren, but no violence. Anyone caught by a wave just ends up back at their base.'
    }
  },
  {
    slug: 'bauernhof',
    fsk: 0,
    added: '2026-11-08',
    cover: 'games/bauernhof/cover.svg',
    title: { de: 'Mein Bauernhof', en: 'My Farm' },
    tagline: { de: 'Kauf Tiere, füttere sie und verkaufe, was sie machen!', en: 'Buy animals, feed them and sell what they make!' },
    desc: {
      de: 'Du hast einen eigenen Bauernhof, aber noch keine Tiere. Kauf beim Tierhändler Hühner, Enten, Schafe, Kaninchen, Schweine, Ziegen, Bienen, Kühe, Alpakas, Pferde, Pfauen und sogar ein Einhorn – bis zu 10 in jedem Stall. Füll ihre Tröge mit Futter und Wasser, sammle Eier, Wolle, Trüffel, Käse und Milch ein und verkaufe sie im Hofladen. Mit den Münzen baust du neue Gehege, säst Weizen und verbesserst deinen Hof: besserer Hofladen, größeres Feld, größeres Haus mit Morgen-Bonus und eine Wasserleitung. Besucher kommen auf deinen Hof, schauen sich die Tiere an und bezahlen dafür. Zwei satte Tiere bekommen Babys, wenn im Stall noch Platz ist.',
      en: 'You have your own farm, but no animals yet. Buy chickens, ducks, sheep, rabbits, pigs, goats, bees, cows, alpacas, horses, peacocks and even a unicorn – up to 10 in each pen – from the animal trader. Fill their troughs with food and water, collect eggs, wool, truffles, cheese and milk and sell them at the farm shop. Use your coins to build new pens, sow wheat and improve your farm: a better farm shop, a bigger field, a bigger house with a morning bonus and a water pipe. Visitors come to your farm, look at the animals and pay for it. Two well-fed animals have babies when there is room in the pen.'
    },
    tags: { de: ['3D', 'Tiere', 'Bauernhof', 'Ton an'], en: ['3D', 'Animals', 'Farm', 'Sound on'] },
    fskReason: {
      de: 'Friedliches Bauernhof-Spiel ohne Gewalt und ohne Zeitdruck.',
      en: 'Peaceful farm game with no violence and no time pressure.'
    }
  }
];
