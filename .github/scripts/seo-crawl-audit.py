from pathlib import Path
from urllib.parse import urlparse, urljoin
import re
import xml.etree.ElementTree as ET

ROOT='https://teamfem.github.io/hiroki_ishizaka/'
BASE_PATH='/hiroki_ishizaka/'
repo=Path('.')

def clean_url(u):
    return u.split('#',1)[0].split('?',1)[0]

def file_to_url(p: Path):
    s=p.as_posix()
    if s=='index.html': return ROOT
    if s.endswith('/index.html'): return ROOT+s[:-10]
    return ROOT+s

def url_to_file(u):
    x=urlparse(u)
    path=x.path
    if not path.startswith(BASE_PATH): return None
    rel=path[len(BASE_PATH):]
    if rel=='': return Path('index.html')
    if rel.endswith('/'): return Path(rel)/'index.html'
    return Path(rel)

def meta_content(html,name):
    m=re.search(r'<meta\b[^>]*\bname=["\']'+re.escape(name)+r'["\'][^>]*\bcontent=["\']([^"\']*)["\'][^>]*>',html,re.I)
    if not m:
        m=re.search(r'<meta\b[^>]*\bcontent=["\']([^"\']*)["\'][^>]*\bname=["\']'+re.escape(name)+r'["\'][^>]*>',html,re.I)
    return m.group(1).strip() if m else None

def canonical(html):
    m=re.search(r'<link\b[^>]*\brel=["\']canonical["\'][^>]*\bhref=["\']([^"\']+)["\'][^>]*>',html,re.I)
    if not m:
        m=re.search(r'<link\b[^>]*\bhref=["\']([^"\']+)["\'][^>]*\brel=["\']canonical["\'][^>]*>',html,re.I)
    return m.group(1).strip() if m else None

def title(html):
    m=re.search(r'<title>(.*?)</title>',html,re.I|re.S)
    return re.sub(r'\s+',' ',m.group(1)).strip() if m else ''

root=ET.parse('sitemap.xml').getroot()
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
sitemap=[e.text.strip() for e in root.findall('s:url/s:loc',ns)]
sitemap_set=set(sitemap)

html_files=sorted(repo.rglob('*.html'))
html_files=[p for p in html_files if '.git' not in p.parts and 'site_libs' not in p.parts]

missing_sitemap_files=[]
for u in sitemap:
    f=url_to_file(u)
    if f is not None and not f.exists(): missing_sitemap_files.append((u,str(f)))

missing_canonical=[]
canonical_mismatch=[]
noindex=[]
public_orphans=[]
duplicate_titles={}
broken_links=[]

for p in html_files:
    html=p.read_text(encoding='utf-8',errors='replace')
    html_for_links=re.sub(r'<!--.*?-->','',html,flags=re.S)
    u=file_to_url(p)
    can=canonical(html)
    robots=(meta_content(html,'robots') or '').lower()
    ttl=title(html)
    if ttl: duplicate_titles.setdefault(ttl,[]).append(str(p))
    if 'noindex' in robots: noindex.append(str(p))
    if u in sitemap_set:
        if not can: missing_canonical.append(str(p))
        elif clean_url(can)!=clean_url(u): canonical_mismatch.append((str(p),can,u))
    else:
        is_google_verification=p.name.startswith('google') and p.suffix=='.html'
        if p.name!='404.html' and not is_google_verification and 'noindex' not in robots:
            public_orphans.append((str(p),can or ''))

    for href in re.findall(r'<a\b[^>]*\bhref=["\']([^"\']+)["\']',html_for_links,re.I):
        href=href.strip()
        if not href or href.startswith(('#','mailto:','tel:','javascript:')): continue
        parsed=urlparse(href)
        if parsed.scheme in ('http','https'):
            if not href.startswith(ROOT): continue
            target=url_to_file(clean_url(href))
        else:
            absu=urljoin(u,href)
            if not absu.startswith(ROOT): continue
            target=url_to_file(clean_url(absu))
        if target is None: continue
        candidates=[target]
        if target.suffix=='':
            candidates += [Path(str(target)+'.html'), target/'index.html']
        if not any(c.exists() for c in candidates):
            broken_links.append((str(p),href,str(target)))

seen=set(); broken_unique=[]
for x in broken_links:
    if x not in seen:
        seen.add(x); broken_unique.append(x)

print('=== SEO / CRAWL AUDIT ===')
print('SITEMAP_URLS',len(sitemap))
print('HTML_FILES_AUDITED',len(html_files))
print('SITEMAP_MISSING_FILES',len(missing_sitemap_files))
for x in missing_sitemap_files: print('  ',x)
print('SITEMAP_PAGES_MISSING_CANONICAL',len(missing_canonical))
for x in missing_canonical: print('  ',x)
print('CANONICAL_MISMATCHES',len(canonical_mismatch))
for x in canonical_mismatch: print('  ',x)
print('NOINDEX_HTML',len(noindex))
for x in noindex: print('  ',x)
print('PUBLIC_HTML_NOT_IN_SITEMAP',len(public_orphans))
for x in public_orphans: print('  ',x)
print('BROKEN_LOCAL_LINKS',len(broken_unique))
for x in broken_unique[:200]: print('  ',x)
print('DUPLICATE_TITLES')
for t,paths in duplicate_titles.items():
    if len(paths)>1:
        print('  ',repr(t),paths)
