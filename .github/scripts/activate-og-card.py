from pathlib import Path
from urllib.parse import urlparse
import re, xml.etree.ElementTree as ET, html

OLD='https://teamfem.github.io/hiroki_ishizaka/head_image.png'
NEW='https://teamfem.github.io/hiroki_ishizaka/og-card.png'
changed=[]

root=ET.parse('sitemap.xml')
ns={'sm':'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls=[n.text.strip() for n in root.findall('.//sm:loc',ns) if n.text]

def path_for(url):
    path=urlparse(url).path
    prefix='/hiroki_ishizaka/'
    rel=path[len(prefix):]
    if not rel: return Path('index.html')
    if rel.endswith('/'): return Path(rel)/'index.html'
    return Path(rel)

def get_content_meta(s,name):
    tags=re.findall(r'<meta\b[^>]*>',s,re.I)
    for tag in tags:
        if not re.search(r'\bname=["\']'+re.escape(name)+r'["\']',tag,re.I):
            continue
        m=re.search(r'\bcontent=["\']([^"\']*)["\']',tag,re.I)
        if m: return html.unescape(m.group(1))
    return ''

def get_canonical(s):
    tags=re.findall(r'<link\b[^>]*>',s,re.I)
    for tag in tags:
        if not re.search(r'\brel=["\']canonical["\']',tag,re.I):
            continue
        m=re.search(r'\bhref=["\']([^"\']+)["\']',tag,re.I)
        if m: return html.unescape(m.group(1))
    return ''

def get_title(s):
    m=re.search(r'<title>(.*?)</title>',s,re.I|re.S)
    return html.unescape(re.sub(r'\s+',' ',m.group(1)).strip()) if m else ''

def social_block(s,p):
    title=get_title(s)
    desc=get_content_meta(s,'description')
    canonical=get_canonical(s)
    if not title or not desc or not canonical:
        raise RuntimeError(f'{p}: cannot construct social metadata')
    langm=re.search(r'<html\b[^>]*\blang=["\']([^"\']+)',s,re.I)
    lang=(langm.group(1) if langm else 'en').lower()
    locale='ja_JP' if lang.startswith('ja') else 'en_GB'
    typ='article' if p.parts[:2]==('blog','posts') else 'website'
    e=lambda x: html.escape(x,quote=True)
    return f'''\n<!-- Social sharing metadata -->\n<meta property="og:type" content="{typ}">\n<meta property="og:site_name" content="Hiroki Ishizaka">\n<meta property="og:locale" content="{locale}">\n<meta property="og:title" content="{e(title)}">\n<meta property="og:description" content="{e(desc)}">\n<meta property="og:url" content="{e(canonical)}">\n<meta property="og:image" content="{NEW}">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<meta property="og:image:type" content="image/png">\n<meta property="og:image:alt" content="Hiroki Ishizaka — Numerical Analysis · PDEs · FEM">\n<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:site" content="@teamfem16key">\n<meta name="twitter:creator" content="@teamfem16key">\n<meta name="twitter:title" content="{e(title)}">\n<meta name="twitter:description" content="{e(desc)}">\n<meta name="twitter:image" content="{NEW}">\n<meta name="twitter:image:alt" content="Hiroki Ishizaka — Numerical Analysis · PDEs · FEM">\n'''

for url in urls:
    p=path_for(url)
    s=p.read_text(encoding='utf-8')
    original=s
    s=s.replace(OLD,NEW)
    if '<meta property="og:image"' not in s:
        if '</head>' not in s.lower():
            raise RuntimeError(f'{p}: head closing tag missing')
        block=social_block(s,p)
        pos=s.lower().rfind('</head>')
        s=s[:pos]+block+s[pos:]
    elif 'property="og:image:width"' not in s:
        m=re.search(r'<meta property="og:image"[^>]*>',s,re.I)
        if m:
            extra='\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<meta property="og:image:type" content="image/png">'
            s=s[:m.end()]+extra+s[m.end():]
    if s!=original:
        p.write_text(s,encoding='utf-8')
        changed.append(p.as_posix())

errors=[]
for url in urls:
    p=path_for(url)
    s=p.read_text(encoding='utf-8')
    if OLD in s: errors.append(f'{p}: old sharing image remains')
    if f'<meta property="og:image" content="{NEW}">' not in s: errors.append(f'{p}: dedicated og:image missing')
    if f'<meta name="twitter:image" content="{NEW}">' not in s: errors.append(f'{p}: dedicated twitter:image missing')
    for marker in ('og:image:width" content="1200','og:image:height" content="630','og:image:type" content="image/png'):
        if marker not in s: errors.append(f'{p}: missing {marker}')
if not Path('og-card.png').exists(): errors.append('og-card.png missing')
if errors: raise RuntimeError('\n'.join(errors))
print('SITEMAP_URLS',len(urls))
print('HTML_FILES_CHANGED',len(changed))
print('DEDICATED_OG_CARD ACTIVE')
