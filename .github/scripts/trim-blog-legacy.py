from pathlib import Path
import re

u = Path('js/utility.js')
text = u.read_text(encoding='utf-8')
if 'if(window.jQuery){\n  jQuery.noConflict();' not in text:
    old = 'jQuery.noConflict();\n(function($) {'
    new = 'if(window.jQuery){\n  jQuery.noConflict();\n(function($) {'
    if old not in text:
        raise SystemExit('utility.js opening marker not found')
    text = text.replace(old, new, 1)
    old_end = '})(jQuery);\n\n/* Modern Blog post shell'
    new_end = '})(jQuery);\n}\n\n/* Modern Blog post shell'
    if old_end not in text:
        raise SystemExit('utility.js closing marker not found')
    text = text.replace(old_end, new_end, 1)
    u.write_text(text, encoding='utf-8')
    print('Guarded legacy jQuery UI in utility.js')
else:
    print('utility.js already guarded')

pattern = re.compile(r'\s*<script\s+src=["\'][^"\']*js/(?:jquery|jquery-migrate)\.js["\'][^>]*></script>\s*', re.I)
changed = 0
removed = 0
for p in sorted(Path('blog/posts').glob('*.html')):
    s = p.read_text(encoding='utf-8')
    ns, n = pattern.subn('\n', s)
    if n:
        p.write_text(ns, encoding='utf-8')
        changed += 1
        removed += n
print(f'Removed {removed} legacy jQuery script tags from {changed} Blog posts')

# Validation: modern Blog posts must still load utility.js.
posts = list(Path('blog/posts').glob('*.html'))
missing = [str(p) for p in posts if 'js/utility.js' not in p.read_text(encoding='utf-8')]
if missing:
    raise SystemExit('Posts missing utility.js: ' + ', '.join(missing[:10]))
print(f'Validated utility.js on {len(posts)} Blog post files')
