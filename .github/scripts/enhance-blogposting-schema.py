from pathlib import Path
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


MONTHS = {
    'january': 1, 'february': 2, 'march': 3, 'april': 4,
    'may': 5, 'june': 6, 'july': 7, 'august': 8,
    'september': 9, 'october': 10, 'november': 11, 'december': 12,
    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'jun': 6, 'jul': 7,
    'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
}


def english_date(s: str):
    m = re.search(
        r'\b(\d{1,2})(?:st|nd|rd|th)?\s+'
        r'(January|February|March|April|May|June|July|August|September|October|November|December|'
        r'Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(20\d{2})\b',
        s, re.I
    )
    if not m:
        return None
    month = MONTHS[m.group(2).lower()]
    return f'{m.group(3)}-{month:02d}-{int(m.group(1)):02d}'


def filename_date(name: str):
    # Legacy article filenames such as article15apr26.html.
    m = re.match(r'article(\d{2})([a-z]{3})(\d{2})', name, re.I)
    if not m:
        return None
    mon = MONTHS.get(m.group(2).lower())
    if not mon:
        return None
    return f'20{m.group(3)}-{mon:02d}-{int(m.group(1)):02d}'


def published_date(text: str, name: str):
    # Preferred machine-readable source.
    tm = re.search(r'<time\b[^>]*\bdatetime=["\'](\d{4}-\d{2}-\d{2})["\']', text, re.I)
    if tm:
        return tm.group(1)

    # Older templates often store the publication date in the breadcrumb.
    m = re.search(r'Blog post from\s+([^<\n]+)', text, re.I)
    if m:
        d = english_date(m.group(1))
        if d:
            return d

    # Some series put the date immediately under the H1 instead of using <time>.
    h1 = re.search(r'<h1\b[^>]*class=["\'][^"\']*section-title[^"\']*["\'][^>]*>.*?</h1>', text, re.I | re.S)
    if h1:
        nearby = text[h1.end():h1.end() + 1400]
        d = english_date(nearby)
        if d:
            return d

    return filename_date(name)


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

    published = published_date(text, p.name)
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
validated = 0
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
    else:
        validated += 1

print(f'VALIDATED_BLOGPOSTING {validated}')
print(f'VALIDATION_ERRORS {len(errors)}')
for x in errors:
    print(' ', x)
if errors or missing_dates:
    raise SystemExit(1)
