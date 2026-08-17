from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Add lightweight bilingual styling to the existing homepage-only style block.
marker='.archive-note{color:var(--muted);font-size:.82rem;margin:8px 0 0}'
addition='''.archive-note{color:var(--muted);font-size:.82rem;margin:8px 0 0}.hero-ja{margin:14px 0 0;font-size:clamp(1rem,2vw,1.22rem);font-weight:650;letter-spacing:.04em;color:#52657b}.programme-ja{margin:-2px 0 14px!important;font-size:.9rem!important;font-weight:720;color:#52657b!important;letter-spacing:.025em}.programme.p2 .programme-ja{color:#d8d0ec!important}.route-ja{display:block;margin-top:4px;font-size:.76rem;font-weight:700;color:#607086;letter-spacing:.02em}'''
if '.hero-ja{' not in s:
    if marker not in s: raise RuntimeError('homepage style marker not found')
    s=s.replace(marker,addition,1)

old='<h1>Mathematics makes<br><span>the invisible visible.</span></h1><p class="lead">'
new='<h1>Mathematics makes<br><span>the invisible visible.</span></h1><p class="hero-ja" lang="ja">数学は見えないものを可視化する</p><p class="lead">'
if 'class="hero-ja"' not in s:
    if old not in s: raise RuntimeError('hero marker not found')
    s=s.replace(old,new,1)

old='<h3>Certified finite element analysis under computable geometric conditions</h3><p>Making discretisation error'
new='<h3>Certified finite element analysis under computable geometric conditions</h3><p class="programme-ja" lang="ja">計算可能な幾何条件の下での認証付き有限要素解析</p><p>Making discretisation error'
if '計算可能な幾何条件の下での認証付き有限要素解析' not in s:
    if old not in s: raise RuntimeError('Programme I marker not found')
    s=s.replace(old,new,1)

old='<h3>Stable reduction theory for unresolved dynamics</h3><p>Eliminating variables'
new='<h3>Stable reduction theory for unresolved dynamics</h3><p class="programme-ja" lang="ja">未解像ダイナミクスの安定縮約理論</p><p>Eliminating variables'
if '未解像ダイナミクスの安定縮約理論' not in s:
    if old not in s: raise RuntimeError('Programme II marker not found')
    s=s.replace(old,new,1)

# Add Japanese labels to the three active research routes as well, without changing
# the English search-facing titles.
repls=[
('<b>Anisotropic FEM &amp; mesh geometry</b><span>','<b>Anisotropic FEM &amp; mesh geometry</b><small class="route-ja" lang="ja">異方性有限要素法とメッシュ幾何</small><span>'),
('<b>Stable reduction &amp; unresolved dynamics</b><span>','<b>Stable reduction &amp; unresolved dynamics</b><small class="route-ja" lang="ja">未解像ダイナミクスの安定縮約理論</small><span>'),
('<b>Exact-curved FEM</b><span>','<b>Exact-curved FEM</b><small class="route-ja" lang="ja">厳密曲線領域上の有限要素法</small><span>'),
]
for old,new in repls:
    if new not in s:
        if old not in s: raise RuntimeError(f'route marker not found: {old}')
        s=s.replace(old,new,1)

# Add Japanese search terms without replacing the English metadata.
old_kw='Unresolved Dynamics,Stable Reduction,Memory Equations,Latent States,Numerical Analysis,PDE'
new_kw='Unresolved Dynamics,Stable Reduction,未解像ダイナミクス,安定縮約理論,Memory Equations,Latent States,Numerical Analysis,PDE'
if new_kw not in s:
    if old_kw not in s: raise RuntimeError('keyword marker not found')
    s=s.replace(old_kw,new_kw,1)

p.write_text(s,encoding='utf-8')

# Validation.
t=p.read_text(encoding='utf-8')
for phrase in (
    '数学は見えないものを可視化する',
    '計算可能な幾何条件の下での認証付き有限要素解析',
    '未解像ダイナミクスの安定縮約理論',
    '異方性有限要素法とメッシュ幾何',
    '厳密曲線領域上の有限要素法',
):
    if phrase not in t: raise RuntimeError(f'missing Japanese phrase: {phrase}')
if t.count('class="hero-ja"') != 1: raise RuntimeError('hero Japanese subtitle count is not one')
print('Homepage Japanese subtitles added and validated.')
