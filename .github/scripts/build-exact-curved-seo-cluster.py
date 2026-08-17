from pathlib import Path

BLOG = Path('blog/index.html')
blog = BLOG.read_text(encoding='utf-8')

# Add a direct tab to the Exact-curved FEM entry cluster.
old_tabs = '<a href="#memory-start">Stable reduction</a><a href="#core">Core series</a>'
new_tabs = '<a href="#memory-start">Stable reduction</a><a href="#curved-start">Exact-curved FEM</a><a href="#core">Core series</a>'
if old_tabs in blog:
    blog = blog.replace(old_tabs, new_tabs, 1)

if 'id="curved-start"' not in blog:
    marker = '<section id="research-routes" class="section">'
    if marker not in blog:
        raise RuntimeError('research-routes marker not found in blog/index.html')
    block = '''<section id="curved-start" class="section"><div class="shell"><div class="section-head"><div><div class="kicker">Start here · Exact-curved FEM</div><h2>Six entry points into finite elements on curved domains.</h2></div><p>Follow the geometry from the basic question of keeping a curved domain curved, through affine-core decomposition and implementation, to numerical comparison and the distinction from isoparametric FEM.</p></div><div class="entry-grid">
<a class="entry-card feature" href="./posts/exact-curved-fem-01.html"><span class="entry-label">Curved domain</span><h3>有限要素法で「丸い領域」を丸いまま扱いたい</h3><p>Separate finite-element approximation error from the geometric error created by polygonalising a curved boundary.</p></a>
<a class="entry-card feature" href="./posts/exact-curved-fem-02.html"><span class="entry-label">Element map</span><h3>曲線要素写像を affine core と curved correction に分ける</h3><p>Factor the element map so that scale, orientation and anisotropy are separated from boundary curvature.</p></a>
<a class="entry-card" href="./posts/exact-curved-fem-03.html"><span class="entry-label">Geometry order</span><h3>Gmsh の geometry order は有限要素次数ではない</h3><p>Distinguish the order used to represent mesh geometry from the polynomial degree used to approximate the unknown.</p></a>
<a class="entry-card" href="./posts/exact-curved-fem-04.html"><span class="entry-label">FEniCSx / UFL</span><h3>UFL の grad と dx の中で何が起きているか</h3><p>See where the inverse-transpose Jacobian and determinant enter when integration is pulled back to a reference element.</p></a>
<a class="entry-card" href="./posts/exact-curved-fem-05.html"><span class="entry-label">Numerical comparison</span><h3>単位円上の Poisson 問題で曲線メッシュを比較する</h3><p>Keep the finite-element degree at P1 and vary only the geometric order to isolate the effect of curved geometry.</p></a>
<a class="entry-card" href="./posts/exact-curved-fem-06.html"><span class="entry-label">Method comparison</span><h3>Exact-curved FEMs と isoparametric FEMs は何が違うのか</h3><p>Compare similar implementations while distinguishing the analytical role of the affine core and curved correction.</p></a>
</div></div></section>
'''
    blog = blog.replace(marker, block + marker, 1)
BLOG.write_text(blog, encoding='utf-8')

