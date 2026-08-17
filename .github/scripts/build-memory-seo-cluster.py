from pathlib import Path

blog = Path('blog/index.html')
text = blog.read_text(encoding='utf-8')
old_tabs = '<div class="blog-tabs"><a href="#start-here">Start here</a><a href="#core">Core series</a>'
new_tabs = '<div class="blog-tabs"><a href="#start-here">FEM start</a><a href="#memory-start">Stable reduction</a><a href="#core">Core series</a>'
if old_tabs in text:
    text = text.replace(old_tabs, new_tabs, 1)

if 'id="memory-start"' not in text:
    marker = '<section id="research-routes" class="section">'
    if marker not in text:
        raise RuntimeError('research-routes marker not found')
    block = '''<section id="memory-start" class="section"><div class="shell"><div class="section-head"><div><div class="kicker">Start here · Stable reduction</div><h2>Six entry points into memory and unresolved dynamics.</h2></div><p>Start from exact elimination of hidden states, then move through measure-valued delay and energy structure to convolution quadrature and a complete model-reduction error budget.</p></div><div class="entry-grid">
<a class="entry-card feature" href="./posts/unresolved-memory-01.html"><span class="entry-label">Overview</span><h3>未解像ダイナミクスと履歴依存型発展方程式</h3><p>The full route from hidden states and memory kernels to stability, discretisation and certification.</p></a>
<a class="entry-card feature" href="./posts/unresolved-memory-02.html"><span class="entry-label">Exact elimination</span><h3>未解像状態を消去すると，なぜmemoryが現れるのか</h3><p>Derive the memory kernel and dynamic Schur complement directly from an enlarged local-in-time system.</p></a>
<a class="entry-card" href="./posts/unresolved-memory-03.html"><span class="entry-label">Delay law</span><h3>measure-valued delayで分布遅延・原子遅延・混合遅延を統一する</h3><p>Use finite Borel measures to treat distributed, atomic and mixed delays in one framework.</p></a>
<a class="entry-card" href="./posts/unresolved-memory-05.html"><span class="entry-label">Energy structure</span><h3>positive-type memoryとcoercivity gap</h3><p>Separate non-negative memory dissipation from uniform coercivity and identify the high-frequency obstruction.</p></a>
<a class="entry-card" href="./posts/unresolved-memory-09.html"><span class="entry-label">Time discretisation</span><h3>BDFとconvolution quadratureは何を離散化しているのか</h3><p>Interpret convolution quadrature as discrete operational calculus acting on a transfer function.</p></a>
<a class="entry-card" href="./posts/unresolved-memory-10.html"><span class="entry-label">Error budget</span><h3>model-reduction errorをどう分解するか</h3><p>Separate closure, kernel, space, time and algebraic errors through an explicit hierarchy of intermediate problems.</p></a>
</div></div></section>
'''
    text = text.replace(marker, block + marker, 1)
blog.write_text(text, encoding='utf-8')

