/* Matheus World – start page and legal pages logic (language, age & consent gate, game list).
   No network requests: everything lives in this browser's localStorage. */
(function () {
  var CONSENT_VERSION = 1;
  var PARENT_AGE = 16; // below this, a parent must confirm
  var KEYS = ['mw-consent', 'mw-lang', 'brainrot-raub-v1', 'brainrot-raub-v2', 'versteck-alarm-v1'];
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var store = null;
  try { store = window.localStorage; store.getItem('x'); } catch (e) { store = null; }
  var get = function (k) { try { return store ? store.getItem(k) : null; } catch (e) { return null; } };
  var set = function (k, v) { try { if (store) store.setItem(k, v); } catch (e) {} };
  var del = function (k) { try { if (store) store.removeItem(k); } catch (e) {} };
  var memConsent = null; // fallback when storage is blocked

  var T = {
    de: {
      'nav.age': 'Alter: {n} · ändern',
      'nav.noage': 'Alter angeben',
      'hero.title': 'Willkommen in <em>Matheus World</em>',
      'hero.text': 'Kostenlose 3D-Spiele direkt im Browser. Auf Deutsch und Englisch, für Handy und PC.',
      'fact.1': 'Keine Anmeldung', 'fact.2': 'Keine Werbung', 'fact.3': 'Kein Download', 'fact.4': 'Kein Tracking',
      'games.title': 'Spiele', 'games.sub': 'Jedes Spiel hat eine Altersempfehlung nach FSK-Stufen.',
      'play': 'Spielen', 'play.locked': 'Ab {n} Jahren', 'play.gate': 'Alter angeben & spielen',
      'other.lang': 'In English', 'locked': 'Ab {n} Jahren',
      'fsk.title': 'Was bedeutet FSK?',
      'fsk.sub': 'Die Farben zeigen, ab welchem Alter ein Spiel geeignet ist.',
      'fsk.0': 'Ohne Altersbeschränkung', 'fsk.6': 'Ab 6 Jahren', 'fsk.12': 'Ab 12 Jahren', 'fsk.16': 'Ab 16 Jahren', 'fsk.18': 'Ab 18 Jahren',
      'fsk.note': 'Die Einstufungen sind eine eigene Einschätzung nach den Kriterien der FSK. Sie wurden nicht offiziell von der FSK oder der USK geprüft.',
      'phone.title': 'Auf dem Handy spielen', 'phone.text': 'Scan den Code oder öffne diese Adresse:',
      'f.terms': 'Nutzungsbedingungen', 'f.privacy': 'Datenschutz', 'f.imprint': 'Impressum',
      'f.reset': 'Meine Daten in diesem Browser löschen', 'f.reset2': 'Wirklich alles löschen? Nochmal klicken',
      'f.done': 'Gelöscht.',
      'g.title': 'Hallo! Wie alt bist du?',
      'g.text': 'Damit wir dir nur Spiele zeigen, die zu deinem Alter passen. Dein Alter bleibt nur in diesem Browser gespeichert.',
      'g.age': 'Dein Alter', 'g.years': 'Jahre',
      'g.tos': 'Ich habe die <a href="terms.html" target="_blank" rel="noopener">Nutzungsbedingungen</a> gelesen und bin einverstanden.',
      'g.privacy': 'Ich habe die <a href="privacy.html" target="_blank" rel="noopener">Datenschutzerklärung</a> gelesen.',
      'g.parent': 'Ein Elternteil hat die Regeln mit mir gelesen und ist einverstanden.',
      'g.go': 'Los geht’s',
      'e.age': 'Bitte gib dein Alter als Zahl zwischen 3 und 120 ein.',
      'e.tos': 'Bitte stimme den Nutzungsbedingungen zu.',
      'e.privacy': 'Bitte bestätige, dass du die Datenschutzerklärung gelesen hast.',
      'e.parent': 'Unter 16 muss ein Elternteil zustimmen.',
      'n.age': '„{g}“ ist ab {n} Jahren. Schau dir die anderen Spiele an!',
      'n.consent': 'Bevor es losgeht: Bitte gib dein Alter an.',
      'n.nostore': 'Dein Browser blockiert den Speicher. Wir fragen deshalb bei jedem Besuch neu.'
    },
    en: {
      'nav.age': 'Age: {n} · change',
      'nav.noage': 'Enter age',
      'hero.title': 'Welcome to <em>Matheus World</em>',
      'hero.text': 'Free 3D games right in your browser. In German and English, for phone and PC.',
      'fact.1': 'No sign-up', 'fact.2': 'No ads', 'fact.3': 'No download', 'fact.4': 'No tracking',
      'games.title': 'Games', 'games.sub': 'Every game has an age rating based on the German FSK levels.',
      'play': 'Play', 'play.locked': 'Ages {n}+', 'play.gate': 'Enter age & play',
      'other.lang': 'Auf Deutsch', 'locked': 'Ages {n}+',
      'fsk.title': 'What does FSK mean?',
      'fsk.sub': 'FSK is the German age rating system. The colours show which age a game suits.',
      'fsk.0': 'All ages', 'fsk.6': 'Ages 6+', 'fsk.12': 'Ages 12+', 'fsk.16': 'Ages 16+', 'fsk.18': 'Ages 18+',
      'fsk.note': 'These ratings are our own assessment using the FSK criteria. They have not been officially reviewed by the FSK or USK.',
      'phone.title': 'Play on your phone', 'phone.text': 'Scan the code or open this address:',
      'f.terms': 'Terms of Use', 'f.privacy': 'Privacy Policy', 'f.imprint': 'Legal notice',
      'f.reset': 'Delete my data in this browser', 'f.reset2': 'Really delete everything? Click again',
      'f.done': 'Deleted.',
      'g.title': 'Hi! How old are you?',
      'g.text': 'So we only show you games that suit your age. Your age stays stored in this browser only.',
      'g.age': 'Your age', 'g.years': 'years',
      'g.tos': 'I have read and agree to the <a href="terms.html" target="_blank" rel="noopener">Terms of Use</a>.',
      'g.privacy': 'I have read the <a href="privacy.html" target="_blank" rel="noopener">Privacy Policy</a>.',
      'g.parent': 'A parent has read the rules with me and agrees.',
      'g.go': 'Let’s go',
      'e.age': 'Please enter your age as a number between 3 and 120.',
      'e.tos': 'Please agree to the Terms of Use.',
      'e.privacy': 'Please confirm you have read the Privacy Policy.',
      'e.parent': 'Under 16, a parent has to agree.',
      'n.age': '“{g}” is for ages {n}+. Check out the other games!',
      'n.consent': 'Before you start: please enter your age.',
      'n.nostore': 'Your browser blocks storage, so we will ask again on every visit.'
    }
  };

  var params = new URLSearchParams(location.search);
  var lang = params.get('lang') || get('mw-lang') || ((navigator.language || 'de').slice(0, 2) === 'de' ? 'de' : 'en');
  if (lang !== 'de' && lang !== 'en') lang = 'de';
  var t = function (k, v) {
    var s = (T[lang][k] || T.de[k] || k);
    if (v) Object.keys(v).forEach(function (x) { s = s.split('{' + x + '}').join(v[x]); });
    return s;
  };

  function readConsent() {
    var c = memConsent;
    if (!c) { try { c = JSON.parse(get('mw-consent') || 'null'); } catch (e) { c = null; } }
    if (!c || c.v !== CONSENT_VERSION || typeof c.age !== 'number') return null;
    c.now = c.age + Math.floor((Date.now() - c.at) / (365.25 * 24 * 3600 * 1000));
    return c;
  }
  function saveConsent(age, parent) {
    var c = { v: CONSENT_VERSION, age: age, at: Date.now(), parent: !!parent, tos: true, privacy: true };
    memConsent = c;
    set('mw-consent', JSON.stringify(c));
  }

  function applyLang() {
    document.documentElement.lang = lang;
    set('mw-lang', lang);
    document.querySelectorAll('[data-i18n]').forEach(function (el) { el.textContent = t(el.getAttribute('data-i18n')); });
    document.querySelectorAll('[data-i18n-html]').forEach(function (el) { el.innerHTML = t(el.getAttribute('data-i18n-html')); });
    document.querySelectorAll('.lang button').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.lang === lang)); });
    renderAgeChip();
    renderGames();
  }

  function renderAgeChip() {
    var chip = $('#ageChip'); if (!chip) return;
    var c = readConsent();
    chip.textContent = c ? t('nav.age', { n: c.now }) : t('nav.noage');
  }

  function el(tag, attrs, kids) {
    var e = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) {
      if (k === 'text') e.textContent = attrs[k];
      else if (k === 'html') e.innerHTML = attrs[k];
      else e.setAttribute(k, attrs[k]);
    });
    (kids || []).forEach(function (k) { if (k) e.appendChild(k); });
    return e;
  }
  function fskBadge(n) {
    var b = el('span', { class: 'fsk', 'data-fsk': String(n), title: t('fsk.' + n) }, [el('b', { text: String(n) })]);
    b.appendChild(document.createTextNode('FSK'));
    return b;
  }

  function renderGames() {
    var grid = $('#games'); if (!grid || !window.MW_GAMES) return;
    grid.innerHTML = '';
    var c = readConsent();
    window.MW_GAMES.forEach(function (g) {
      var locked = c && c.now < g.fsk;
      var other = lang === 'de' ? 'en' : 'de';
      var href = 'games/' + g.slug + '/' + lang + '/index.html';
      var play;
      if (locked) play = el('a', { class: 'play', 'aria-disabled': 'true', role: 'link', text: t('play.locked', { n: g.fsk }) });
      else if (!c) { play = el('a', { class: 'play', href: href, text: t('play.gate') }); play.addEventListener('click', function (e) { e.preventDefault(); openGate(null, g.slug); }); }
      else play = el('a', { class: 'play', href: href, text: t('play') });
      var cover = el('div', { class: 'cover' }, [
        el('img', { src: g.cover, alt: '', loading: 'lazy', width: '640', height: '400' }),
        fskBadge(g.fsk),
        locked ? el('div', { class: 'lockmsg', text: t('locked', { n: g.fsk }) }) : null
      ]);
      var card = el('article', { class: 'card' + (locked ? ' locked' : '') }, [
        cover,
        el('div', { class: 'body' }, [
          el('h3', { text: g.title[lang] }),
          el('p', { class: 'tagline', text: g.tagline[lang] }),
          el('p', { class: 'desc', text: g.desc[lang] }),
          el('ul', { class: 'tags' }, g.tags[lang].map(function (x) { return el('li', { text: x }); })),
          el('p', { class: 'fskwhy', text: 'FSK ' + g.fsk + ': ' + g.fskReason[lang] }),
          el('div', { class: 'actions' }, [
            play,
            (!locked && c) ? el('a', { class: 'alt-lang', href: 'games/' + g.slug + '/' + other + '/index.html', hreflang: other, lang: other, text: t('other.lang') }) : null
          ])
        ])
      ]);
      grid.appendChild(card);
    });
  }

  /* ---------- Gate ---------- */
  var pendingGame = null;
  function openGate(notice, gameSlug) {
    var g = $('#gate'); if (!g) return;
    pendingGame = gameSlug || null;
    var c = readConsent();
    $('#gAge').value = c ? c.now : '';
    $('#gTos').checked = !!c; $('#gPrivacy').checked = !!c; $('#gParent').checked = !!(c && c.parent);
    $('#gErr').textContent = '';
    var n = $('#gNotice');
    if (!store) notice = (notice ? notice + ' ' : '') + t('n.nostore');
    n.textContent = notice || ''; n.hidden = !notice;
    toggleParent();
    g.hidden = false;
    setTimeout(function () { $('#gAge').focus(); }, 30);
  }
  function closeGate() { var g = $('#gate'); if (g) g.hidden = true; }
  function toggleParent() {
    var a = parseInt($('#gAge').value, 10);
    $('#gParentRow').hidden = !(a > 0 && a < PARENT_AGE);
  }
  function submitGate(e) {
    e.preventDefault();
    var a = parseInt($('#gAge').value, 10), err = $('#gErr');
    if (!(a >= 3 && a <= 120)) { err.textContent = t('e.age'); $('#gAge').focus(); return; }
    if (!$('#gTos').checked) { err.textContent = t('e.tos'); return; }
    if (!$('#gPrivacy').checked) { err.textContent = t('e.privacy'); return; }
    if (a < PARENT_AGE && !$('#gParent').checked) { err.textContent = t('e.parent'); return; }
    saveConsent(a, a < PARENT_AGE);
    showNotice('');
    closeGate();
    applyLang();
    if (pendingGame) {
      var g = (window.MW_GAMES || []).filter(function (x) { return x.slug === pendingGame; })[0];
      if (g && a >= g.fsk && store) { location.href = 'games/' + g.slug + '/' + lang + '/index.html'; return; }
      if (g && a < g.fsk) showNotice(t('n.age', { g: g.title[lang], n: g.fsk }));
    }
  }
  function showNotice(msg) {
    var n = $('#pageNotice'); if (!n) return;
    n.textContent = msg; n.hidden = !msg;
  }

  function init() {
    document.querySelectorAll('.lang button').forEach(function (b) {
      b.addEventListener('click', function () { lang = b.dataset.lang; showNotice(''); applyLang(); });
    });
    var chip = $('#ageChip'); if (chip) chip.addEventListener('click', function () { openGate(); });
    var form = $('#gateForm');
    if (form) { form.addEventListener('submit', submitGate); $('#gAge').addEventListener('input', toggleParent); }
    var reset = $('#resetData'), armed = null;
    if (reset) reset.addEventListener('click', function () {
      if (!armed) {
        reset.classList.add('armed'); reset.textContent = t('f.reset2');
        armed = setTimeout(function () { armed = null; reset.classList.remove('armed'); reset.textContent = t('f.reset'); }, 4000);
        return;
      }
      clearTimeout(armed); armed = null; reset.classList.remove('armed');
      KEYS.forEach(del); memConsent = null;
      reset.textContent = t('f.done');
      setTimeout(function () { reset.textContent = t('f.reset'); }, 2500);
      applyLang();
      if ($('#gate')) openGate();
    });
    var y = $('#year'); if (y) y.textContent = new Date().getFullYear();

    applyLang();

    // Coming back from a game page (gate.js) or first visit
    if ($('#gate')) {
      var next = params.get('next'), why = params.get('why'), c = readConsent();
      var g = next && (window.MW_GAMES || []).filter(function (x) { return x.slug === next; })[0];
      if (!c) openGate(next ? t('n.consent') : '', g ? g.slug : null);
      else if (g && why === 'age') showNotice(t('n.age', { g: g.title[lang], n: g.fsk }));
      else if (g && c.now >= g.fsk && why === 'consent') location.replace('games/' + g.slug + '/' + lang + '/index.html');
      if (next && history.replaceState) history.replaceState(null, '', location.pathname);
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
