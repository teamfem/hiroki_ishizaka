(function(){
  'use strict';

  function initBackToTop(){
    if(document.querySelector('.site-toplink,.article-toplink')) return;

    var style=document.createElement('style');
    style.textContent='\
.site-toplink{position:fixed;right:22px;bottom:22px;z-index:80;width:48px;height:48px;display:grid;place-items:center;border:1px solid rgba(223,230,239,.96);border-radius:50%;background:rgba(255,255,255,.94);color:#245b8a;font-size:1.25rem;font-weight:800;line-height:1;box-shadow:0 12px 30px rgba(20,32,51,.14);opacity:0;visibility:hidden;transform:translateY(8px);transition:opacity .2s ease,transform .2s ease,visibility .2s ease,background .2s ease,color .2s ease;-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);cursor:pointer}\
.site-toplink.is-visible{opacity:1;visibility:visible;transform:translateY(0)}\
.site-toplink:hover{background:#142033;color:#fff;border-color:#142033}\
.site-toplink:focus-visible{outline:3px solid rgba(36,91,138,.25);outline-offset:3px}\
@media(max-width:620px){.site-toplink{right:14px;bottom:14px;width:44px;height:44px}}\
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.site-toplink{transition:none}}';
    document.head.appendChild(style);

    var button=document.createElement('button');
    button.type='button';
    button.className='site-toplink';
    button.setAttribute('aria-label','Back to top');
    button.setAttribute('title','Back to top');
    button.textContent='↑';
    document.body.appendChild(button);

    function update(){
      button.classList.toggle('is-visible',window.scrollY>320);
    }
    button.addEventListener('click',function(){
      var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      window.scrollTo({top:0,behavior:reduce?'auto':'smooth'});
    });
    window.addEventListener('scroll',update,{passive:true});
    update();
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',initBackToTop);
  else initBackToTop();
})();
