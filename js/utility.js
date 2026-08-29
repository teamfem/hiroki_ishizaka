if(window.jQuery){
  jQuery.noConflict();
(function($) {
	
		//マウスオーバー（ファイルの末尾に「_off」「_on」で切り替え）
		$("img.over,input.over")
		.each( function(){
			$("<img>,<input>").attr("src",$(this).attr("src").replace(/^(.+)_off(\.[a-z]+)$/, "$1_on$2"));
		})
		.mouseover( function(){
			$(this).attr("src",$(this).attr("src").replace(/^(.+)_off(\.[a-z]+)$/, "$1_on$2"));
		})
		.mouseout( function(){
			$(this).attr("src",$(this).attr("src").replace(/^(.+)_on(\.[a-z]+)$/, "$1_off$2"));
		});
		
		//テーブルのセルとリストに偶数・奇数を付与
		$("li:nth-child(odd),tr:nth-child(odd)").addClass("odd"),
		$("li:nth-child(even),tr:nth-child(even)").addClass("even");

		//スムーズスクロール
		var topBtn = $('.page-top');
		topBtn.hide();
		$(window).scroll(function () {
			if ($(this).scrollTop() > 100) {
				topBtn.fadeIn();
			} else {
				topBtn.fadeOut();
			}
		});

		$("a[href^='#']").click(function(){
			var Hash = $(this.hash);
			var HashOffset = $(Hash).offset().top;
			$("html,body").animate({
				scrollTop: $($(this).attr("href")).offset().top }, 'slow','swing');
			return false;
		});

		//グローバルメニューのプルダウン設定
		$("#menu li").hover(function() {
			$("> ul:not(:animated)", this).fadeIn("normal");
		}, function() {
			$("> ul", this).fadeOut("normal");
		});
		
		//モバイル用のグローバルメニュー設定
		$(".global-nav-panel").click(function(){
			$("#menu").toggleClass("show-menu");
		});

		$(".global-nav-panel").click(function(){
			if($("span",this).hasClass("btn-global-nav icon-gn-menu")){
				$("span",this).removeClass("icon-gn-menu").addClass("icon-gn-close");
				$("span",this).text("閉じる");
			} else {
				$("span",this).removeClass("icon-gn-close").addClass("icon-gn-menu");
				$("span",this).text("メニュー");
			};
        });

		//クリックでテキストを選択
		$(".text-field")
			.focus(function(){
				$(this).select();
			})
			.click(function(){
				$(this).select();
				return false;
			});

		function lpHeader(){
			hdrWidth = $(window).width();
			hdrHeight = $(window).height();
			$('.full-screen,.full-screen .site-header-in,.full-screen .site-header-conts').css({
				width: hdrWidth + 'px',
				height: hdrHeight + 'px',
				maxHeight: '1500px'
			});

			if(window.innerWidth < 678) {
				h1Size = hdrWidth / 12;
				fontSize = hdrWidth / 16;
				$('.full-screen .site-header-conts h1').css('font-size', h1Size + 'px');
				$('.full-screen .site-header-conts .lp-catch').css('font-size', fontSize + 'px');
			} else {
				h1Size = hdrHeight / 12;
				fontSize = hdrHeight / 24;
				$('.full-screen .site-header-conts h1').css('font-size', h1Size + 'px');
				$('.full-screen .site-header-conts .lp-catch').css('font-size', fontSize + 'px');
			}
		}
		lpHeader();
		$(window).resize(function() {
			lpHeader();
		});
	
})(jQuery);
}