configs = {
    'exact-curved-fem-01.html': {
        'old_h2': '<h2>Introduction</h2>',
        'new_h2': '<h2>はじめに――有限要素法で曲線領域を「曲がったまま」扱うとは何か</h2>',
        'old_desc': '有限要素法で「丸い領域」を丸いまま扱いたいについて，有限要素法・数値解析・PDEの観点から整理するHiroki Ishizakaの研究ノートです．',
        'new_desc': '曲線領域を多角形化したときの幾何誤差と有限要素近似誤差を分け，Exact-curved FEMで曲線境界をそのまま扱う考え方をGmsh/FEniCSxとともに整理します．',
        'keywords': '石坂宏樹,Hiroki Ishizaka,Exact-curved FEM,curved domain,geometric error,Gmsh,FEniCSx,finite element method',
        'links': [
            ('exact-curved-fem-02.html','曲線要素写像を affine core と curved correction に分ける'),
            ('exact-curved-fem-03.html','Gmsh の geometry order は有限要素次数ではない'),
            ('../../publications/#preprints','Current preprints'),
            ('../../fem/#vision10','Vision 10：Exact-curved geometry programme')
        ]
    },
    'exact-curved-fem-02.html': {
        'old_h2': '<h2>Introduction</h2>',
        'new_h2': '<h2>はじめに――曲線要素写像を affine core と curved correction に分ける理由</h2>',
        'old_desc': '曲線要素写像を affine core と curved correction に分けるについて，有限要素法・数値解析・PDEの観点から整理するHiroki Ishizakaの研究ノートです．',
        'new_desc': '曲線要素写像を F_K=Psi_K∘Phi_TK と分解し，affine coreが担うスケール・向き・異方性と，curved correctionが担う曲線幾何を分離して解析する考え方を解説します．',
        'keywords': '石坂宏樹,Hiroki Ishizaka,Exact-curved FEM,affine core,curved correction,element map,anisotropic finite elements,curved elements',
        'links': [
            ('exact-curved-fem-01.html','曲線領域を丸いまま扱うという出発点'),
            ('exact-curved-fem-06.html','Exact-curved FEMs と isoparametric FEMs の違い'),
            ('../../research/#fem-summary','FEM research architecture'),
            ('../../fem/#vision10','Vision 10：Exact-curved geometry programme')
        ]
    },
    'exact-curved-fem-03.html': {
        'old_h2': '<h2>Introduction</h2>',
        'new_h2': '<h2>はじめに――Gmsh の geometry order と有限要素次数は何が違うのか</h2>',
        'old_desc': 'Gmsh の geometry order は有限要素次数ではないについて，有限要素法・数値解析・PDEの観点から整理するHiroki Ishizakaの研究ノートです．',
        'new_desc': 'Gmshのgeometry order q_geoと有限要素次数kを区別し，曲線メッシュの幾何表現を高次化しても未知関数の有限要素近似次数が自動的に上がるわけではないことを整理します．',
        'keywords': '石坂宏樹,Hiroki Ishizaka,Gmsh,geometry order,finite element degree,curved mesh,FEniCSx,Exact-curved FEM',
        'links': [
            ('exact-curved-fem-02.html','affine core と curved correction'),
            ('exact-curved-fem-04.html','UFL の grad と dx の中で何が起きているか'),
            ('exact-curved-fem-05.html','単位円上で geometry order を比較する'),
            ('../../fem/#vision10','Vision 10：Exact-curved geometry programme')
        ]
    },
    'exact-curved-fem-04.html': {
        'old_h2': '<h2>Introduction</h2>',
        'new_h2': '<h2>はじめに――UFL の grad と dx は曲線要素写像をどう扱うのか</h2>',
        'old_desc': 'UFL の grad と dx の中で何が起きているかについて，有限要素法・数値解析・PDEの観点から整理するHiroki Ishizakaの研究ノートです．',
        'new_desc': 'FEniCSx/UFLのgradとdxで，曲線要素写像F_KのJacobianがどこに現れるかを整理し，勾配のDF_K^{-T}と積分測度の|det DF_K|を参照要素への引き戻しから解説します．',
        'keywords': '石坂宏樹,Hiroki Ishizaka,FEniCSx,UFL,grad,dx,Jacobian,curved element map,Exact-curved FEM',
        'links': [
            ('exact-curved-fem-03.html','Gmsh の geometry order と有限要素次数'),
            ('exact-curved-fem-05.html','単位円上の Poisson 問題で曲線メッシュを比較する'),
            ('exact-curved-fem-02.html','曲線要素写像の二段分解'),
            ('../../research/#fem-summary','FEM research architecture')
        ]
    },
    'exact-curved-fem-05.html': {
        'old_h2': '<h2>Introduction</h2>',
        'new_h2': '<h2>はじめに――P1有限要素で幾何次数だけを変えると何が変わるのか</h2>',
        'old_desc': '単位円上の Poisson 問題で曲線メッシュを比較するについて，有限要素法・数値解析・PDEの観点から整理するHiroki Ishizakaの研究ノートです．',
        'new_desc': '単位円上のPoisson問題で有限要素次数をP1に固定し，geometry orderだけを変えて直線メッシュと曲線メッシュを比較し，幾何誤差と有限要素誤差の違いを確認します．',
        'keywords': '石坂宏樹,Hiroki Ishizaka,Poisson equation,unit disk,curved mesh,geometry order,P1 finite element,Gmsh,FEniCSx',
        'links': [
            ('exact-curved-fem-03.html','geometry order と有限要素次数の違い'),
            ('exact-curved-fem-04.html','UFL の grad と dx'),
            ('exact-curved-fem-06.html','Exact-curved FEMs と isoparametric FEMs'),
            ('../../publications/#preprints','Current preprints')
        ]
    },
    'exact-curved-fem-06.html': {
        'old_h2': '<h2>Introduction</h2>',
        'new_h2': '<h2>はじめに――Exact-curved FEM と isoparametric FEM は何が違うのか</h2>',
        'old_desc': 'Exact-curved FEMs と isoparametric FEMs は何が違うのかについて，有限要素法・数値解析・PDEの観点から整理するHiroki Ishizakaの研究ノートです．',
        'new_desc': 'Exact-curved FEMとisoparametric FEMを比較し，実装は似ていても，affine coreとcurved correctionを分離して要素の異方性と境界曲率を別々に解析する点を整理します．',
        'keywords': '石坂宏樹,Hiroki Ishizaka,Exact-curved FEM,isoparametric FEM,affine core,curved correction,curved elements,finite element analysis',
        'links': [
            ('exact-curved-fem-02.html','affine core と curved correction の分解'),
            ('exact-curved-fem-05.html','単位円上の数値比較'),
            ('../../fem/#vision10','Vision 10：Exact-curved geometry programme'),
            ('../../publications/#preprints','Current preprints')
        ]
    }
}

