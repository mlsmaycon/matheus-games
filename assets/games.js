/*
  Matheus World – game registry.
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
      de: 'Hack Holz, bau Stein ab und bau zuerst dein Haus: Fundament, Wände, Dach. Drinnen baust du Bett (braucht Wolle vom Schaf), Tisch, Kamin, Truhe und einen Spielautomaten. Bau eine zweite Etage, jag Hasen und Wildschweine, verbessere Hammer, Schwert und Bogen mit Monster-Beute und schlaf im Bett. Gib Hund Bello einen Knochen. Brat Fleisch und Eier am Lagerfeuer, pflanz Setzlinge, bau eine Spitzhacke und hol Kohle und Gold aus der Höhle für eine Goldrüstung. Manchmal kommt ein Wanderhändler zum Tauschen, und die Computer-Spieler Lena, Tom und Ali sammeln mit dir und kämpfen nachts mit. Zu zweit spielbar an einer Tastatur. Bau dir Schwert oder Bogen, freunde dich mit Hund Bello an und sammel Eier. Wenn es dunkel wird, kommen Schleime, Grummel und Fledermäuse.',
      en: 'Chop wood, mine stone and build your house first: foundation, walls, roof. Inside you build a bed (needs wool from the sheep), table, fireplace, chest and an arcade machine. Add a second floor, hunt rabbits and boars, upgrade your hammer, sword and bow with monster loot and sleep in your bed. Give Bello the dog a bone. Cook meat and eggs at the campfire, plant saplings, craft a pickaxe and dig coal and gold in the cave for gold armour. Sometimes a travelling merchant comes by to trade, and the computer players Lena, Tom and Ali gather with you and fight at night. Two players can play on one keyboard. Craft a sword or bow, make friends with Bello the dog and collect eggs. When it gets dark, slimes, grumbles and bats arrive.'
    },
    tags: { de: ['3D', 'Bauen', 'Tiere', '2 Spieler', 'Computer-Spieler'], en: ['3D', 'Building', 'Animals', '2 players', 'Computer players'] },
    fskReason: {
      de: 'Comic-Monster und Wildtiere werden mit Hammer, Schwert oder Bogen besiegt und verschwinden in einer Rauchwolke. Kein Blut. Die eigenen Haustiere kann man nicht angreifen.',
      en: 'Cartoon monsters and wild animals are defeated with a hammer, sword or bow and vanish in a puff of smoke. No blood. Your own pets can’t be attacked.'
    }
  }
];
