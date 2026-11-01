/*
  My Craft Games – age & consent gate for game pages.
  Include in <head> BEFORE anything else:
    <script src="../../../assets/gate.js" data-fsk="6" data-game="my-game"></script>
  If the visitor has not confirmed their age and accepted the Terms and Privacy Policy,
  or is younger than the game's FSK rating, they are sent back to the start page.
  Everything is stored only in this browser (localStorage); nothing is sent anywhere.
*/
(function () {
  var CONSENT_VERSION = 1;
  var s = document.currentScript;
  var fsk = parseInt((s && s.getAttribute('data-fsk')) || '0', 10);
  var game = (s && s.getAttribute('data-game')) || '';
  var lang = (document.documentElement.lang || 'de').slice(0, 2) === 'en' ? 'en' : 'de';
  var store = null;
  try { store = window.localStorage; store.setItem('mw-lang', lang); } catch (e) { store = null; }
  if (!store) return; // storage blocked: cannot remember consent, so the start page asks every time

  var c = null;
  try { c = JSON.parse(store.getItem('mw-consent') || 'null'); } catch (e) { c = null; }
  var age = -1;
  if (c && c.v === CONSENT_VERSION && typeof c.age === 'number' && typeof c.at === 'number') {
    age = c.age + Math.floor((Date.now() - c.at) / (365.25 * 24 * 3600 * 1000));
  }
  if (age >= fsk) return;

  var root = s.src.replace(/assets\/gate\.js(\?.*)?$/, '');
  var why = age < 0 ? 'consent' : 'age';
  location.replace(root + 'index.html?next=' + encodeURIComponent(game) + '&why=' + why + '&lang=' + lang);
})();