for name, cfg in configs.items():
    p = Path('blog/posts') / name
    text = p.read_text(encoding='utf-8')

    if cfg['new_h2'] not in text:
        if cfg['old_h2'] not in text:
            raise RuntimeError(f'opening H2 not found: {name}')
        text = text.replace(cfg['old_h2'], cfg['new_h2'], 1)

    if cfg['old_desc'] in text:
        text = text.replace(cfg['old_desc'], cfg['new_desc'])
    elif cfg['new_desc'] not in text:
        raise RuntimeError(f'description not found: {name}')

    old_keywords = '石坂宏樹,Hiroki Ishizaka,Finite Element Method,有限要素法'
    if old_keywords in text:
        text = text.replace(old_keywords, cfg['keywords'])

    if '<!-- curved-search-entry-related -->' not in text:
        pos = text.find(cfg['new_h2'])
        boundary = text.find('</article>\n</div>\n\n<h2', pos)
        if boundary < 0:
            raise RuntimeError(f'intro boundary not found: {name}')
        close_end = text.find('</div>', boundary) + len('</div>')
        items = ''.join(f'<li><a href="{href}">{label}</a></li>' for href, label in cfg['links'])
        related = ('\n\n<!-- curved-search-entry-related -->\n'
                   '<div style="padding:12px 15px;margin:14px 0 22px;border:1px solid #dfe6ef;border-radius:14px;background:#f7f9fc;">\n'
                   '<b>関連して読む</b>\n<ul>' + items + '</ul>\n</div>')
        text = text[:close_end] + related + text[close_end:]

    p.write_text(text, encoding='utf-8')

# Validate the full cluster.
blog = BLOG.read_text(encoding='utf-8')
assert blog.count('id="curved-start"') == 1
assert '<a href="#curved-start">Exact-curved FEM</a>' in blog
for name, cfg in configs.items():
    text = (Path('blog/posts') / name).read_text(encoding='utf-8')
    assert cfg['new_h2'] in text
    assert cfg['new_desc'] in text
    assert cfg['keywords'] in text
    assert text.count('<!-- curved-search-entry-related -->') == 1
print('Exact-curved FEM SEO cluster prepared and validated.')
