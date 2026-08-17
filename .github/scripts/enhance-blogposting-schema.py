from pathlib import Path
from datetime import datetime
import json, re

TODAY = '2026-08-17'
OG_IMAGE = 'https://teamfem.github.io/hiroki_ishizaka/head_image.png'


def section_for(name: str) -> str:
    if name.startswith('anisotropic-geometry-'):
        return 'Anisotropic finite-element geometry'
    if name.startswith('unresolved-memory-'):
        return 'Memory, delay and stable reduction'
    if name.startswith('exact-curved-fem-'):
        return 'Exact-curved FEM'
    if name.startswith('paradoxes-pitfalls-'):
        return 'Classical paradoxes and finite-element pitfalls'
    if name.startswith('pinns-'):
        return 'Physics-informed neural networks and numerical analysis'
    if name.startswith('lean4-'):
        return 'Certified FEM and formal reasoning'
    if name.startswith('disease-progression-') or name.startswith('dental-math-'):
        return 'Mathematical modelling of latent-state and disease progression'
    if name == 'article10may26_5.html':
        return 'Exploratory numerical analysis'
    if name.startswith('article'):
        return 'Foundations in numerical analysis and computational FEM'
    return 'Research notes in numerical analysis'


def fallback_date(name: str):
    # Legacy article filenames such as article15apr26.html.
    m = re.match(r'article(\d{2})([a-z]{3})(\d{2})', name, re.I)
    if not m:
        return None
    months = {'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}
    mon = months.get(m.group(2).lower())
    if not mon:
        return None
    return f'20{m.group(3)}-{mon:02d}-{int(m.group(1)):02d}'


def meta_value(text: str, name: str):
    patterns = [
        rf'<meta\b[^>]*\bname=["\']{re.escape(name)}["\'][^>]*\bcontent=["\']([^"\']*)["\'][^>]*>',
        rf'<meta\b[^>]*\bcontent=["\']([^"\']*)["\'][^>]*\bname=["\']{re.escape(name)}["\'][^>]*>'
    ]
    for pat in patterns:
        m = re.search(pat, text, re.I)
        if m:
            return m.group(1).strip()
    return ''


files = sorted(Path('blog/posts').glob('*.html'))
updated = 0
missing_dates = []

for p in files:
    text = p.read_text(encoding='utf-8')
    m = re.search(r'<script\s+id=["\']site-structured-data["\']\s+type=["\']application/ld\+json["\']>(.*?)</script>', text, re.I | re.S)
    if not m:
        continue

    data = json.loads(m.group(1))
    graph = data.get('@graph', [])
    posting = next((x for x in graph if isinstance(x, dict) and x.get('@type') == 'BlogPosting'), None)
    if not posting:
        continue

    tm = re.search(r'<time\b[^>]*\bdatetime=["\'](\d{4}-\d{2}-\d{2})["\']', text, re.I)
    published = tm.group(1) if tm else fallback_date(p.name)
    if not published:
        missing_dates.append(p.as_posix())
        continue

    section = section_for(p.name)
    keywords = meta_value(text, 'keywords')

    posting['datePublished'] = published
    posting['dateModified'] = max(published, TODAY)
    posting['articleSection'] = section
    posting['genre'] = 'Research note'
    posting['image'] = OG_IMAGE
    if keywords:
        posting['keywords'] = keywords

    new_json = json.dumps(data, ensure_ascii=False, indent=2)
    text = text[:m.start(1)] + '\n' + new_json + '\n' + text[m.end(1):]

    # Add Open Graph article metadata, idempotently.
    text = re.sub(r'\n?<meta\s+property=["\']article:(published_time|modified_time|section)["\'][^>]*>', '', text, flags=re.I)
    og_marker = '<meta property="og:type" content="article">'
    if og_marker in text:
        extra = (og_marker + '\n'
                 f'<meta property="article:published_time" content="{published}">\n'
                 f'<meta property="article:modified_time" content="{max(published, TODAY)}">\n'
                 f'<meta property="article:section" content="{section}">')
        text = text.replace(og_marker, extra, 1)

    p.write_text(text, encoding='utf-8')
    updated += 1

print(f'UPDATED_BLOGPOSTING {updated}')
print(f'MISSING_PUBLISHED_DATES {len(missing_dates)}')
for x in missing_dates:
    print(' ', x)

# Validation pass.
errors = []
for p in files:
    text = p.read_text(encoding='utf-8')
    m = re.search(r'<script\s+id=["\']site-structured-data["\']\s+type=["\']application/ld\+json["\']>(.*?)</script>', text, re.I | re.S)
    if not m:
        continue
    try:
        data = json.loads(m.group(1))
    except Exception as e:
        errors.append((p.as_posix(), f'JSON: {e}'))
        continue
    posting = next((x for x in data.get('@graph', []) if isinstance(x, dict) and x.get('@type') == 'BlogPosting'), None)
    if not posting:
        errors.append((p.as_posix(), 'missing BlogPosting'))
        continue
    required = ['datePublished','dateModified','articleSection','genre','image']
    absent = [k for k in required if not posting.get(k)]
    if absent:
        errors.append((p.as_posix(), 'missing '+','.join(absent)))

print(f'VALIDATION_ERRORS {len(errors)}')
for x in errors:
    print(' ', x)
if errors or missing_dates:
    raise SystemExit(1)
