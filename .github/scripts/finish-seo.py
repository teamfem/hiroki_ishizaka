from pathlib import Path
import re, json, html

ROOT=Path('.')
GENERIC='について，有限要素法・数値解析・PDEの観点から整理するHiroki Ishizakaの研究ノートです'
changed=[]
duplicate_pages=[]

META_DESC_RE=re.compile(r'<meta\b(?=[^>]*\bname=["\']description["\'])[^>]*>',re.I)
CANON_RE=re.compile(r'<link\b(?=[^>]*\brel=["\']canonical["\'])[^>]*>',re.I)

def attr(tag,name):
    m=re.search(r'\b'+re.escape(name)+r'=["\']([^"\']*)["\']',tag,re.I)
    return html.unescape(m.group(1)) if m else ''

def score_description(s):
    score=len(s)
    if GENERIC in s: score-=10000
    if '研究ノートです' in s and len(s)<100: score-=1000
    return score

def sync_meta(text, key, value, attr_name='property'):
    pat=re.compile(r'<meta\b(?=[^>]*\b'+re.escape(attr_name)+r'=["\']'+re.escape(key)+r'["\'])[^>]*>',re.I)
    repl=f'<meta {attr_name}="{key}" content="{html.escape(value,quote=True)}">'
    if pat.search(text):
        return pat.sub(repl,text,count=1)
    return text

def sync_blogposting_jsonld(text, value):
    pat=re.compile(r'(<script\b[^>]*id=["\']site-structured-data["\'][^>]*>)(.*?)(</script>)',re.I|re.S)
    m=pat.search(text)
    if not m: return text
    try:
        data=json.loads(m.group(2))
    except Exception:
        return text
    graph=data.get('@graph',[]) if isinstance(data,dict) else []
    touched=False
    for node in graph:
        if not isinstance(node,dict): continue
        typ=node.get('@type')
        if typ=='BlogPosting' or (isinstance(typ,list) and 'BlogPosting' in typ):
            if node.get('description')!=value:
                node['description']=value
                touched=True
    if not touched: return text
    body='\n'+json.dumps(data,ensure_ascii=False,indent=2)+'\n'
    return text[:m.start()]+m.group(1)+body+m.group(3)+text[m.end():]

for p in sorted(ROOT.rglob('*.html')):
    if '.github' in p.parts or p.name.startswith('google'):
        continue
    text=p.read_text(encoding='utf-8')
    original=text
    tags=META_DESC_RE.findall(text)
    if len(tags)>1:
        values=[attr(t,'content').strip() for t in tags if attr(t,'content').strip()]
        if not values:
            raise RuntimeError(f'{p}: duplicate description tags without content')
        chosen=max(values,key=score_description)
        duplicate_pages.append((p.as_posix(),len(tags),chosen))
        first=True
        def repl(m):
            nonlocal_holder=None
            return ''
        # Replace first description with chosen and remove subsequent ones.
        out=[]; last=0
        for i,m in enumerate(META_DESC_RE.finditer(text)):
            out.append(text[last:m.start()])
            if i==0:
                out.append(f'<meta name="description" content="{html.escape(chosen,quote=True)}">')
            last=m.end()
        out.append(text[last:])
        text=''.join(out)
        text=sync_meta(text,'og:description',chosen,'property')
        text=sync_meta(text,'twitter:description',chosen,'name')
        text=sync_blogposting_jsonld(text,chosen)
    if text!=original:
        p.write_text(text,encoding='utf-8')
        changed.append(p.as_posix())

# Strengthen the existing final audit so future checks catch duplicate metadata.
audit=Path('.github/scripts/final-site-audit.py')
if audit.exists():
    s=audit.read_text(encoding='utf-8')
    marker="    text=path.read_text(encoding='utf-8')\n"
    addition="""    text=path.read_text(encoding='utf-8')\n    desc_tags=re.findall(r'<meta\\b(?=[^>]*\\bname=[\\\"\\\']description[\\\"\\\'])[^>]*>',text,re.I)\n    if len(desc_tags)!=1: fail(f'Meta description count {len(desc_tags)}: {path}')\n    canon_tags=re.findall(r'<link\\b(?=[^>]*\\brel=[\\\"\\\']canonical[\\\"\\\'])[^>]*>',text,re.I)\n    if len(canon_tags)!=1: fail(f'Canonical count {len(canon_tags)}: {path}')\n"""
    if 'Meta description count' not in s:
        if marker not in s: raise RuntimeError('final audit insertion marker not found')
        s=s.replace(marker,addition,1)
        audit.write_text(s,encoding='utf-8')

# Validate every normal HTML page has at most one description; sitemap audit enforces exactly one.
remaining=[]
for p in sorted(ROOT.rglob('*.html')):
    if '.github' in p.parts or p.name.startswith('google'):
        continue
    t=p.read_text(encoding='utf-8')
    n=len(META_DESC_RE.findall(t))
    if n>1: remaining.append((p.as_posix(),n))
if remaining: raise RuntimeError(f'Remaining duplicate descriptions: {remaining}')

print('DUPLICATE_DESCRIPTION_PAGES',len(duplicate_pages))
for item in duplicate_pages:
    print('FIXED',item[0],item[1],item[2])
print('HTML_FILES_CHANGED',len(changed))
print('FINAL_SEO_METADATA_CLEANUP VALIDATED')
