from pathlib import Path

p = Path('publications/index.html')
s = p.read_text(encoding='utf-8')

arxiv = 'https://arxiv.org/abs/2608.15262'
wrong_s7 = f'''<article class="pub"><div class="pub-top"><div><span class="pub-id">[S7]</span><h3>Certified Space–Time Enclosures for a Semilinear Parabolic Problem via CR–RT Elliptic Reconstruction</h3><div class="pub-meta"><b>H. Ishizaka*</b></div></div><span class="status">Preprint</span></div><div class="pub-links"><a href="{arxiv}">arXiv</a></div></article>\n'''
if wrong_s7 in s:
    s = s.replace(wrong_s7, '', 1)

mp5 = '<article class="pipe"><span class="code">MP5</span><h3>In preparation</h3><p>Working manuscript; title not yet fixed.</p></article>'
mp4 = '<article class="pipe dark"><span class="code">MP4</span><h3>Stable reduction of coupled diffusion systems to equations with memory</h3><p>Concrete PDE development of the stable-reduction programme.</p></article>'
if mp5 not in s:
    if mp4 not in s:
        raise RuntimeError('MP4 anchor not found')
    s = s.replace(mp4, mp5 + mp4, 1)

n3_old = '<article class="pub"><div class="pub-top"><div><span class="pub-id">[N3]</span><h3>Stable Reduction of Unresolved Dynamics: An Operator-Theoretic Framework</h3><div class="pub-meta"><b>H. Ishizaka</b></div></div><span class="status">Research note</span></div></article>'
n3_new = f'<article class="pub"><div class="pub-top"><div><span class="pub-id">[N3]</span><h3>Stable Reduction of Unresolved Dynamics: An Operator-Theoretic Framework</h3><div class="pub-meta"><b>H. Ishizaka</b></div></div><span class="status">Research note</span></div><div class="pub-links"><a href="{arxiv}">arXiv</a></div></article>'
if n3_old in s:
    s = s.replace(n3_old, n3_new, 1)
elif n3_new not in s:
    raise RuntimeError('N3 entry not found')

p.write_text(s, encoding='utf-8')

r = p.read_text(encoding='utf-8')
assert r.count(arxiv) == 1, r.count(arxiv)
assert '[S7]' not in r
assert n3_new in r
assert mp5 in r
print('Corrected arXiv 2608.15262: linked only from N3; restored MP5; removed erroneous S7.')
