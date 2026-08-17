from pathlib import Path
import re

ROOT='https://teamfem.github.io/hiroki_ishizaka'

def extract_section(src):
    markers=['<div class="section-in">', "<div class='section-in'>"]
    start=-1
    marker=''
    for m in markers:
        start=src.find(m)
        if start>=0:
            marker=m
            break
    if start<0:
        raise RuntimeError('section-in start not found')
    start += len(marker)
    ends=['</div><!--section-in-->', '</div><!-- section-in -->', '<!--section-in-->']
    end=-1
    for e in ends:
        p=src.find(e,start)
        if p>=0:
            end=p
            break
    if end<0:
        # Fallback: stop before the old main/footer closing area.
        candidates=[src.find('</main>',start),src.find('<!--▲メインコンテンツ-->',start),src.find('<footer',start)]
        candidates=[p for p in candidates if p>=0]
        if not candidates:
            raise RuntimeError('section-in end not found')
        end=min(candidates)
    body=src[start:end]
    body=re.sub(r'<h1[^>]*>.*?</h1>','',body,count=1,flags=re.S|re.I)
    body=re.sub(r'<script\b[^>]*>.*?</script>','',body,flags=re.S|re.I)
    return body.strip()

def make_page(kind,title,dek,canonical,back_href,back_label,body):
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Hiroki Ishizaka</title>
<meta name="description" content="{dek}">
<link rel="canonical" href="{canonical}">
<link rel="stylesheet" href="../css/modern.css">
<link rel="icon" href="../favicon.ico">
<script>window.MathJax={{tex:{{inlineMath:[["\\\\(","\\\\)"]],displayMath:[["\\\\[","\\\\]"]]}}}};</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>
.detail-archive{{max-width:920px;margin:0 auto}}.detail-archive h2{{font-size:1.75rem;margin:2.2em 0 .7em;letter-spacing:-.03em}}.detail-archive h3{{font-size:1.25rem;margin:1.8em 0 .65em;letter-spacing:-.02em}}.detail-archive h4{{font-size:1.08rem;margin:1.5em 0 .55em}}.detail-archive p,.detail-archive li{{line-height:1.8;color:#35495f}}.detail-archive ul,.detail-archive ol{{padding-left:1.4em}}.detail-archive a{{color:var(--accent);text-decoration:underline;text-underline-offset:.14em}}.detail-archive table{{display:block;max-width:100%;overflow-x:auto;border-collapse:collapse}}.detail-archive th,.detail-archive td{{border:1px solid var(--line);padding:9px 10px;vertical-align:top}}.detail-archive hr{{border:0;border-top:1px solid var(--line);margin:1.7em 0}}.detail-archive mjx-container[display="true"]{{overflow-x:auto;overflow-y:hidden;padding:.25em 0}}.archive-notice{{padding:15px 17px;border:1px solid var(--line);border-radius:14px;background:var(--soft);color:var(--muted);font-size:.88rem;margin-bottom:28px}}
</style>
</head>
<body>
<header class="topbar"><div class="shell nav"><a class="brand" href="../">Hiroki Ishizaka<small>Numerical Analysis · PDEs · FEM</small></a><nav class="navlinks" aria-label="Primary navigation"><a href="../research/">Research</a><a href="../publications/">Publications</a><a href="../fem/">Visions</a><a href="../blog/">Blog</a><a href="../links/">Links</a></nav></div></header>
<main>
<section class="page-hero"><div class="shell"><div class="eyebrow"><span class="dot"></span>{kind}</div><h1>{title}</h1><p>{dek}</p><div class="actions" style="margin-top:22px"><a class="btn primary" href="{back_href}">{back_label}</a></div></div></section>
<section class="section"><div class="shell"><article class="detail-archive"><div class="archive-notice">This static archive exposes the full detailed material directly in HTML for reading, citation and search. The modern overview remains the recommended entry point.</div>
{body}
</article></div></section>
</main>
<footer class="footer"><div class="shell footer-inner"><span>© 2026 Hiroki Ishizaka</span><span>{kind}</span></div></footer>
<script src="../js/modern-ui.js"></script>
</body>
</html>
'''

fem_src=Path('fem/vision-details.txt').read_text(encoding='utf-8')
sup_src=Path('suppl/syllabus-details.txt').read_text(encoding='utf-8')
Path('fem/details.html').write_text(make_page('Research Visions','Detailed Research Visions','Full detailed research visions on anisotropic FEM, computable geometry, stable reduction, memory equations, exact-curved geometry, certification and related open problems.',ROOT+'/fem/details.html','./','Back to Research Visions',extract_section(fem_src)),encoding='utf-8')
Path('suppl/details.html').write_text(make_page('Supplementary Visions','Detailed Learning Maps','Full detailed learning maps and syllabi connecting finite element analysis, PDE theory, anisotropic geometry, de Rham complexes, memory equations and certified computation.',ROOT+'/suppl/details.html','./','Back to Supplementary Visions',extract_section(sup_src)),encoding='utf-8')

# Add direct crawlable links to the modern overview pages.
fem=Path('fem/index.html').read_text(encoding='utf-8')
needle='<a href="../publications/">Current manuscripts</a>'
if './details.html' not in fem and needle in fem:
    fem=fem.replace(needle,needle+'<a href="./details.html">Detailed archive</a>',1)
Path('fem/index.html').write_text(fem,encoding='utf-8')

sup=Path('suppl/index.html').read_text(encoding='utf-8')
hero='</div></div></section>\n<section class="section"><div class="shell"><div class="section-head"><div><div class="kicker">Recommended routes</div>'
if './details.html' not in sup and hero in sup:
    replacement='<div class="actions" style="margin-top:22px"><a class="btn" href="./details.html">Detailed learning-map archive</a></div></div></div></section>\n<section class="section"><div class="shell"><div class="section-head"><div><div class="kicker">Recommended routes</div>'
    sup=sup.replace(hero,replacement,1)
Path('suppl/index.html').write_text(sup,encoding='utf-8')

site=Path('sitemap.xml').read_text(encoding='utf-8')
new_urls=[ROOT+'/fem/details.html',ROOT+'/suppl/details.html']
insert=''
for u in new_urls:
    if u not in site:
        insert += f'\n  <url>\n    <loc>{u}</loc>\n  </url>\n'
if insert:
    site=site.replace('\n</urlset>',insert+'\n</urlset>')
Path('sitemap.xml').write_text(site,encoding='utf-8')
print('Static detail pages generated and linked.')