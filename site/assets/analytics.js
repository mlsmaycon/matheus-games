/*
  My Craft Games – optional Google Analytics 4, ONLY after opt-in consent.
  Until the visitor (or, for children under 16, a parent) clicks "Accept",
  nothing is loaded from Google and no cookies are set.
  The choice is stored in localStorage ("mcg-analytics") and can be changed any time
  via the "Cookie settings" link in the footer.
  Include on every page:  <script src="assets/analytics.js" defer></script>  (path relative to the page)
*/
(function () {
  var GA_ID = 'G-0QMCMFM2YN';
  var KEY = 'mcg-analytics', VER = 1;
  var me = document.currentScript;
  var root = me ? me.src.replace(/assets\/analytics\.js(\?.*)?$/, '') : '';
  var game = '';
  var gs = document.querySelector('script[data-game]');
  if (gs) game = gs.getAttribute('data-game') || '';

  var store = null;
  try { store = window.localStorage; store.getItem('x'); } catch (e) { store = null; }
  function get(k) { try { return store ? store.getItem(k) : null; } catch (e) { return null; } }
  function set(k, v) { try { if (store) store.setItem(k, v); } catch (e) {} }
  function del(k) { try { if (store) store.removeItem(k); } catch (e) {} }

  function lang() {
    var l = (get('mw-lang') || document.documentElement.lang || 'de').slice(0, 2);
    return l === 'en' ? 'en' : 'de';
  }
  function age() {
    try {
      var c = JSON.parse(get('mw-consent') || 'null');
      if (c && typeof c.age === 'number' && typeof c.at === 'number')
        return c.age + Math.floor((Date.now() - c.at) / (365.25 * 24 * 3600 * 1000));
    } catch (e) {}
    return -1;
  }
  function choice() {
    try { var c = JSON.parse(get(KEY) || 'null'); return c && c.v === VER ? c.choice : null; } catch (e) { return null; }
  }

  var T = {
    de: {
      title: 'Darf My Craft Games zählen, welche Spiele gespielt werden?',
      text: 'Wenn du zustimmst, nutzen wir Google Analytics. Dabei setzt Google Cookies und erfährt zum Beispiel, welche Seiten und Spiele aufgerufen werden. Es gibt keine Werbung und keine Profile für Werbung. Ohne Zustimmung wird nichts an Google gesendet.',
      kid: 'Du bist unter 16? Dann frag bitte deine Eltern, bevor du zustimmst.',
      more: 'Mehr in der Datenschutzerklärung',
      yes: 'Zustimmen', yesParent: 'Ein Elternteil stimmt zu', no: 'Ablehnen',
      settings: 'Cookie-Einstellungen'
    },
    en: {
      title: 'May My Craft Games count which games are played?',
      text: 'If you agree, we use Google Analytics. Google then sets cookies and learns, for example, which pages and games are opened. There are no ads and no ad profiles. Without your consent, nothing is sent to Google.',
      kid: 'Are you under 16? Then please ask a parent before you agree.',
      more: 'More in the Privacy Policy',
      yes: 'Accept', yesParent: 'A parent agrees', no: 'Decline',
      settings: 'Cookie settings'
    }
  };

  var loaded = false;
  function load() {
    window['ga-disable-' + GA_ID] = false;
    if (loaded) return;
    loaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    gtag('consent', 'default', { ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', analytics_storage: 'granted' });
    gtag('set', 'ads_data_redaction', true);
    gtag('js', new Date());
    gtag('config', GA_ID, {
      allow_google_signals: false,
      allow_ad_personalization_signals: false,
      content_group: game ? 'game' : 'site',
      site_language: lang()
    });
    if (game) gtag('event', 'play_game', { game_slug: game, game_language: (document.documentElement.lang || 'de').slice(0, 2) });
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
  }
  function clearCookies() {
    var host = location.hostname, parts = host.split('.'), domains = ['', host];
    for (var i = 1; i < parts.length - 1; i++) domains.push('.' + parts.slice(i).join('.'));
    domains.push('.' + host);
    document.cookie.split(';').forEach(function (c) {
      var n = c.split('=')[0].trim();
      if (!/^_ga|^_gid|^_gat/.test(n)) return;
      domains.forEach(function (d) {
        document.cookie = n + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/' + (d ? '; domain=' + d : '');
      });
    });
  }
  function decide(c) {
    set(KEY, JSON.stringify({ v: VER, choice: c, at: Date.now() }));
    hide();
    if (c === 'granted') load();
    else { window['ga-disable-' + GA_ID] = true; if (window.gtag) gtag('consent', 'update', { analytics_storage: 'denied' }); clearCookies(); }
  }

  var box = null;
  function css() {
    if (document.getElementById('mcg-cc-css')) return;
    var st = document.createElement('style'); st.id = 'mcg-cc-css';
    st.textContent =
      '.mcg-cc{position:fixed;left:12px;right:12px;bottom:12px;z-index:900;max-width:760px;margin:0 auto;background:#171a33;color:#f6f4ee;border:2px solid #ffffff2e;border-radius:16px;padding:14px 16px;box-shadow:0 10px 40px #0008;font:14px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif}' +
      '.mcg-cc b{display:block;font-size:15px;margin-bottom:4px}.mcg-cc p{margin:0 0 6px}.mcg-cc .kid{color:#ffd23f;font-weight:600}' +
      '.mcg-cc a{color:#9ad0ff}.mcg-cc .row{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end;margin-top:8px}' +
      '.mcg-cc button{font:700 14px system-ui,sans-serif;border:0;border-radius:10px;padding:9px 16px;cursor:pointer}' +
      '.mcg-cc .yes{background:#ff9f2e;color:#171a33}.mcg-cc .no{background:#ffffff1f;color:#f6f4ee}' +
      '.mcg-cc button:focus-visible{outline:3px solid #fff;outline-offset:2px}' +
      '.mcg-cs,.mw-copy .mcg-cs{background:none!important;border:0!important;box-shadow:none!important;padding:0!important;margin:0!important;color:inherit!important;text-decoration:underline;cursor:pointer;font:inherit!important;opacity:inherit;width:auto!important;height:auto!important}';
    document.head.appendChild(st);
  }
  function hide() { if (box) { box.remove(); box = null; } }
  function show() {
    css(); hide();
    var t = T[lang()], a = age(), kid = a >= 0 && a < 16;
    box = document.createElement('div');
    box.className = 'mcg-cc'; box.setAttribute('role', 'dialog'); box.setAttribute('aria-live', 'polite');
    box.setAttribute('aria-label', t.title);
    box.innerHTML = '<b></b><p class="txt"></p>' + (a < 0 || kid ? '<p class="kid"></p>' : '') +
      '<p><a class="more"></a></p><div class="row"><button type="button" class="no"></button><button type="button" class="yes"></button></div>';
    box.querySelector('b').textContent = t.title;
    box.querySelector('.txt').textContent = t.text;
    var k = box.querySelector('.kid'); if (k) k.textContent = t.kid;
    var m = box.querySelector('.more'); m.textContent = t.more; m.href = root + 'privacy.html#analytics';
    var no = box.querySelector('.no'), yes = box.querySelector('.yes');
    no.textContent = t.no; yes.textContent = kid ? t.yesParent : t.yes;
    no.addEventListener('click', function () { decide('denied'); });
    yes.addEventListener('click', function () { decide('granted'); });
    document.body.appendChild(box);
  }
  function settingsLinks() {
    var t = T[lang()];
    document.querySelectorAll('[data-cookie-settings]').forEach(function (b) {
      if (!b.dataset.bound) { b.dataset.bound = '1'; b.addEventListener('click', function (e) { e.preventDefault(); show(); }); }
    });
    var gc = document.querySelector('.mw-copy');
    if (gc && !gc.querySelector('.mcg-cs')) {
      var b = document.createElement('button'); b.type = 'button'; b.className = 'mcg-cs'; b.textContent = t.settings;
      b.addEventListener('click', show); gc.appendChild(document.createTextNode(' · ')); gc.appendChild(b);
    }
  }
  // Which game card was chosen on the start page
  document.addEventListener('click', function (e) {
    if (!loaded || !window.gtag) return;
    var a = e.target.closest && e.target.closest('a[href*="games/"]');
    if (!a) return;
    var m = a.getAttribute('href').match(/games\/([a-z0-9-]+)\/(de|en)\//);
    if (m) gtag('event', 'select_game', { game_slug: m[1], game_language: m[2] });
  }, true);

  window.mcgAnalytics = {
    open: show,
    choice: choice,
    reset: function () { del(KEY); window['ga-disable-' + GA_ID] = true; clearCookies(); }
  };

  function init() {
    settingsLinks();
    var c = choice();
    if (c === 'granted') load();
    else if (c !== 'denied') {
      // On the start page, ask after the age question has been answered.
      if (age() < 0 && document.getElementById('gate')) {
        var iv = setInterval(function () { if (age() >= 0) { clearInterval(iv); if (!choice()) show(); } }, 800);
      } else show();
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
