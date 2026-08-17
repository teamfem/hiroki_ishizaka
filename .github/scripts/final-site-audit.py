from pathlib import Path
from urllib.parse import urlparse, urljoin
import re
import xml.etree.ElementTree as ET

ROOT=Path('.')
BASE='https://teamfem.github.io/hiroki_ishizaka/'

errors=[]
warnings=[]

def fail(msg): errors.append(msg)
def warn(msg): warnings.append(msg)

def html_for_url(url):
    p=urlparse(url).path
    prefix='/hiroki_ishizaka/'
    if not p.startswith(prefix): return None
    rel=p[len(prefix):]
    if not rel: return Path('index.html')
    if rel.endswith('/'):
        return Path(rel)/'index.html'
    return Path(rel)

# Sitemap inventory.
tree=ET.parse('sitemap.xml')
ns={'sm':'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls=[n.text.strip() for n in tree.findall('.//sm:loc',ns) if n.text]
if len(urls)!=len(set(urls)): fail('Duplicate URLs in sitemap')

sitemap_paths=set()
titles={}
for url in urls:
    path=html_for_url(url)
    if path is None:
        fail(f'Off-site sitemap URL: {url}')
        continue
    sitemap_paths.add(path.as_posix())
    if not path.exists():
        fail(f'Missing sitemap file: {url} -> {path}')
        continue
    text=path.read_text(encoding='utf-8')
    tm=re.search(r'<title>(.*?)</title>',text,re.I|re.S)
    if not tm: fail(f'Missing title: {path}')
    else:
        title=re.sub(r'\s+',' ',tm.group(1)).strip()
        titles.setdefault(title,[]).append(path.as_posix())
    cm=re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']',text,re.I)
    if not cm: fail(f'Missing canonical: {path}')
    elif cm.group(1)!=url: fail(f'Canonical mismatch: {path}: {cm.group(1)} != {url}')
    if re.search(r'<meta[^>]+name=["\']robots["\'][^>]+content=["\'][^"\']*noindex',text,re.I):
        fail(f'Sitemap URL is noindex: {path}')

for title,paths in titles.items():
    if len(paths)>1: fail(f'Duplicate title: {title}: {paths}')

# Normal public HTML should be represented in sitemap, except deliberate exceptions.
exclude={'404.html'}
for p in ROOT.glob('google*.html'): exclude.add(p.as_posix())
for p in ROOT.rglob('*.html'):
    if '.github' in p.parts: continue
    s=p.as_posix()
    if s in exclude: continue
    if s not in sitemap_paths:
        fail(f'Public HTML outside sitemap: {s}')

# 404 should remain noindex.
if Path('404.html').exists():
    t=Path('404.html').read_text(encoding='utf-8')
    if not re.search(r'<meta[^>]+name=["\']robots["\'][^>]+content=["\'][^"\']*noindex',t,re.I):
        fail('404.html is not noindex')

# Local links in sitemap pages. Remove HTML comments before parsing hrefs.
for url in urls:
    p=html_for_url(url)
    if not p or not p.exists(): continue
    text=p.read_text(encoding='utf-8')
    text=re.sub(r'<!--.*?-->','',text,flags=re.S)
    for href in re.findall(r'<a\b[^>]*\bhref=["\']([^"\']+)["\']',text,re.I):
        href=href.strip()
        if not href or href.startswith(('#','mailto:','tel:','javascript:')): continue
        absolute=urljoin(url,href)
        parsed=urlparse(absolute)
        if parsed.netloc!='teamfem.github.io' or not parsed.path.startswith('/hiroki_ishizaka/'): continue
        target=html_for_url(absolute.split('#',1)[0].split('?',1)[0])
        if target and not target.exists(): fail(f'Broken local link: {p} -> {href} -> {target}')

# Static modern navigation: every page using .navlinks must contain all eight links.
modern_count=0
for p in ROOT.rglob('*.html'):
    if '.github' in p.parts: continue
    text=p.read_text(encoding='utf-8')
    m=re.search(r'<nav class=["\']navlinks["\'][^>]*>(.*?)</nav>',text,re.I|re.S)
    if not m: continue
    modern_count+=1
    block=m.group(1)
    if len(re.findall(r'<a\b',block,re.I))!=8: fail(f'Modern nav does not have 8 links: {p}')
    for label in ('Research','Publications','Visions','Supplementary','Blog','Geometry','Links','Contact'):
        if f'>{label}</a>' not in block: fail(f'Modern nav missing {label}: {p}')

# Blog source menus remain useful without runtime modernisation.
blog_count=0
for p in Path('blog/posts').glob('*.html'):
    blog_count+=1
    text=p.read_text(encoding='utf-8')
    m=re.search(r'<ul id=["\']menu["\']>(.*?)</ul>',text,re.I|re.S)
    if not m or len(re.findall(r'<li\b',m.group(1),re.I))!=8:
        fail(f'Blog source menu does not have 8 entries: {p}')

print(f'SITEMAP_URLS {len(urls)}')
print(f'MODERN_NAV_PAGES {modern_count}')
print(f'BLOG_POSTS {blog_count}')
print(f'ERRORS {len(errors)}')
print(f'WARNINGS {len(warnings)}')
for x in errors: print('ERROR:',x)
for x in warnings: print('WARNING:',x)
if errors: raise SystemExit(1)
print('FINAL_SITE_AUDIT CLEAN')