configs = {
'unresolved-memory-01.html': ('<h2>Introduction：計算から消した状態は，本当に消えるのか</h2>','<h2>はじめに――未解像ダイナミクスはなぜmemoryを残すのか</h2>', [('unresolved-memory-02.html','未解像状態を消去すると，なぜmemoryが現れるのか'),('unresolved-memory-03.html','measure-valued delayで遅延を統一する'),('../../research/#stable-reduction','Stable reduction research'),('../../fem/#vision18','Vision 18：Stable reduction theory')]),
'unresolved-memory-02.html': ('<h2>Introduction：memoryはどこから来るのか</h2>','<h2>はじめに――未解像状態を消去すると，なぜmemory kernelが現れるのか</h2>', [('unresolved-memory-01.html','未解像ダイナミクスと履歴依存型方程式の全体像'),('unresolved-memory-05.html','positive-type memoryとcoercivity gap'),('unresolved-memory-09.html','BDFとconvolution quadrature'),('../../research/#stable-reduction','Stable reduction research')]),
'unresolved-memory-03.html': ('<h2>Introduction：delay lawを「関数」ではなく「測度」で表す</h2>','<h2>はじめに――measure-valued delayで何を統一できるのか</h2>', [('unresolved-memory-04.html','指数重みでmeasure-valued delayのwell-posednessを得る'),('unresolved-memory-07.html','kernel stabilityとfinite-atomic approximation'),('unresolved-memory-01.html','memory seriesの全体像'),('../../publications/#preprints','Current preprints')]),
'unresolved-memory-05.html': ('<h2>Introduction：散逸的であることとcoerciveであることは同じではない</h2>','<h2>はじめに――positive-type memoryはcoercivityを与えるのか</h2>', [('unresolved-memory-06.html','graph-space well-posednessとは何か'),('unresolved-memory-08.html','離散内部変数でcross-term cancellationを保存する'),('unresolved-memory-01.html','memory seriesの全体像'),('../../research/#stable-reduction','Stable reduction research')]),
'unresolved-memory-09.html': ('<h2>Introduction：CQはkernelを格子点で積分する方法ではない</h2>','<h2>はじめに――BDF convolution quadratureは何を離散化するのか</h2>', [('unresolved-memory-08.html','離散内部変数でcross-term cancellationを保存する'),('unresolved-memory-10.html','model-reduction errorをどう分解するか'),('unresolved-memory-02.html','dynamic Schur complementとmemory kernel'),('../../publications/#preprints','Current preprints')]),
'unresolved-memory-10.html': ('<h2>Introduction：細かいメッシュだけでは正しい答えにならない</h2>','<h2>はじめに――model-reduction errorと離散化誤差をどう分けるか</h2>', [('unresolved-memory-07.html','kernel stabilityとfinite-atomic approximation'),('unresolved-memory-09.html','BDFとconvolution quadrature'),('unresolved-memory-11.html','誤差に応じて潜在状態を追加するmodel adaptivity'),('../../research/#stable-reduction','Stable reduction research')])
}

descs = {
'unresolved-memory-01.html': ('未解像ダイナミクスから生じる履歴依存型方程式を，measure-valued delay，Volterra memory，内部変数，kernel stability，構造保存完全離散化の観点から整理します．','Stable reductionの入口として，未解像状態の消去から生じるmemoryを，measure-valued delay，Volterra memory，kernel stability，BDF/CQまで一つの流れで整理します．'),
'unresolved-memory-09.html': ('BDFとconvolution quadratureは何を離散化しているのかについて，有限要素法・数値解析・PDEの観点から整理するHiroki Ishizakaの研究ノートです．','BDF convolution quadratureを，kernelの直接積分ではなくLaplace領域のtransfer functionにBDF symbolを代入する離散operational calculusとして解説します．')
}

for name,(old_h2,new_h2,links) in configs.items():
    p = Path('blog/posts') / name
    s = p.read_text(encoding='utf-8')
    if new_h2 not in s:
        if old_h2 not in s:
            raise RuntimeError(f'opening h2 not found: {name}')
        s = s.replace(old_h2, new_h2, 1)
    if name in descs:
        old_desc,new_desc = descs[name]
        if old_desc in s:
            s = s.replace(old_desc,new_desc)
    if '<!-- memory-search-entry-related -->' not in s:
        pos = s.find(new_h2)
        boundary = s.find('</article>\n</div>\n\n<h2', pos)
        if boundary < 0:
            raise RuntimeError(f'intro boundary not found: {name}')
        close_end = s.find('</div>', boundary) + len('</div>')
        items = ''.join(f'<li><a href="{href}">{label}</a></li>' for href,label in links)
        block = '\n\n<!-- memory-search-entry-related -->\n<div style="padding:12px 15px;margin:14px 0 22px;border:1px solid #dfe6ef;border-radius:14px;background:#f7f9fc;">\n<b>関連して読む</b>\n<ul>' + items + '</ul>\n</div>'
        s = s[:close_end] + block + s[close_end:]
    p.write_text(s, encoding='utf-8')

assert blog.read_text(encoding='utf-8').count('id="memory-start"') == 1
for name,(_,new_h2,_) in configs.items():
    s=(Path('blog/posts')/name).read_text(encoding='utf-8')
    assert new_h2 in s
    assert s.count('<!-- memory-search-entry-related -->') == 1
print('Stable reduction SEO cluster prepared and validated.')
