from pathlib import Path

p=Path('research/index.html')
text=p.read_text(encoding='utf-8')
if 'id="detailed-research-map"' in text:
    print('Detailed research map already present')
    raise SystemExit(0)

style='''
.research-matrix-wrap{overflow-x:auto;margin-top:18px}.research-matrix{width:100%;min-width:980px;border-collapse:separate;border-spacing:0;background:#fff;border:1px solid var(--line);border-radius:18px;overflow:hidden}.research-matrix th,.research-matrix td{padding:13px 14px;border-right:1px solid var(--line);border-bottom:1px solid var(--line);vertical-align:top;text-align:left;font-size:.82rem;line-height:1.5}.research-matrix th{background:var(--soft);font-weight:800}.research-matrix tr:last-child th,.research-matrix tr:last-child td{border-bottom:0}.research-matrix th:last-child,.research-matrix td:last-child{border-right:0}.restored-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:18px}.restored-card{background:#fff;border:1px solid var(--line);border-radius:18px;padding:21px}.restored-card h3{font-size:1.03rem;margin:0 0 9px}.restored-card ul{margin:0;padding-left:1.15em;color:var(--muted);font-size:.86rem}.research-archive{margin-top:24px;background:#fff;border:1px solid var(--line);border-radius:18px;padding:20px}.research-archive summary{cursor:pointer;font-weight:800;color:var(--accent)}.research-archive-content{margin-top:20px;padding-top:18px;border-top:1px solid var(--line);font-size:.94rem;color:#32445a}.research-archive-content h1{display:none}.research-archive-content h2{font-size:1.65rem;margin-top:2em}.research-archive-content h3{font-size:1.22rem;margin-top:1.7em}.research-archive-content table{width:100%;border-collapse:collapse;display:block;overflow-x:auto}.research-archive-content th,.research-archive-content td{border:1px solid var(--line);padding:9px 10px;vertical-align:top}.research-archive-content a{color:var(--accent);text-decoration:underline;text-underline-offset:.14em}.archive-note{color:var(--muted);font-size:.82rem;margin-top:8px}@media(max-width:900px){.restored-grid{grid-template-columns:1fr}}
'''
text=text.replace('</style>',style+'</style>',1)

block='''<section id="detailed-research-map" class="section"><div class="shell"><div class="section-head"><div><div class="kicker">Detailed research map</div><h2>Five goals × four research lines.</h2></div><p>This restores the more detailed map from the previous Research page while keeping the modern overview above.</p></div><div class="research-matrix-wrap"><table class="research-matrix"><thead><tr><th>Research line \\ Goal</th><th>Efficiency</th><th>Abstraction</th><th>Automation</th><th>Application</th><th>Verification</th></tr></thead><tbody>
<tr><th>G · Geometry &amp; anisotropic FEM</th><td>Reduce cost by directional interpolation and refine only where geometry or solution structure requires it.</td><td>Organise flatness, semi-regularity, discrete Sobolev inequalities and related mesh conditions into computable geometry.</td><td>Design anisotropic AFEM driven by geometric parameters.</td><td>Extend FEM geometry to spheres, polygonal domains, CutFEM and other complex geometries.</td><td>Make mesh assumptions explicit and checkable through computable geometric conditions.</td></tr>
<tr><th>R · Reliable &amp; goal-oriented PDE simulation</th><td>Target the dominant seminorm error or quantity of interest rather than over-resolving every component.</td><td>Abstract goal functionals, dual problems and goal-oriented error-control structures.</td><td>Combine functional / hypercircle majorants, CR–RT fluxes and verified adaptive computation.</td><td>Pressure-robust Stokes/Navier–Stokes, fractional-time PDEs and long-time stable simulations.</td><td>Provide certified outputs through equilibrated fluxes, DWR and a posteriori certificates.</td></tr>
<tr><th>A · Automation, learning &amp; new methods</th><td>Automatically tune parameters and mesh strategies from mathematical and data-driven indicators.</td><td>Compare FEM, PINNs and Deep Ritz through the common ideas of representation, metric and projection.</td><td>Use geometric parameters and error indicators as features for mesh generation and method selection.</td><td>Connect numerical analysis with climate, disaster, engineering and data-science applications.</td><td>Add a reliability layer to physics-informed ML and surrogate models.</td></tr>
<tr><th>V · Verification, formal reasoning &amp; AI4Math</th><td>Use certified bounds for stopping criteria and efficient adaptation.</td><td>Restructure interpolation, stability, conservation and error bounds into formalisation-ready statements.</td><td>Support lemma search, proof assistance and counterexample detection in FEM analysis.</td><td>Present certified outputs suitable for digital twins and decision-support workflows.</td><td>Build a finite-element foundation that remains verifiable in an AI4Math setting.</td></tr>
</tbody></table></div>
<div class="section-head" style="margin-top:34px"><div><div class="kicker">Restored research memo</div><h2>Specific problems retained from the previous page.</h2></div><p>These were compressed out of the modern summary but remain useful as concrete research directions.</p></div><div class="restored-grid">
<article class="restored-card"><h3>DG medius analysis under semi-regular geometry</h3><ul><li>Identify what anisotropic elements change in standard DG analysis.</li><li>Clarify penalty terms, condition numbers and error estimates.</li><li>Rebuild the older DG research note around these questions.</li></ul></article>
<article class="restored-card"><h3>Helmholtz decomposition on non-simple domains</h3><ul><li>Multiply connected domains and domains with corners.</li><li>Connection with pressure robustness.</li><li>Influence of boundary regularity and topology.</li></ul></article>
<article class="restored-card"><h3>Lagrange FEM and hypercircle certification</h3><ul><li>Transfer anisotropic information through RT-type flux estimates.</li><li>Investigate whether equilibrated fluxes bypass low-regularity interpolation restrictions in 3D.</li><li>Determine how computable geometric assumptions enter certified computation.</li></ul></article>
</div>
<details class="research-archive"><summary>Read full detailed research archive (Japanese)</summary><p class="archive-note">This is the complete pre-modern Research page, preserved for mathematical detail and historical continuity.</p><div id="research-archive-content" class="research-archive-content"><span class="loading">Load on open.</span></div></details>
</div></section>'''
marker='<section class="section"><div class="shell"><div class="section-head"><div><div class="kicker">Research memo</div>'
if marker not in text:
    raise SystemExit('Research memo marker not found')
text=text.replace(marker,block+'\n'+marker,1)

script='''<script>
(function(){
  var box=document.querySelector('.research-archive');
  var target=document.getElementById('research-archive-content');
  if(!box||!target) return;
  var loaded=false;
  box.addEventListener('toggle',function(){
    if(!box.open||loaded) return;
    loaded=true;
    target.innerHTML='<span class="loading">Loading detailed archive…</span>';
    fetch('./research-details.txt').then(function(r){if(!r.ok) throw new Error('HTTP '+r.status);return r.text();}).then(function(html){
      var doc=new DOMParser().parseFromString(html,'text/html');
      var src=doc.querySelector('.section-in');
      if(!src) throw new Error('archive content not found');
      target.innerHTML=src.innerHTML;
      target.querySelectorAll('script').forEach(function(n){n.remove();});
      if(window.MathJax&&MathJax.typesetPromise) MathJax.typesetPromise([target]).catch(function(){});
    }).catch(function(){target.innerHTML='<span class="vision-error">The detailed archive could not be loaded.</span>';});
  });
})();
</script>
'''
text=text.replace('<script src="../js/modern-ui.js"></script>',script+'<script src="../js/modern-ui.js"></script>',1)
p.write_text(text,encoding='utf-8')
print('Restored detailed research map and archive access')
