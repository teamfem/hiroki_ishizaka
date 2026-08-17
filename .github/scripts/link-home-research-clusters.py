from pathlib import Path

# Home: add three direct research-entry routes before the profile/about section.
home_path = Path('index.html')
home = home_path.read_text(encoding='utf-8')
if 'id="research-entry-routes"' not in home:
    marker = '<section class="section"><div class="shell grid"><article class="panel about">'
    if marker not in home:
        raise RuntimeError('Home insertion marker not found')
    block = '''<section id="research-entry-routes" class="section"><div class="shell"><div class="section-head"><div><div class="kicker">Research entry routes</div><h2>Start from three active research themes.</h2></div><p>Each route begins with explanatory research notes and continues to formal results, current manuscripts and longer-term research visions.</p></div><div class="quick"><a href="./blog/#start-here"><b>Anisotropic FEM &amp; mesh geometry</b><span>Mesh conditions, maximum-angle phenomena, semi-regularity, graded meshes and Shishkin meshes</span></a><a href="./blog/#memory-start"><b>Stable reduction &amp; unresolved dynamics</b><span>Hidden-state elimination, memory, measure-valued delay, coercivity, convolution quadrature and reduction error</span></a><a href="./blog/#curved-start"><b>Exact-curved FEM</b><span>Curved domains, affine-core decomposition, geometry order, FEniCSx/UFL and comparison with isoparametric FEM</span></a></div></div></section>'''
    home = home.replace(marker, block + marker, 1)
home_path.write_text(home, encoding='utf-8')

# Research: replace the older theme-route block with explicit three-cluster routes plus formal continuations.
research_path = Path('research/index.html')
research = research_path.read_text(encoding='utf-8')
start = research.find('<section id="theme-routes" class="section">')
end = research.find('<section id="detailed-research-map" class="section">', start)
if start < 0 or end < 0:
    raise RuntimeError('Research theme-routes block not found')
new_block = '''<section id="theme-routes" class="section"><div class="shell"><div class="section-head"><div><div class="kicker">Follow a research theme</div><h2>Three routes from notes to formal research.</h2></div><p>These routes connect explanatory Blog entries directly to peer-reviewed results, current manuscripts and the corresponding Research Visions.</p></div><div class="quick"><a href="../blog/#start-here"><b>Anisotropic FEM &amp; mesh geometry</b><span>Begin with mesh geometry, maximum-angle phenomena, semi-regularity, graded meshes and layer-adapted meshes</span></a><a href="../blog/#memory-start"><b>Stable reduction &amp; unresolved dynamics</b><span>Begin with hidden-state elimination, memory and delay, then proceed to energy structure, CQ and reduction error</span></a><a href="../blog/#curved-start"><b>Exact-curved FEM</b><span>Begin with curved-domain geometry, affine-core decomposition, implementation and comparison with isoparametric FEM</span></a><a href="../publications/#journals"><b>Peer-reviewed FEM results</b><span>Formal results on geometric conditions, interpolation, CR–RT, Morley, Nitsche, DG and discrete inequalities</span></a><a href="../publications/#preprints"><b>Current manuscripts and preprints</b><span>Memory and delay, certified computation, spherical mesh geometry and exact-curved finite elements</span></a><a href="../fem/#vision20"><b>Vision 20 · CR–RT / DMP / maximum norm</b><span>Pointwise structure beyond interpolation estimates</span></a><a href="../fem/#vision18"><b>Vision 18 · Stable reduction</b><span>Unresolved dynamics as an operator-theoretic reduction programme</span></a><a href="../fem/#vision10"><b>Vision 10 · Exact-curved geometry</b><span>Curved CR–RT, shape analysis, ALE and geometry-aware finite elements</span></a><a href="../geo/"><b>History of geometric conditions in FEM</b><span>From classical angle conditions to computable anisotropic geometry</span></a></div></div></section>\n'''
research = research[:start] + new_block + research[end:]

# Add a direct Blog-route button to the stable-reduction focus without duplicating it.
needle = '<a class="btn" style="margin-top:8px" href="../fem/#vision18">Research Vision 18</a>'
replacement = needle + '<a class="btn" style="margin-top:8px;margin-left:8px" href="../blog/#memory-start">Read the Blog entry route</a>'
if 'href="../blog/#memory-start">Read the Blog entry route</a>' not in research:
    if needle not in research:
        raise RuntimeError('Stable-reduction button marker not found')
    research = research.replace(needle, replacement, 1)
research_path.write_text(research, encoding='utf-8')

# Validation.
home_check = home_path.read_text(encoding='utf-8')
research_check = research_path.read_text(encoding='utf-8')
assert home_check.count('id="research-entry-routes"') == 1
for anchor in ('./blog/#start-here','./blog/#memory-start','./blog/#curved-start'):
    assert anchor in home_check
for anchor in ('../blog/#start-here','../blog/#memory-start','../blog/#curved-start'):
    assert anchor in research_check
assert research_check.count('id="theme-routes"') == 1
print('Home and Research cluster links prepared and validated.')
