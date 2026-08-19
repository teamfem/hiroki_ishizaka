from pathlib import Path
from urllib.parse import urlparse
import datetime as dt
import re
import subprocess
import xml.etree.ElementTree as ET

SITE_PREFIX = '/hiroki_ishizaka/'
SITEMAP = Path('sitemap.xml')


def local_path(url: str) -> Path:
    path = urlparse(url).path
    if not path.startswith(SITE_PREFIX):
        raise RuntimeError(f'Unexpected sitemap URL: {url}')
    rel = path[len(SITE_PREFIX):]
    if not rel:
        return Path('index.html')
    if rel.endswith('/'):
        return Path(rel) / 'index.html'
    return Path(rel)


def embedded_modified_date(path: Path) -> str | None:
    if not path.exists() or path.suffix.lower() != '.html':
        return None
    text = path.read_text(encoding='utf-8')
    patterns = [
        r'"dateModified"\s*:\s*"(\d{4}-\d{2}-\d{2})"',
        r'<meta\s+property=["\']article:modified_time["\']\s+content=["\'](\d{4}-\d{2}-\d{2})',
        r'<meta\s+content=["\'](\d{4}-\d{2}-\d{2})[^"\']*["\']\s+property=["\']article:modified_time["\']',
    ]
    for pattern in patterns:
        m = re.search(pattern, text, re.I)
        if m:
            return m.group(1)
    return None


def git_modified_date(path: Path) -> str:
    proc = subprocess.run(
        ['git', 'log', '-1', '--format=%cs', '--', path.as_posix()],
        check=True,
        text=True,
        capture_output=True,
    )
    value = proc.stdout.strip()
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        raise RuntimeError(f'No Git modification date for {path}')
    return value


def modified_date(path: Path) -> str:
    # Blog posts already carry article-level modification dates.  Prefer these
    # because they describe the article itself rather than a repository-wide
    # metadata/navigation edit.  Other pages use the latest Git change date.
    if path.parts[:2] == ('blog', 'posts'):
        embedded = embedded_modified_date(path)
        if embedded:
            return embedded
    return git_modified_date(path)


root = ET.parse(SITEMAP).getroot()
ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
entries = root.findall('sm:url', ns)
if len(entries) != 69:
    raise RuntimeError(f'Expected 69 sitemap URLs, found {len(entries)}')

rows: list[tuple[str, str]] = []
for entry in entries:
    loc = entry.find('sm:loc', ns)
    if loc is None or not loc.text:
        raise RuntimeError('Sitemap entry without loc')
    url = loc.text.strip()
    path = local_path(url)
    if not path.exists():
        raise RuntimeError(f'Missing local file for {url}: {path}')
    date = modified_date(path)
    # Defensive ISO-date validation.
    dt.date.fromisoformat(date)
    rows.append((url, date))

lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">', '']
for url, date in rows:
    lines.extend([
        '  <url>',
        f'    <loc>{url}</loc>',
        f'    <lastmod>{date}</lastmod>',
        '  </url>',
        '',
    ])
lines.append('</urlset>')
SITEMAP.write_text('\n'.join(lines) + '\n', encoding='utf-8')

# Final validation.
text = SITEMAP.read_text(encoding='utf-8')
if text.count('<loc>') != 69 or text.count('<lastmod>') != 69:
    raise RuntimeError('Final sitemap does not contain 69 loc/lastmod pairs')
ET.parse(SITEMAP)
print('SITEMAP_URLS', len(rows))
print('LASTMOD_ENTRIES', len(rows))
print('OLDEST_LASTMOD', min(date for _, date in rows))
print('NEWEST_LASTMOD', max(date for _, date in rows))
