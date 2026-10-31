# Matheus Games

Browser games built with plain HTML, CSS and JavaScript. No build step: open a game's `index.html` in a browser and play.

## Games

### Brainrot-Raub (`brainrot-raub/`)

A 3D game in the style of "Steal a Brainrot". Buy creatures off the conveyor belt, collect the money they earn, steal the best ones from three rival bases, and protect your own base with a laser shield.

- **Tech:** one HTML file, plain JavaScript, [three.js r128](https://threejs.org/) from a CDN for 3D rendering
- **Controls:** WASD / arrow keys or drag on the playfield to move, E to buy or steal, Q to sell, mouse wheel to zoom
- **Saving:** progress is stored in the browser's localStorage
- `qr-code.png` links to the hosted version on claude.ai (only works for people the game has been shared with)

Language of the game: German.

### Versteck-Alarm (`versteck-alarm/`)

A 3D hide-and-seek game in a house with a bedroom, bathroom, living room, kitchen, garden and garage, with 22 hiding spots.

- **Hide mode:** you and three AI kids hide while the seeker counts to 12. Survive 100 seconds. The seeker's flashlight cone shows where he is looking, running makes noise, and kids who panic may bolt from their spot.
- **Seek mode:** find four hidden kids in 120 seconds. Two of them are runners who jump out and flee. Hints are sound only: the giggle button (or H) makes the nearest kid giggle, panned left/right by direction and louder when closer. Hidden kids also rustle or giggle on their own.
- **Tech:** one HTML file, plain JavaScript, three.js r128 from a CDN, Web Audio for sounds
- **Controls:** WASD / arrow keys or drag on the playfield, E to hide or search, Shift to sneak, H to hear a giggle, M to toggle sound, mouse wheel to zoom
- **Saving:** records are stored in the browser's localStorage

Language of the game: German.
