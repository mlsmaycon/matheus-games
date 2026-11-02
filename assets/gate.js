/*
  My Craft Games – age & consent gate for game pages.
  Include in <head> BEFORE anything else:
    <script src="../../../assets/gate.js" data-fsk="6" data-game="my-game"></script>
  If the visitor has not confirmed their age and accepted the Terms and Privacy Policy,
  or is younger than the game's FSK rating, the game is covered by a notice that links to
  the start page (where the age is asked). The page itself stays readable for search engines.
  Everything is stored only in this browser (localStorage); this file sends nothing anywhere.
*/
(function () {
  var CONSENT_VERSION = 1;
  var s = document.currentScript;
  var fsk = parseInt((s && s.getAttribute('data-fsk')) || '0', 10);
  var game = (s && s.getAttribute('data-game')) || '';
  var lang = (document.documentElement.lang || 'de').slice(0, 2) === 'en' ? 'en' : 'de';
  var store = null;
  try { store = window.localStorage; store.setItem('mw-lang', lang); } catch (e) { store = null; }
  if (!store) return; // storage blocked: the start page asks every time instead

  var c = null;
  try { c = store ? JSON.parse(store.getItem('mw-consent') || 'null') : null; } catch (e) { c = null; }
  var age = -1;
  if (c && c.v === CONSENT_VERSION && typeof c.age === 'number' && typeof c.at === 'number') {
    age = c.age + Math.floor((Date.now() - c.at) / (365.25 * 24 * 3600 * 1000));
  }
  if (age >= fsk) return;

  var root = s.src.replace(/assets\/gate\.js(\?.*)?$/, '');
  var why = age < 0 ? 'consent' : 'age';
  var T = {
    de: {
      consentT: 'Kurz bevor du spielst', consent: 'Bitte gib auf der Startseite dein Alter an und stimme den Nutzungsbedingungen zu. Danach geht es direkt hierher zurück.',
      consentB: 'Alter angeben & spielen',
      ageT: 'Dieses Spiel ist ab {n} Jahren', age: 'Schau dir auf der Startseite die anderen Spiele an, die zu deinem Alter passen.',
      ageB: 'Zu den Spielen'
    },
    en: {
      consentT: 'Just before you play', consent: 'Please enter your age on the start page and accept the Terms of Use. You will come straight back here afterwards.',
      consentB: 'Enter age & play',
      ageT: 'This game is for ages {n}+', age: 'Have a look at the other games on the start page that suit your age.',
      ageB: 'Go to the games'
    }
  }[lang];
  var href = root + 'index.html?next=' + encodeURIComponent(game) + '&why=' + why + '&lang=' + lang;
  var box = null;

  // While the notice is shown, keys must not reach the game underneath.
  window.addEventListener('keydown', function (e) {
    if (box && !box.contains(e.target)) { e.stopImmediatePropagation(); if (e.key !== 'Tab') e.preventDefault(); }
  }, true);

  function show() {
    var st = document.createElement('style');
    st.textContent = '.mw-gate{position:fixed;inset:0;z-index:1000;display:flex;align-items:center;justify-content:center;padding:16px;background:#0b0e22e6;font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}' +
      '.mw-gate div{max-width:440px;background:#171a33;color:#f6f4ee;border:2px solid #ffffff2e;border-radius:18px;padding:22px 22px 20px;text-align:center;box-shadow:0 12px 50px #000a}' +
      '.mw-gate h2{margin:0 0 8px;font-size:22px}.mw-gate p{margin:0 0 16px;opacity:.9}' +
      '.mw-gate a{display:inline-block;background:#ff9f2e;color:#171a33;font-weight:800;text-decoration:none;border-radius:12px;padding:11px 20px}' +
      '.mw-gate a:focus-visible{outline:3px solid #fff;outline-offset:3px}';
    document.head.appendChild(st);
    box = document.createElement('div');
    box.className = 'mw-gate'; box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true');
    var inner = document.createElement('div'), h = document.createElement('h2'), p = document.createElement('p'), a = document.createElement('a');
    h.id = 'mw-gate-title'; box.setAttribute('aria-labelledby', h.id);
    h.textContent = (why === 'age' ? T.ageT : T.consentT).replace('{n}', fsk);
    p.textContent = why === 'age' ? T.age : T.consent;
    a.href = href; a.textContent = why === 'age' ? T.ageB : T.consentB;
    inner.appendChild(h); inner.appendChild(p); inner.appendChild(a); box.appendChild(inner);
    document.body.appendChild(box);
    try { a.focus(); } catch (e) {}
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', show); else show();
})();
