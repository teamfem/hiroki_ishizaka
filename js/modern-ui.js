(function(){
  'use strict';

  function addSharedStyles(){
    if(document.getElementById('modern-ui-styles')) return;
    var style=document.createElement('style');
    style.id='modern-ui-styles';
    style.textContent='\
.site-toplink{position:fixed;right:22px;bottom:22px;z-index:80;width:48px;height:48px;display:grid;place-items:center;border:1px solid rgba(223,230,239,.96);border-radius:50%;background:rgba(255,255,255,.94);color:#245b8a;font-size:1.25rem;font-weight:800;line-height:1;box-shadow:0 12px 30px rgba(20,32,51,.14);opacity:0;visibility:hidden;transform:translateY(8px);transition:opacity .2s ease,transform .2s ease,visibility .2s ease,background .2s ease,color .2s ease;-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);cursor:pointer}\
.site-toplink.is-visible{opacity:1;visibility:visible;transform:translateY(0)}\
.site-toplink:hover{background:#142033;color:#fff;border-color:#142033}\
.site-toplink:focus-visible,.mobile-nav-toggle:focus-visible{outline:3px solid rgba(36,91,138,.25);outline-offset:3px}\
.mobile-nav-toggle{display:none;margin-left:auto;width:44px;height:44px;border:1px solid #dfe6ef;border-radius:13px;background:rgba(255,255,255,.9);align-items:center;justify-content:center;gap:4px;flex-direction:column;cursor:pointer}\
.mobile-nav-toggle span{display:block;width:18px;height:2px;border-radius:2px;background:#34445a;transition:transform .2s ease,opacity .2s ease}\
.mobile-nav-toggle[aria-expanded="true"] span:nth-child(1){transform:translateY(6px) rotate(45deg)}\
.mobile-nav-toggle[aria-expanded="true"] span:nth-child(2){opacity:0}\
.mobile-nav-toggle[aria-expanded="true"] span:nth-child(3){transform:translateY(-6px) rotate(-45deg)}\
.mobile-nav-panel{display:none;position:absolute;top:100%;left:0;right:0;background:rgba(247,249,252,.98);border-bottom:1px solid #dfe6ef;box-shadow:0 16px 30px rgba(20,32,51,.08);padding:10px 20px 16px;-webkit-backdrop-filter:blur(18px);backdrop-filter:blur(18px)}\
.mobile-nav-panel.is-open{display:block}\
.mobile-nav-panel-inner{width:min(1160px,100%);margin:auto;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}\
.mobile-nav-panel a{display:block;padding:11px 13px;border:1px solid #e6ebf1;border-radius:12px;background:#fff;color:#34445a;font-size:.88rem;font-weight:700}\
.mobile-nav-panel a:hover{color:#245b8a;border-color:#cbd8e5}\
@media(max-width:940px){.topbar .navlinks{display:none}.mobile-nav-toggle{display:flex}.site-toplink{right:16px;bottom:16px}.topbar{overflow:visible}}\
@media(max-width:520px){.mobile-nav-panel-inner{grid-template-columns:1fr}.mobile-nav-panel{padding-left:12px;padding-right:12px}.site-toplink{right:14px;bottom:14px;width:44px;height:44px}}\
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.site-toplink,.mobile-nav-toggle span{transition:none}}';
    document.head.appendChild(style);
  }

  function ensureContactLink(){
    var desktop=document.querySelector('.topbar .navlinks');
    if(!desktop) return;
    var exists=Array.prototype.some.call(desktop.querySelectorAll('a'),function(a){return a.textContent.trim().toLowerCase()==='contact';});
    if(exists) return;
    var link=document.createElement('a');
    link.href='/hiroki_ishizaka/contact/';
    link.textContent='Contact';
    desktop.appendChild(link);
  }

  function initBackToTop(){
    if(document.querySelector('.site-toplink,.article-toplink')) return;
    var button=document.createElement('button');
    button.type='button';
    button.className='site-toplink';
    button.setAttribute('aria-label','Back to top');
    button.setAttribute('title','Back to top');
    button.textContent='↑';
    document.body.appendChild(button);

    function update(){button.classList.toggle('is-visible',window.scrollY>320);}
    button.addEventListener('click',function(){
      var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      window.scrollTo({top:0,behavior:reduce?'auto':'smooth'});
    });
    window.addEventListener('scroll',update,{passive:true});
    update();
  }

  function initMobileNav(){
    var header=document.querySelector('.topbar');
    var nav=header&&header.querySelector('.nav');
    var desktop=nav&&nav.querySelector('.navlinks');
    if(!header||!nav||!desktop||nav.querySelector('.mobile-nav-toggle')) return;

    var toggle=document.createElement('button');
    toggle.type='button';
    toggle.className='mobile-nav-toggle';
    toggle.setAttribute('aria-label','Open navigation menu');
    toggle.setAttribute('aria-expanded','false');
    toggle.setAttribute('aria-controls','mobile-site-nav');
    toggle.innerHTML='<span></span><span></span><span></span>';
    nav.appendChild(toggle);

    var panel=document.createElement('nav');
    panel.id='mobile-site-nav';
    panel.className='mobile-nav-panel';
    panel.setAttribute('aria-label','Mobile navigation');
    var inner=document.createElement('div');
    inner.className='mobile-nav-panel-inner';
    desktop.querySelectorAll('a').forEach(function(link){inner.appendChild(link.cloneNode(true));});
    panel.appendChild(inner);
    header.appendChild(panel);

    function close(){
      panel.classList.remove('is-open');
      toggle.setAttribute('aria-expanded','false');
      toggle.setAttribute('aria-label','Open navigation menu');
    }
    function open(){
      panel.classList.add('is-open');
      toggle.setAttribute('aria-expanded','true');
      toggle.setAttribute('aria-label','Close navigation menu');
    }
    toggle.addEventListener('click',function(){panel.classList.contains('is-open')?close():open();});
    inner.addEventListener('click',close);
    document.addEventListener('keydown',function(e){if(e.key==='Escape')close();});
    window.addEventListener('resize',function(){if(window.innerWidth>940)close();},{passive:true});
  }

  function init(){
    addSharedStyles();
    ensureContactLink();
    initMobileNav();
    initBackToTop();
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init);
  else init();
})();
