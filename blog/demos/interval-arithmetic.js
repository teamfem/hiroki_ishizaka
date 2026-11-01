/* Episode 03: interval dependency and idealised wrapping.
   This is NOT an IEEE 1788 / outward-rounded validated interval library.
   Exact real-number formulas are analysed mathematically; SVG uses binary64. */
(function(root){
 'use strict';
 function radius(r){
  if(!Number.isFinite(r))throw new TypeError('r must be finite');
  if(r<0||r>2)throw new RangeError('r must be in [0,2]');
  return r;
 }
 function steps(n){
  if(!Number.isInteger(n))throw new TypeError('n must be an integer');
  if(n<0||n>4)throw new RangeError('n must be between 0 and 4');
  return n;
 }
 function intervalSubtract(x,y){
  if(!Array.isArray(x)||!Array.isArray(y)||x.length!==2||y.length!==2||
    !Object.prototype.hasOwnProperty.call(x,0)||!Object.prototype.hasOwnProperty.call(x,1)||
    !Object.prototype.hasOwnProperty.call(y,0)||!Object.prototype.hasOwnProperty.call(y,1)||
    !x.every(Number.isFinite)||!y.every(Number.isFinite))throw new TypeError('finite interval endpoints required');
  if(x[0]>x[1]||y[0]>y[1])throw new RangeError('interval endpoints reversed');
  return [x[0]-y[1],x[1]-y[0]];
 }
 function dependency(r){
  radius(r);
  return {input:[0,r],independent:intervalSubtract([0,r],[0,r]),sameVariable:[0,0],overestimationWidth:2*r};
 }
 function wrapping(n){
  steps(n);
  const halfWidth=2**(n/2),theta=n*Math.PI/4;
  const original=[[-1,-1],[1,-1],[1,1],[-1,1]];
  const corners=original.map(([x,y])=>[Math.cos(theta)*x-Math.sin(theta)*y,
                                         Math.sin(theta)*x+Math.cos(theta)*y]);
  return {n,halfWidth,boxArea:4*(2**n),trueArea:4,ratio:2**n,corners};
 }
 function createLesson(){
  let r=1,n=2,dependencyGuess=null,wrapGuess=null;
  function getState(){return Object.freeze({r,n,dependencyGuess,wrapGuess,
      dependencyResult:dependencyGuess===null?null:Object.freeze({correct:dependencyGuess==='zero'?(r===0):r>0,data:dependency(r)}),
      wrapResult:wrapGuess===null?null:Object.freeze({correct:wrapGuess===(n===0?'same':'increase'),data:wrapping(n)})});}
  function setRadius(value){r=radius(value);dependencyGuess=null;return getState();}
  function setSteps(value){n=steps(value);wrapGuess=null;return getState();}
  function predictDependency(choice){
   if(!['zero','wide'].includes(choice))throw new TypeError('invalid dependency choice');
   if(dependencyGuess!==null)throw new Error('prediction already made');
   dependencyGuess=choice;return getState();
  }
  function predictWrapping(choice){
   if(!['same','increase'].includes(choice))throw new TypeError('invalid wrapping choice');
   if(wrapGuess!==null)throw new Error('prediction already made');
   wrapGuess=choice;return getState();
  }
  function reset(){r=1;n=2;dependencyGuess=null;wrapGuess=null;return getState();}
  return Object.freeze({getState,setRadius,setSteps,predictDependency,predictWrapping,reset});
 }
 function mount(doc){
  const byId=id=>doc.getElementById(id);
  if(!byId('dependency-form')||byId('dependency-form').dataset.mounted)return null;
  byId('dependency-form').dataset.mounted='true';
  const lesson=createLesson();
  const NS='http://www.w3.org/2000/svg';
  const e=(tag,attrs,parent)=>{const x=doc.createElementNS(NS,tag);
    for(const [k,v] of Object.entries(attrs))x.setAttribute(k,String(v));parent.appendChild(x);return x;};
  function depDraw(r){
   const svg=byId('dependency-svg');
   svg.querySelectorAll('[data-generated]').forEach(x=>x.remove());
   const layer=e('g',{'data-generated':''},svg);
   e('line',{x1:45,y1:75,x2:555,y2:75,stroke:'#597083','stroke-width':2},layer);
   for(let i=-2;i<=2;i++){
    let x=300+110*i;
    e('line',{x1:x,y1:69,x2:x,y2:81,stroke:'#597083'},layer);
    const label=e('text',{x,y:101,'text-anchor':'middle','font-size':14,fill:'#38536a'},layer);
    label.textContent=String(i);
   }
   const a=300-110*r,b=300+110*r;
   e('line',{x1:a,y1:54,x2:b,y2:54,stroke:'#c47a24','stroke-width':12,'stroke-linecap':'round'},layer);
   e('circle',{cx:300,cy:75,r:7,fill:'#167b9d'},layer);
   const desc=svg.querySelector('desc');
   if(desc)desc.textContent='橙色の区間演算結果は ['+(-r).toFixed(2)+','+r.toFixed(2)+']。青い点は同じ変数 x-x の真の値域 {0}。';
  }
  function wrapDraw(n){
   const data=wrapping(n),svg=byId('wrapping-svg');
   svg.querySelectorAll('[data-generated]').forEach(x=>x.remove());
   const layer=e('g',{'data-generated':''},svg);
   const s=130/data.halfWidth;
   e('line',{x1:-160,y1:0,x2:160,y2:0,stroke:'#a8b9c6'},layer);
   e('line',{x1:0,y1:-160,x2:0,y2:160,stroke:'#a8b9c6'},layer);
   e('rect',{x:-130,y:-130,width:260,height:260,fill:'#e9a45b','fill-opacity':.11,
      stroke:'#be702b','stroke-width':3,'stroke-dasharray':'7 5'},layer);
   const poly=data.corners.map(p=>(s*p[0])+','+(-s*p[1])).join(' ');
   e('polygon',{points:poly,fill:'#3287af','fill-opacity':.32,stroke:'#176d9a','stroke-width':3},layer);
   const desc=svg.querySelector('desc');
   if(desc)desc.textContent=n+'回回転後の真の正方形（青、面積4）と、毎回軸平行な区間ボックスで囲み直した結果（橙、面積'+data.boxArea+'）。';
  }
  function render(){
   const s=lesson.getState(),hasDep=!!s.dependencyResult,hasWrap=!!s.wrapResult;
   byId('r').value=String(s.r);byId('r-output').textContent=s.r.toFixed(2);
   byId('n').value=String(s.n);byId('n-output').textContent=String(s.n);
   byId('dependency-answer').hidden=!hasDep;byId('wrapping-answer').hidden=!hasWrap;
   byId('dep-confirm').disabled=hasDep;byId('wrap-confirm').disabled=hasWrap;
   for(const input of byId('dependency-form').querySelectorAll('input'))input.disabled=hasDep;
   for(const input of byId('wrapping-form').querySelectorAll('input'))input.disabled=hasWrap;
   if(!hasDep)byId('dependency-form').reset();
   if(!hasWrap)byId('wrapping-form').reset();
   if(hasDep){
    const d=s.dependencyResult.data;
    byId('dep-prediction').textContent=s.dependencyResult.correct?'予想は一致しました。':'予想は一致しませんでした。';
    byId('dep-interval').textContent='['+(-s.r).toFixed(2)+', '+s.r.toFixed(2)+']';
    byId('dep-width').textContent=d.overestimationWidth.toFixed(2);
    depDraw(s.r);
   }else byId('dependency-svg').querySelectorAll('[data-generated]').forEach(x=>x.remove());
   if(hasWrap){
    const d=s.wrapResult.data;
    byId('wrap-prediction').textContent=s.wrapResult.correct?'予想は一致しました。':'予想は一致しませんでした。';
    byId('wrap-area').textContent=String(d.boxArea);
    byId('wrap-ratio').textContent=String(d.ratio);
    wrapDraw(s.n);
   }else byId('wrapping-svg').querySelectorAll('[data-generated]').forEach(x=>x.remove());
  }
  byId('r').addEventListener('input',()=>{lesson.setRadius(Number(byId('r').value));render();byId('dep-status').textContent='rを変更しました。再度予想してください。';});
  byId('n').addEventListener('input',()=>{lesson.setSteps(Number(byId('n').value));render();byId('wrap-status').textContent='回数を変更しました。再度予想してください。';});
  byId('dependency-form').addEventListener('submit',ev=>{
   ev.preventDefault();const picked=byId('dependency-form').querySelector('input:checked');
   if(!picked)return;
   lesson.predictDependency(picked.value);render();
   byId('dep-status').textContent='予想を確定しました。結果と証明を確認してください。';
   byId('dependency-title').focus();
  });
  byId('wrapping-form').addEventListener('submit',ev=>{
   ev.preventDefault();const picked=byId('wrapping-form').querySelector('input:checked');
   if(!picked)return;
   lesson.predictWrapping(picked.value);render();
   byId('wrap-status').textContent='予想を確定しました。結果と証明を確認してください。';
   byId('wrapping-title').focus();
  });
  byId('reset').addEventListener('click',()=>{
   lesson.reset();render();byId('dep-status').textContent='初期値に戻しました。';byId('wrap-status').textContent='初期値に戻しました。';
  });
  render();return lesson;
 }
 const api=Object.freeze({intervalSubtract,dependency,wrapping,createLesson,mount});
 if(typeof module!=='undefined'&&module.exports)module.exports=api;
 if(root){root.IntervalLesson=api;
  const ready=()=>mount(root.document);
  if(root.document.readyState==='loading')root.document.addEventListener('DOMContentLoaded',ready);else ready();
 }
})(typeof window!=='undefined'?window:undefined);
