from pathlib import Path

p = Path('publications/index.html')
s = p.read_text(encoding='utf-8')

arxiv = 'https://arxiv.org/abs/2608.15262'
title = 'Certified Space–Time Enclosures for a Semilinear Parabolic Problem via CR–RT Elliptic Reconstruction'

s7 = f'''<article class="pub"><div class="pub-top"><div><span class="pub-id">[S7]</span><h3>{title}</h3><div class="pub-meta"><b>H. Ishizaka*</b></div></div><span class="status">Preprint</span></div><div class="pub-links"><a href="{arxiv}">arXiv</a></div></article>\n'''

anchor = '<article class="pub"><div class="pub-top"><div><span class="pub-id">[S6]</span><h3>Exact characterisation of maximum-angle conditions for spherical finite element meshes</h3>'
if arxiv not in s:
    if anchor not in s:
        raise RuntimeError('S6 anchor not found')
    s = s.replace(anchor, s7 + anchor, 1)

mp5 = '<article class="pipe"><span class="code">MP5</span><h3>In preparation</h3><p>Working manuscript; title not yet fixed.</p></article>'
if mp5 in s:
    s = s.replace(mp5, '', 1)

p.write_text(s, encoding='utf-8')

# Validation
r = p.read_text(encoding='utf-8')
if r.count(arxiv) != 1:
    raise RuntimeError(f'arXiv link count is {r.count(arxiv)}, expected 1')
if r.count(title) != 1:
    raise RuntimeError(f'title count is {r.count(title)}, expected 1')
if '<span class="pub-id">[S7]</span>' not in r:
    raise RuntimeError('S7 entry missing')
if 'MP5</span><h3>In preparation</h3>' in r:
    raise RuntimeError('obsolete MP5 placeholder remains')
print('Added S7 arXiv entry and removed MP5 placeholder.')
