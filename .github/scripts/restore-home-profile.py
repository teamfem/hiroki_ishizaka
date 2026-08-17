from pathlib import Path

p=Path('index.html')
text=p.read_text(encoding='utf-8')
if 'id="home-philosophy"' in text:
    print('Homepage profile/philosophy already restored')
    raise SystemExit(0)

# Restore the Slides profile link from the previous homepage.
needle='<a href="https://www.researchgate.net/profile/Hiroki-Ishizaka">ResearchGate</a><a href="https://x.com/teamfem16key">X</a>'
replace='<a href="https://www.researchgate.net/profile/Hiroki-Ishizaka">ResearchGate</a><a href="https://sites.google.com/view/hiroki-ishizaka-website/home">Slides</a><a href="https://x.com/teamfem16key">X</a>'
if needle not in text:
    raise SystemExit('Profile link marker not found')
text=text.replace(needle,replace,1)

style='''<style>
.home-profile-grid{display:grid;grid-template-columns:.85fr 1.15fr;gap:18px}.home-profile-card{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:26px;box-shadow:0 12px 32px rgba(20,32,51,.05)}.home-profile-card h3{font-size:1.18rem;margin:0 0 12px}.home-profile-card p{color:var(--muted);margin:0 0 10px}.home-profile-list{display:grid;gap:8px;margin-top:16px}.home-profile-list span{padding:9px 11px;border-radius:12px;background:var(--soft);color:#44566c;font-size:.84rem;font-weight:700}.philosophy-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:20px}.philosophy-card{background:#fff;border:1px solid var(--line);border-radius:18px;padding:22px}.philosophy-card .num{font-size:.72rem;font-weight:850;letter-spacing:.08em;text-transform:uppercase;color:var(--accent)}.philosophy-card h3{font-size:1.05rem;line-height:1.35;margin:7px 0 9px}.philosophy-card p{font-size:.88rem;color:var(--muted);margin:0}.philosophy-quote{margin-top:16px;padding:18px 20px;border-left:4px solid var(--accent);background:#fff;border-radius:0 16px 16px 0;color:#3d5068;font-weight:650}.home-archive{margin-top:22px;background:#fff;border:1px solid var(--line);border-radius:18px;padding:20px}.home-archive summary{cursor:pointer;font-weight:800;color:var(--accent)}.home-archive-content{margin-top:20px;padding-top:18px;border-top:1px solid var(--line);font-size:.94rem;color:#32445a}.home-archive-content h3{font-size:1.2rem;margin:1.8em 0 .6em}.home-archive-content p{margin:0 0 1.15em}.home-archive-content ul,.home-archive-content ol{padding-left:1.35em}.home-archive-content a{color:var(--accent);text-decoration:underline;text-underline-offset:.14em}.home-archive-content mjx-container[display="true"]{overflow-x:auto;overflow-y:hidden}.archive-note{color:var(--muted);font-size:.82rem;margin:8px 0 0}@media(max-width:900px){.home-profile-grid,.philosophy-grid{grid-template-columns:1fr}}
</style>'''
text=text.replace('</head>',style+'</head>',1)

