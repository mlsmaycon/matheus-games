"""Shared fixtures: serve the built site (dist/) on a local port and open it in Chromium.

Run:  python3 tools/build.py && python3 -m pytest tests
(the tests build the site themselves if dist/ is missing)
"""
import functools, http.server, json, os, socketserver, subprocess, sys, threading
import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(REPO, 'dist')
LANGS = ('de', 'en')


def load_games():
    out = subprocess.check_output(['node', '-e',
        "const fs=require('fs');const w={};new Function('window',fs.readFileSync(process.argv[1],'utf8'))(w);"
        "process.stdout.write(JSON.stringify(w.MW_GAMES))", os.path.join(REPO, 'site', 'assets', 'games.js')])
    return json.loads(out)


GAMES = load_games()
SLUGS = [g['slug'] for g in GAMES]


@pytest.fixture(scope='session')
def dist():
    if not os.path.isfile(os.path.join(DIST, 'index.html')):
        subprocess.run([sys.executable, os.path.join(REPO, 'tools', 'build.py')], check=True)
    return DIST


@pytest.fixture(scope='session')
def base_url(dist):
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    handler = functools.partial(Quiet, directory=dist)
    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), handler)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f'http://127.0.0.1:{srv.server_address[1]}/'
    srv.shutdown()


@pytest.fixture(scope='session')
def browser():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--use-gl=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist'])
        yield b
        b.close()


class Page:
    """A fresh browser context with helpers: collects JS errors and requests to other hosts."""
    def __init__(self, browser, base_url, viewport=(1280, 900)):
        self.base = base_url
        self.ctx = browser.new_context(viewport={'width': viewport[0], 'height': viewport[1]})
        # Never really talk to Google from tests: answer analytics requests locally.
        self.ctx.route('**/*googletagmanager.com/**', lambda r: r.fulfill(status=200, body='', content_type='text/javascript'))
        self.ctx.route('**/*google-analytics.com/**', lambda r: r.fulfill(status=204, body=''))
        self.pg = self.ctx.new_page()
        self.errors, self.external = [], []
        self.pg.on('pageerror', lambda e: self.errors.append(str(e)))
        self.pg.on('console', lambda m: self.errors.append(m.text) if m.type == 'error' else None)
        self.pg.on('request', lambda r: None if r.url.startswith(base_url) or r.url.startswith('data:') else self.external.append(r.url))

    def goto(self, path, wait=1200):
        self.pg.goto(self.base + path)
        self.pg.wait_for_timeout(wait)
        return self.pg

    def set_storage(self, age=30, analytics='denied'):
        self.goto('LICENSE.txt', 50)
        self.pg.evaluate("""([age, an]) => {
            localStorage.setItem('mw-consent', JSON.stringify({v: 1, age: age, at: Date.now(), tos: true, privacy: true}));
            if (an) localStorage.setItem('mcg-analytics', JSON.stringify({v: 1, choice: an, at: Date.now()}));
        }""", [age, analytics])

    def close(self):
        self.ctx.close()


@pytest.fixture
def page(browser, base_url):
    p = Page(browser, base_url)
    yield p
    p.close()


@pytest.fixture
def phone(browser, base_url):
    p = Page(browser, base_url, viewport=(400, 800))
    yield p
    p.close()
