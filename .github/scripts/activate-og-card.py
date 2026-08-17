from pathlib import Path
from urllib.parse import urlparse
import re, xml.etree.ElementTree as ET

OLD='https://teamfem.github.io/hiroki_ishizaka/head_image.png'
NEW='https://teamfem.github.io/hiroki_ishizaka/og-card.png'
changed=[]

for p in sorted(Path('.').rglob('*.html')):
    if '.github' in p.parts or p.name.startswith('google'):
        continue
    s=p.read_text(encoding='utf-8')
    original=s
    s=s.replace(OLD,NEW)
    if '<meta property="og:image"' in s and 'property="og:image:width"' not in s:
        m=re.search(r'<meta property="og:image"[^>]*>',s,re.I)
        if m:
            extra='\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<meta property="og:image:type" content="image/png">'
            s=s[:m.end()]+extra+s[m.end():]
    if s!=original:
        p.write_text(s,encoding='utf-8')
        changed.append(p.as_posix())

# Validate sitemap pages use the dedicated image consistently.
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
