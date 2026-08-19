from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen
import json
import os
import subprocess
import time
import xml.etree.ElementTree as ET

HOST = 'teamfem.github.io'
BASE = 'https://teamfem.github.io/hiroki_ishizaka/'
KEY = '7f93c6b67bd8de89ea3501dfb9cb7045'
KEY_LOCATION = BASE + KEY + '.txt'
ENDPOINT = 'https://api.indexnow.org/indexnow'


def sitemap_urls() -> list[str]:
    root = ET.parse('sitemap.xml').getroot()
    ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    return [x.text.strip() for x in root.findall('.//sm:loc', ns) if x.text]


def public_url_for_path(path: str) -> str | None:
    path = path.replace('\\', '/')
    if not path.endswith('.html'):
        return None
    if path == '404.html' or path.startswith('google') or '/google' in path:
        return None
    if path == 'index.html':
        return BASE
    if path.endswith('/index.html'):
        return BASE + path[:-10]
    return BASE + path


def changed_files() -> list[str]:
    before = os.environ.get('BEFORE', '').strip()
    after = os.environ.get('AFTER', '').strip()
    zero = '0' * 40
    if not before or not after or before == zero:
        return []
    proc = subprocess.run(
        ['git', 'diff', '--name-only', before, after],
        text=True,
        check=True,
        capture_output=True,
    )
    return [x.strip() for x in proc.stdout.splitlines() if x.strip()]


all_urls = sitemap_urls()
allowed = set(all_urls)
changed = []
for path in changed_files():
    url = public_url_for_path(path)
    if url and url in allowed:
        changed.append(url)

# On initial installation (workflow-file-only push), notify the full public sitemap.
urls = sorted(set(changed)) if changed else all_urls
if not urls:
    raise RuntimeError('No URLs available for IndexNow submission')

# Wait until GitHub Pages serves the verification key from the public site.
verified = False
for _ in range(18):
    try:
        with urlopen(KEY_LOCATION, timeout=15) as r:
            body = r.read().decode('utf-8').strip()
            if r.status == 200 and body == KEY:
                verified = True
                break
    except Exception:
        pass
    time.sleep(10)
if not verified:
    raise RuntimeError(f'IndexNow key not yet reachable at {KEY_LOCATION}')

payload = json.dumps({
    'host': HOST,
    'key': KEY,
    'keyLocation': KEY_LOCATION,
    'urlList': urls,
}).encode('utf-8')
req = Request(
    ENDPOINT,
    data=payload,
    method='POST',
    headers={
        'Content-Type': 'application/json; charset=utf-8',
        'User-Agent': 'hiroki-ishizaka-github-pages-indexnow/1.0',
    },
)

last_error = None
for attempt in range(3):
    try:
        with urlopen(req, timeout=30) as r:
            status = r.status
            if status in (200, 202):
                print('INDEXNOW_STATUS', status)
                print('INDEXNOW_URLS', len(urls))
                for url in urls:
                    print(url)
                break
            last_error = RuntimeError(f'Unexpected IndexNow status {status}')
    except Exception as exc:
        last_error = exc
    if attempt < 2:
        time.sleep(15 * (attempt + 1))
else:
    raise RuntimeError(f'IndexNow submission failed: {last_error}')