/* Modern Blog post shell -------------------------------------------------- */
(function(){
  var path = window.location.pathname;
  if(!/\/blog\/posts\/[^/]+\.html$/.test(path) || /-modern-preview\.html$/.test(path)) return;

  var source = document.querySelector('.section-in');
  if(!source) return;

  function addStylesheet(href){
    if(document.querySelector('link[href="'+href+'"]')) return;
    var link=document.createElement('link');
    link.rel='stylesheet';
    link.href=href;
    document.head.appendChild(link);
  }
  addStylesheet('../../css/modern.css');
  addStylesheet('../../css/blog-post-modern.css');
  document.querySelectorAll('link[rel="stylesheet"]').forEach(function(link){
    var href=link.getAttribute('href')||'';
    if(/(?:^|\/)css\/(?:base|rwd)\.css(?:\?|$)/.test(href)) link.disabled=true;
  });

  var originalTitle=document.title;
  var file=(path.split('/').pop()||'').replace(/\.html$/,'');
  var titleNode=source.querySelector('h1.section-title, h1');
  var title=titleNode ? titleNode.textContent.trim() : originalTitle.split('|')[0].trim();
  if(title) document.title=title+' | Hiroki Ishizaka';

  var defs=[
    {re:/^anisotropic-geometry-(\d+)$/,label:'異方性有限要素法の幾何学的基礎',anchor:'../#geometry',max:12,prefix:'anisotropic-geometry-',pad:2,tag:'Geometry · Anisotropic FEM'},
    {re:/^unresolved-memory-(\d+)$/,label:'Memory, delay and stable reduction',anchor:'../#memory',max:11,prefix:'unresolved-memory-',pad:2,tag:'Unresolved dynamics · Memory'},
    {re:/^exact-curved-fem-(\d+)$/,label:'Exact-curved FEM',anchor:'../#curved',max:6,prefix:'exact-curved-fem-',pad:2,tag:'Exact geometry · FEM'},
    {re:/^paradoxes-pitfalls-(\d+)$/,label:'Classical paradoxes and modern questions',anchor:'../#paradoxes',max:2,prefix:'paradoxes-pitfalls-',pad:2,tag:'Numerical analysis · Counterexamples'},
    {re:/^pinns-(\d+)$/,label:'PINNs · Deep Ritz · learning-assisted computation',anchor:'../#applications',max:7,prefix:'pinns-',pad:2,tag:'Scientific machine learning'},
    {re:/^dental-math-(\d+)$/,label:'Mathematics for dental modelling',anchor:'../#applications',max:2,prefix:'dental-math-',pad:2,tag:'Applications · Mathematical modelling'},
    {re:/^disease-progression-math-(\d+)$/,label:'Latent-state disease progression',anchor:'../#applications',max:1,prefix:'disease-progression-math-',pad:2,tag:'Applications · Unresolved dynamics'},
    {re:/^lean4-(\d+)$/,label:'Certified FEM · verified output · AI4Math',anchor:'../#certified',max:1,prefix:'lean4-',pad:2,tag:'Certification · AI4Math'}
  ];
  var def=null, number=null;
  defs.some(function(d){var m=file.match(d.re);if(m){def=d;number=parseInt(m[1],10);return true;}return false;});
  if(!def && /^article/.test(file)) def={label:'Foundational and computational notes',anchor:'../#foundations',tag:'Numerical methods · Implementation'};
  if(!def) def={label:'Research Note',anchor:'../',tag:'Numerical analysis · PDEs · FEM'};

  var metaCandidate=titleNode ? titleNode.nextElementSibling : null;
  var metaTime=metaCandidate && metaCandidate.querySelector ? metaCandidate.querySelector('time[datetime]') : null;
  if(!metaTime) metaTime=source.querySelector('time[datetime]');
  var metaStatus=metaCandidate && metaCandidate.querySelector ? metaCandidate.querySelector('.cat') : null;
  var metaSeries=metaCandidate && metaCandidate.querySelector ? metaCandidate.querySelector('b,strong') : null;

  function publishedDateFromStructuredData(){
    try{
      var node=document.getElementById('site-structured-data');
      if(!node) return '';
      var data=JSON.parse(node.textContent||'{}');
      var graph=data['@graph']||[];
      for(var i=0;i<graph.length;i++){
        var type=graph[i]['@type'];
        if((type==='BlogPosting'||(Array.isArray(type)&&type.indexOf('BlogPosting')>=0))&&graph[i].datePublished) return graph[i].datePublished;
      }
    }catch(e){}
    return '';
  }
  function formatISODate(iso){
    var m=String(iso||'').match(/^(\d{4})-(\d{2})-(\d{2})$/);
    if(!m) return iso||'';
    var day=parseInt(m[3],10), mod100=day%100, suffix='th';
    if(mod100<11||mod100>13){if(day%10===1)suffix='st';else if(day%10===2)suffix='nd';else if(day%10===3)suffix='rd';}
    var months=['January','February','March','April','May','June','July','August','September','October','November','December'];
    return day+suffix+' '+months[parseInt(m[2],10)-1]+' '+m[1];
  }

  var date=metaTime ? metaTime.textContent.trim() : '';
  if(!date) date=formatISODate(publishedDateFromStructuredData());
  if(!date){
    var dm=originalTitle.match(/from\s+([^|]+?)\s*\|/i);
    if(dm) date=dm[1].trim();
  }
  var seriesLabel=(metaSeries && metaSeries.textContent.trim().length<120) ? metaSeries.textContent.trim() : def.label;
  if(!seriesLabel || /^(今回の結論|この連載の読み方)/.test(seriesLabel)) seriesLabel=def.label;
  var status=metaStatus ? metaStatus.textContent.trim() : '';

  var fragment=document.createDocumentFragment();
  Array.prototype.slice.call(source.childNodes).forEach(function(node){
    if(node===titleNode) return;
    if(node===metaCandidate && metaTime) return;
    fragment.appendChild(node);
  });

  function pageFor(n){
    if(!def.prefix || !n || n<1 || n>def.max) return null;
    var s=String(n);
    if(def.pad) s=s.padStart(def.pad,'0');
    return './'+def.prefix+s+'.html';
  }
  var prev=number ? pageFor(number-1) : null;
  var next=number ? pageFor(number+1) : null;

  document.body.className='modern-blog-post';
  document.body.innerHTML='\
<header class="topbar"><div class="shell nav"><a class="brand" href="../../">Hiroki Ishizaka<small>Numerical Analysis · PDEs · FEM</small></a><nav class="navlinks" aria-label="Primary navigation"><a href="../../research/">Research</a><a href="../../publications/">Publications</a><a href="../../fem/">Visions</a><a href="../../suppl/">Supplementary</a><a href="../../blog/" aria-current="page">Blog</a><a href="../../geo/">Geometry</a><a href="../../links/">Links</a><a href="../../contact/">Contact</a></nav></div></header>\
<main id="top"><section class="article-hero"><div class="shell"><div class="crumbs"><a href="../../">Home</a><span>›</span><a href="../">Blog</a><span>›</span><a href="'+def.anchor+'">'+def.label+'</a></div><div class="article-series"></div><h1></h1><div class="article-meta"></div></div></section><div class="article-layout"><article id="article-body" class="article-body"></article><aside class="article-side"><nav class="toc" aria-label="Table of contents"><div class="toc-title">On this page</div><div id="toc-links"></div></nav><div class="series-nav"><b>Series navigation</b><a href="'+def.anchor+'">← Blog series index</a></div></aside></div><div class="article-footer-nav"><div class="navbox" id="post-nav"></div></div></main>\
<footer class="footer"><div class="shell footer-inner"><span>© 2026 Hiroki Ishizaka</span><span>Research Notes · Numerical Analysis</span></div></footer><a class="article-toplink" href="#top" aria-label="Back to top">↑</a>';

  document.querySelector('.article-series').textContent=seriesLabel;
  document.querySelector('.article-hero h1').textContent=title;
  var meta=document.querySelector('.article-meta');
  [date,status,def.tag].filter(Boolean).forEach(function(text,i){var s=document.createElement('span');if(i===0 && date){var b=document.createElement('b');b.textContent=text;s.appendChild(b);}else{s.textContent=text;}meta.appendChild(s);});

  var article=document.getElementById('article-body');
  article.appendChild(fragment);
  var headings=Array.prototype.slice.call(article.querySelectorAll('h2'));
  var toc=document.getElementById('toc-links');
  headings.forEach(function(h,i){
    if(!h.id) h.id='section-'+(i+1);
    var a=document.createElement('a');a.href='#'+h.id;a.textContent=h.textContent.trim();toc.appendChild(a);
  });
  if(!headings.length){var s=document.createElement('span');s.className='loading';s.textContent='No section headings';toc.appendChild(s);}

  var side=document.querySelector('.series-nav');
  if(prev){var a=document.createElement('a');a.href=prev;a.textContent='← Previous article';side.appendChild(a);}
  if(next){var a=document.createElement('a');a.href=next;a.textContent='Next article →';side.appendChild(a);}

  var postNav=document.getElementById('post-nav');
  function navLink(href,kicker,text){var a=document.createElement('a');a.href=href;var sp=document.createElement('span');sp.textContent=kicker;a.appendChild(sp);a.appendChild(document.createTextNode(text));postNav.appendChild(a);}
  navLink(def.anchor,'Series',def.label);
  if(prev) navLink(prev,'Previous article','← Previous in this series');
  if(next) navLink(next,'Next article','Next in this series →');
  if(!prev && !next) postNav.classList.add('single');

  if(!document.querySelector('script[src*=\"modern-ui.js\"]')){var ui=document.createElement('script');ui.src='../../js/modern-ui.js';document.body.appendChild(ui);}

  function fitDisplayMath(root){
    var boxes=Array.prototype.slice.call(root.querySelectorAll('mjx-container[display="true"]'));
    boxes.forEach(function(box){
      box.classList.remove('math-scaled','math-scroll');
      box.style.fontSize='';
      var math=box.querySelector('mjx-math');
      if(!math) return;

      var available=box.clientWidth;
      var width=math.getBoundingClientRect().width;
      if(!available || width<=available+2) return;

      var scale=Math.max(0.66,Math.min(1,(available/width)*0.97));
      box.style.fontSize=scale+'em';

      var fittedWidth=math.getBoundingClientRect().width;
      if(fittedWidth<=box.clientWidth+2){
        box.classList.add('math-scaled');
      }else{
        box.classList.add('math-scroll');
      }
    });
  }

  var resizeTimer=null;
  window.addEventListener('resize',function(){
    clearTimeout(resizeTimer);
    resizeTimer=setTimeout(function(){fitDisplayMath(article);},120);
  });

  if(window.MathJax && MathJax.typesetPromise){
    MathJax.typesetPromise([article]).then(function(){fitDisplayMath(article);}).catch(function(){});
  }
})();
