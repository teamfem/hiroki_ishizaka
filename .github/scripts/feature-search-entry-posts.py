from pathlib import Path
import re

BLOG = Path('blog/index.html')
html = BLOG.read_text(encoding='utf-8')

# Add a Start here tab.
if 'href="#start-here"' not in html:
    html = html.replace('<div class="blog-tabs">', '<div class="blog-tabs"><a href="#start-here">Start here</a>', 1)

# Add styles for the search-entry section.
style_anchor = '@media(max-width:980px)'
if '.entry-grid{' not in html and style_anchor in html:
    styles = '''.entry-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.entry-card{display:block;background:#fff;border:1px solid var(--line);border-radius:20px;padding:22px;transition:.2s ease}.entry-card:hover{box-shadow:0 12px 30px rgba(20,32,51,.07);transform:translateY(-1px)}.entry-card .entry-label{display:block;font-size:.7rem;font-weight:850;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);margin-bottom:8px}.entry-card h3{font-size:1.05rem;line-height:1.42;margin:0 0 9px}.entry-card p{font-size:.84rem;color:var(--muted);margin:0}.entry-card.feature{border-color:#cbd9e8;background:linear-gradient(180deg,#fff,#f8fbfe)}\n'''
    html = html.replace(style_anchor, styles + style_anchor, 1)
    html = html.replace('@media(max-width:700px){', '@media(max-width:700px){.entry-grid{grid-template-columns:1fr}', 1)

# Insert a curated search-entry section before the existing research routes.
if 'id="start-here"' not in html:
    marker = '<section id="research-routes"'
    section = '''<section id="start-here" class="section"><div class="shell"><div class="section-head"><div><div class="kicker">Start here</div><h2>Six entry points into anisotropic finite-element geometry.</h2></div><p>These notes answer distinct questions that frequently arise before the technical error analysis begins: why mesh geometry matters, what can fail, how regularity conditions differ, and how layer-adapted meshes fit the picture.</p></div><div class="entry-grid">
<a class="entry-card feature" href="./posts/anisotropic-geometry-01.html"><span class="entry-label">Mesh geometry</span><h3>有限要素法ではなぜメッシュの幾何条件が必要なのか</h3><p>Start with the role of element geometry in interpolation, stability and convergence.</p></a>
<a class="entry-card feature" href="./posts/paradoxes-pitfalls-02.html"><span class="entry-label">Maximum-angle condition</span><h3>有限要素解は収束しているのに正解へ収束しない ――最大角条件とBabuška–Aziz反例</h3><p>A counterexample showing why apparent numerical convergence is not enough.</p></a>
<a class="entry-card" href="./posts/anisotropic-geometry-02.html"><span class="entry-label">Semi-regularity</span><h3>正則性と準正則性を角度を使わずに表す</h3><p>Compare regularity assumptions through computable geometric parameters.</p></a>
<a class="entry-card" href="./posts/anisotropic-geometry-05.html"><span class="entry-label">Mesh terminology</span><h3>graded mesh，quasi-uniformity，shape regularityの違い</h3><p>Separate local grading, global mesh-size balance and element-shape quality.</p></a>
<a class="entry-card" href="./posts/anisotropic-geometry-07.html"><span class="entry-label">Layer-adapted mesh</span><h3>Shishkin meshは正則か，準正則か</h3><p>Read Shishkin geometry through anisotropy, transition points and semi-regularity.</p></a>
<a class="entry-card" href="./posts/paradoxes-pitfalls-01.html"><span class="entry-label">Geometric approximation</span><h3>領域が収束しても解は正しく収束しない ――バブシュカ・パラドックス</h3><p>A geometric paradox explaining why convergence of domains need not imply convergence of solutions.</p></a>
</div></div></section>\n'''
    html = html.replace(marker, section + marker, 1)

BLOG.write_text(html, encoding='utf-8')

# Tailor descriptions for the six main search-entry notes.
descriptions = {
    'blog/posts/anisotropic-geometry-01.html': '有限要素法の誤差解析でメッシュの幾何条件が必要になる理由を，shape regularity，最大角条件，異方性メッシュ，補間誤差の観点から整理します．',
    'blog/posts/paradoxes-pitfalls-02.html': '最大角条件を破る三角形分割で，有限要素解が見かけ上収束しても真の解へ収束しないBabuška–Aziz反例を解説します．',
    'blog/posts/anisotropic-geometry-02.html': 'shape regularityとsemi-regularityを角度ではなく幾何パラメータで捉え，異方性有限要素解析で何を仮定すべきかを整理します．',
    'blog/posts/anisotropic-geometry-05.html': 'graded mesh，quasi-uniform mesh，shape-regular meshの違いを整理し，局所細分化と要素形状の品質を混同しないための基準を解説します．',
    'blog/posts/anisotropic-geometry-07.html': 'Shishkin meshを正則性・準正則性・異方性の観点から調べ，遷移点と細長い三角形要素が有限要素誤差解析にどう関係するかを解説します．',
    'blog/posts/paradoxes-pitfalls-01.html': '曲面領域を多角形で近似するとき，領域が収束しても有限要素解が正しい極限へ収束しないBabuška paradoxの仕組みを解説します．',
}

for path, new_desc in descriptions.items():
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']\s*/?>', text, flags=re.I)
    if not m:
        raise RuntimeError(f'description meta not found: {path}')
    old = m.group(1)
    text = text.replace(old, new_desc)
    p.write_text(text, encoding='utf-8')

print('Featured six search-entry posts and tailored their descriptions.')