block='''<section id="home-philosophy" class="section"><div class="shell"><div class="section-head"><div><div class="kicker">Professional profile</div><h2>Mathematics, computation and reasoning.</h2></div><p>Selected professional information and research philosophy retained from the previous homepage.</p></div><div class="home-profile-grid"><article class="home-profile-card"><h3>Professional activities</h3><p>Independent Researcher — Numerical Analysis, Partial Differential Equations and Finite Element Methods.</p><div class="home-profile-list"><span>AI Evaluator · Mathematics / Reasoning / Numerical Methods</span><span>Scientific-Computing SME · PDEs &amp; FEMs</span><span>JP / EN</span><span>Member · Mathematical Society of Japan</span><span>Member · Japan Society for Industrial and Applied Mathematics</span></div></article><article class="home-profile-card"><h3>What “invisible” means here</h3><p>Discretisation error, mesh geometry, unresolved scales, latent states, memory, dissipation and limits of numerical prediction are usually not observed directly. Mathematics can represent them through operators, norms, kernels, measures, internal variables, geometric parameters and computable error bounds.</p><p>The guiding question is what has been omitted, how that omitted structure acts on observable dynamics, and which conclusions remain mathematically valid.</p></article></div><div class="philosophy-grid"><article class="philosophy-card"><span class="num">01 · Approximation</span><h3>Certified FEM makes hidden numerical error visible.</h3><p>Mesh geometry and discretisation are treated as mathematical structure to be quantified rather than background implementation detail.</p></article><article class="philosophy-card"><span class="num">02 · Reduction</span><h3>Stable reduction is more than dimension reduction.</h3><p>Variables may be removed, but their dynamical influence must survive through memory, internal states, effective dissipation or nonlocal closure when the full system requires it.</p></article><article class="philosophy-card"><span class="num">03 · Reconstruction</span><h3>Some hidden states should be reconstructed, not eliminated.</h3><p>Partial and noisy history-dependent observations lead to questions of observability, identifiability, stability and uncertainty for physically meaningful latent states.</p></article></div><div class="philosophy-quote">Trustworthy simulation is one consequence of this work, not its sole starting point. Reliability emerges when invisible errors, unresolved influences, stability mechanisms and ranges of validity are mathematically represented and controlled.</div><details class="home-archive"><summary>Read the extended research philosophy from the previous site</summary><p class="archive-note">The longer programme descriptions are preserved here without bringing the old visual layout back.</p><div id="home-archive-content" class="home-archive-content"><span class="loading">Load on open.</span></div></details></div></section>'''
marker='<section class="section"><div class="shell"><div class="section-head"><div><div class="kicker">Recent work</div>'
if marker not in text:
    raise SystemExit('Recent work marker not found')
text=text.replace(marker,block+marker,1)

script='''<script>
(function(){
  var box=document.querySelector('.home-archive');
  var target=document.getElementById('home-archive-content');
  if(!box||!target) return;
  var loaded=false;
  function typeset(){
    if(window.MathJax&&MathJax.typesetPromise){MathJax.typesetPromise([target]).catch(function(){});return;}
    if(document.getElementById('MathJax-script')) return;
    window.MathJax={tex:{inlineMath:[['\\\\(','\\\\)']],displayMath:[['\\\\[','\\\\]']]}};
    var s=document.createElement('script');s.id='MathJax-script';s.async=true;s.src='https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js';document.head.appendChild(s);
  }
  box.addEventListener('toggle',function(){
    if(!box.open||loaded) return;
    loaded=true;
    target.innerHTML='<span class="loading">Loading extended philosophy…</span>';
    fetch('./home-details.txt').then(function(r){if(!r.ok) throw new Error('HTTP '+r.status);return r.text();}).then(function(html){
      var doc=new DOMParser().parseFromString(html,'text/html');
      var src=doc.querySelector('.section-in');
      if(!src) throw new Error('archive content not found');
      var nodes=Array.prototype.slice.call(src.children);
      var start=nodes.findIndex(function(n){return n.tagName==='H3'&&n.textContent.trim()==='Research philosophy';});
      var end=nodes.findIndex(function(n,i){return i>start&&n.tagName==='H3'&&n.textContent.trim()==='Website guide';});
      if(start<0) throw new Error('philosophy section not found');
      if(end<0) end=nodes.length;
      target.innerHTML='';
      nodes.slice(start,end).forEach(function(n){target.appendChild(n.cloneNode(true));});
      target.querySelectorAll('script').forEach(function(n){n.remove();});
      typeset();
    }).catch(function(){target.innerHTML='<span class="vision-error">The extended philosophy could not be loaded.</span>';});
  });
})();
</script>'''
text=text.replace('<script src="./js/modern-ui.js"></script>',script+'<script src="./js/modern-ui.js"></script>',1)
p.write_text(text,encoding='utf-8')
print('Restored professional profile and extended homepage philosophy')
