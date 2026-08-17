from pathlib import Path

# Publications: replace the older theme route with the three current Blog entry clusters.
pub_path = Path('publications/index.html')
pub = pub_path.read_text(encoding='utf-8')
start = pub.find('<section id="theme-routes" class="section">')
end = pub.find('<section id="pipeline" class="section">', start)
if start < 0 or end < 0:
    raise RuntimeError('Publications theme-routes block not found')
new_pub = '''<section id="theme-routes" class="section"><div class="shell"><div class="section-head"><div><div class="kicker">Follow the research themes</div><h2>From formal results back to the explanatory routes.</h2></div><p>The publication list records formal results. These routes connect the main strands to explanatory Blog notes and then onward to the corresponding Research Visions.</p></div><div class="quick"><a href="../blog/#start-here"><b>Anisotropic FEM &amp; mesh geometry</b><span>Mesh conditions, maximum-angle phenomena, semi-regularity, graded meshes and Shishkin meshes behind the published FEM results</span></a><a href="../blog/#memory-start"><b>Stable reduction &amp; unresolved dynamics</b><span>Hidden-state elimination, memory and delay, coercivity, convolution quadrature and model-reduction error</span></a><a href="../blog/#curved-start"><b>Exact-curved FEM</b><span>Curved-domain geometry, affine-core decomposition, geometry order, FEniCSx/UFL and isoparametric comparison</span></a><a href="../research/#fem-summary"><b>Research architecture</b><span>How the published interpolation, CR–RT, Morley, Nitsche, DG and certification results fit together</span></a><a href="../fem/#vision20"><b>Vision 20 · CR–RT / DMP / maximum norm</b><span>Next questions on monotonicity, pointwise bounds and connectivity</span></a><a href="../fem/#vision21"><b>Vision 21 · 3D de Rham / Maxwell</b><span>Extension from RT foundations to Nédélec, Hodge and Maxwell analysis</span></a><a href="../fem/#vision18"><b>Vision 18 · Stable reduction</b><span>Operator-theoretic reduction of unresolved dynamics</span></a><a href="../fem/#vision10"><b>Vision 10 · Exact-curved geometry</b><span>Curved CR–RT, shape differentiation, ALE and geometry-aware finite elements</span></a><a href="../fem/#vision17"><b>Vision 17 · Certification &amp; AI4Math</b><span>Verified output, formal reasoning and reusable mathematical certificates</span></a></div></div></section>\n'''
pub = pub[:start] + new_pub + pub[end:]
pub_path.write_text(pub, encoding='utf-8')

# Research Visions: update evidence routes to current Blog cluster anchors.
fem_path = Path('fem/index.html')
fem = fem_path.read_text(encoding='utf-8')
start = fem.find('<section id="evidence-routes" class="section">')
end = fem.find('<section id="visions" class="section">', start)
if start < 0 or end < 0:
    raise RuntimeError('Visions evidence-routes block not found')
new_fem = '''<section id="evidence-routes" class="section"><div class="shell"><div class="section-head"><div><div class="kicker">From vision to evidence</div><h2>Move between open questions, explanations and proved results.</h2></div><p>The Visions page describes future mathematical questions. These routes connect the three active programmes back to explanatory Blog notes and to the formal research record.</p></div><div class="quick"><a href="../blog/#start-here"><b>Anisotropic FEM &amp; mesh geometry</b><span>Explanatory route behind the geometric conditions, CR–RT and pointwise-analysis visions</span></a><a href="../blog/#memory-start"><b>Stable reduction &amp; unresolved dynamics</b><span>Explanatory route behind Visions 11 and 18, from exact elimination to full discretisation</span></a><a href="../blog/#curved-start"><b>Exact-curved FEM</b><span>Explanatory route behind Vision 10, from curved domains to implementation and method comparison</span></a><a href="../research/#fem-summary"><b>Established FEM foundations</b><span>Current mathematical architecture and completed strands</span></a><a href="../publications/#journals"><b>Peer-reviewed evidence</b><span>Published journal papers supporting the geometry and FEM programme</span></a><a href="../publications/#preprints"><b>Current public manuscripts</b><span>Memory, exact-curved geometry, certification and spherical-mesh preprints</span></a><a href="../research/#stable-reduction"><b>Stable-reduction programme</b><span>Research architecture behind Vision 18</span></a><a href="../blog/#certified"><b>Certification notes</b><span>Public notes supporting Vision 17</span></a></div></div></section>\n'''
fem = fem[:start] + new_fem + fem[end:]

# Add direct Blog entry links on the three matching Core cards.
replacements = [
    ('<span class="vision-ref">Vision 20</span></article>', '<span class="vision-ref">Vision 20</span><br><a class="vision-ref" href="../blog/#start-here">Read the anisotropic FEM entry route →</a></article>'),
    ('<span class="vision-ref">Visions 11 &amp; 18</span></article>', '<span class="vision-ref">Visions 11 &amp; 18</span><br><a class="vision-ref" href="../blog/#memory-start">Read the stable-reduction entry route →</a></article>'),
    ('<span class="vision-ref">Vision 10</span></article>', '<span class="vision-ref">Vision 10</span><br><a class="vision-ref" href="../blog/#curved-start">Read the Exact-curved FEM entry route →</a></article>'),
]
for old, new in replacements:
    if new not in fem:
        if old not in fem:
            raise RuntimeError(f'Core card marker not found: {old}')
        fem = fem.replace(old, new, 1)
fem_path.write_text(fem, encoding='utf-8')

# Validation.
pub_check = pub_path.read_text(encoding='utf-8')
fem_check = fem_path.read_text(encoding='utf-8')
for anchor in ('../blog/#start-here','../blog/#memory-start','../blog/#curved-start'):
    assert anchor in pub_check
    assert anchor in fem_check
assert pub_check.count('id="theme-routes"') == 1
assert fem_check.count('id="evidence-routes"') == 1
assert 'Read the anisotropic FEM entry route' in fem_check
assert 'Read the stable-reduction entry route' in fem_check
assert 'Read the Exact-curved FEM entry route' in fem_check
print('Publications and Research Visions reverse links prepared and validated.')
