from pathlib import Path
import re

ROOT = Path('.')
ITEMS = [
    ('research/', 'Research', 'research'),
    ('publications/', 'Publications', 'publications'),
    ('fem/', 'Visions', 'fem'),
    ('suppl/', 'Supplementary', 'suppl'),
    ('blog/', 'Blog', 'blog'),
    ('geo/', 'Geometry', 'geo'),
    ('links/', 'Links', 'links'),
    ('contact/', 'Contact', 'contact'),
]


def prefix_for(path: Path) -> str:
    depth = len(path.parent.parts)
    return './' if depth == 0 else '../' * depth


def current_section(path: Path):
    parts = path.parts
    if not parts:
        return None
    first = parts[0]
    if first in {x[2] for x in ITEMS}:
        return first
    return None


def modern_nav(path: Path) -> str:
    prefix = prefix_for(path)
    current = current_section(path)
    links = []
    for href, label, key in ITEMS:
        cur = ' aria-current="page"' if current == key else ''
        links.append(f'<a href="{prefix}{href}"{cur}>{label}</a>')
    return '<nav class="navlinks" aria-label="Primary navigation">' + ''.join(links) + '</nav>'


def legacy_blog_menu() -> str:
    links = [
        ('../../research/', 'Research'),
        ('../../publications/', 'Publications'),
        ('../../fem/', 'Visions'),
        ('../../suppl/', 'Supplementary'),
        ('../../blog/', 'Blog'),
        ('../../geo/', 'Geometry'),
        ('../../links/', 'Links'),
        ('../../contact/', 'Contact'),
    ]
    body = '\n'.join(f'\t\t\t\t<li><a href="{href}">{label}</a></li>' for href, label in links)
    return '<ul id="menu">\n' + body + '\n\t\t\t</ul>'

html_changed = 0
modern_pages = 0
blog_posts = 0

for path in sorted(ROOT.rglob('*.html')):
    if '.github' in path.parts:
        continue
    text = path.read_text(encoding='utf-8')
    original = text

    if '<nav class="navlinks" aria-label="Primary navigation">' in text:
        text, n = re.subn(
            r'<nav class="navlinks" aria-label="Primary navigation">.*?</nav>',
            modern_nav(path),
            text,
            count=1,
            flags=re.S,
        )
        if n != 1:
            raise RuntimeError(f'Could not normalise modern nav in {path}')
        modern_pages += 1

    if path.parts[:2] == ('blog', 'posts'):
        text, n = re.subn(r'<ul id="menu">.*?</ul>', legacy_blog_menu(), text, count=1, flags=re.S)
        if n != 1:
            raise RuntimeError(f'Could not normalise static Blog menu in {path}')
        blog_posts += 1

    if text != original:
        path.write_text(text, encoding='utf-8')
        html_changed += 1

# Make the modern Blog runtime shell itself contain the same eight static links.
utility = Path('js/utility.js')
u = utility.read_text(encoding='utf-8')
old_runtime = '<nav class="navlinks" aria-label="Primary navigation"><a href="../../research/">Research</a><a href="../../publications/">Publications</a><a href="../../fem/">Visions</a><a href="../">Blog</a><a href="../../links/">Links</a></nav>'
new_runtime = '<nav class="navlinks" aria-label="Primary navigation"><a href="../../research/">Research</a><a href="../../publications/">Publications</a><a href="../../fem/">Visions</a><a href="../../suppl/">Supplementary</a><a href="../../blog/" aria-current="page">Blog</a><a href="../../geo/">Geometry</a><a href="../../links/">Links</a><a href="../../contact/">Contact</a></nav>'
if old_runtime in u:
    u = u.replace(old_runtime, new_runtime, 1)
elif new_runtime not in u:
    raise RuntimeError('Blog runtime navigation marker not found in js/utility.js')
utility.write_text(u, encoding='utf-8')

# modern-ui becomes progressive enhancement: preserve a complete static nav,
# only rebuild as a fallback for an unexpectedly incomplete page.
ui = Path('js/modern-ui.js')
m = ui.read_text(encoding='utf-8')
start = m.find('  function ensurePrimaryNavigation(){')
end = m.find('\n\n  function initBackToTop(){', start)
if start < 0 or end < 0:
    raise RuntimeError('ensurePrimaryNavigation block not found')
new_function = '''  function ensurePrimaryNavigation(){
    var desktop=document.querySelector('.topbar .navlinks');
    if(!desktop) return;

    var base='/hiroki_ishizaka/';
    var items=[
      {href:base+'research/',label:'Research'},
      {href:base+'publications/',label:'Publications'},
      {href:base+'fem/',label:'Visions'},
      {href:base+'suppl/',label:'Supplementary'},
      {href:base+'blog/',label:'Blog'},
      {href:base+'geo/',label:'Geometry'},
      {href:base+'links/',label:'Links'},
      {href:base+'contact/',label:'Contact'}
    ];
    var links=desktop.querySelectorAll('a');

    // Static HTML is the source of truth. Rebuild only as a fallback if a
    // future page is unexpectedly missing navigation entries.
    if(links.length<items.length){
      desktop.textContent='';
      items.forEach(function(item){
        var link=document.createElement('a');
        link.href=item.href;
        link.textContent=item.label;
        desktop.appendChild(link);
      });
      links=desktop.querySelectorAll('a');
    }

    var path=window.location.pathname;
    links.forEach(function(link){
      link.removeAttribute('aria-current');
      try{
        var target=new URL(link.href,window.location.href).pathname;
        if(target!==base && path.indexOf(target)===0) link.setAttribute('aria-current','page');
      }catch(e){}
    });
  }'''
m = m[:start] + new_function + m[end:]
ui.write_text(m, encoding='utf-8')

# Validation: every modern static nav has exactly 8 links and all 8 targets.
expected_keys = [x[0] for x in ITEMS]
for path in sorted(ROOT.rglob('*.html')):
    if '.github' in path.parts:
        continue
    text = path.read_text(encoding='utf-8')
    match = re.search(r'<nav class="navlinks" aria-label="Primary navigation">(.*?)</nav>', text, re.S)
    if match:
        block = match.group(1)
        if block.count('<a ') != 8:
            raise RuntimeError(f'{path}: static modern nav does not have 8 links')
        pref = prefix_for(path)
        for href in expected_keys:
            if f'href="{pref}{href}"' not in block:
                raise RuntimeError(f'{path}: missing static nav target {pref}{href}')

for path in sorted(Path('blog/posts').glob('*.html')):
    text = path.read_text(encoding='utf-8')
    match = re.search(r'<ul id="menu">(.*?)</ul>', text, re.S)
    if not match or match.group(1).count('<li>') != 8:
        raise RuntimeError(f'{path}: Blog source menu does not have 8 items')
    for href, _ in [
        ('../../research/', ''), ('../../publications/', ''), ('../../fem/', ''),
        ('../../suppl/', ''), ('../../blog/', ''), ('../../geo/', ''),
        ('../../links/', ''), ('../../contact/', ''),
    ]:
        if f'href="{href}"' not in match.group(1):
            raise RuntimeError(f'{path}: missing Blog source nav target {href}')

ucheck = utility.read_text(encoding='utf-8')
for href in ('../../research/','../../publications/','../../fem/','../../suppl/','../../blog/','../../geo/','../../links/','../../contact/'):
    if href not in ucheck:
        raise RuntimeError(f'js/utility.js missing runtime nav target {href}')

mcheck = ui.read_text(encoding='utf-8')
if "if(links.length<items.length)" not in mcheck:
    raise RuntimeError('modern-ui.js is not preserving complete static navigation')

print(f'HTML files changed: {html_changed}')
print(f'Modern nav pages validated: {modern_pages}')
print(f'Blog post source menus validated: {blog_posts}')
print('Static eight-tab navigation validated site-wide.')
