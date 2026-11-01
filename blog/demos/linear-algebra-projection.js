/* Episode 02: orthogonal projection onto span((1,t)^T).
   Exact real-number identities are explained in the article; the browser uses
   ordinary binary64 arithmetic for illustrating the geometry, not certification. */
(function(root){
  'use strict';
  const b=Object.freeze([2,1]);
  function parameter(t){
    if(!Number.isFinite(t))throw new TypeError('t must be finite');
    if(t < -2 || t > 2)throw new RangeError('t must belong to [-2,2]');
    return t;
  }
  function coefficient(t){
    parameter(t);
    return (2+t)/(1+t*t);
  }
  function cost(t,x){
    parameter(t);
    if(!Number.isFinite(x))throw new TypeError('coefficient must be finite');
    return (x-2)**2+(t*x-1)**2;
  }
  function projection(t){
    parameter(t);
    const x=coefficient(t),p=[x,t*x],r=[b[0]-p[0],b[1]-p[1]];
    return {coefficient:x,point:p,residual:r,normalDot:r[0]+t*r[1],squaredResidual:r[0]**2+r[1]**2};
  }
  function createLesson(initialT=1){
    let t=parameter(initialT),guess=null,result=null,step=0;
    function getState(){return Object.freeze({t,guess,result:result&&Object.freeze({...result}),proofStep:step});}
    function setT(value){t=parameter(value);guess=null;result=null;step=0;return getState();}
    function predict(value){
      if(!Number.isFinite(value)||value < -1||value > 3)throw new RangeError('guess must be in [-1,3]');
      if(result)throw new Error('change t or reset before another prediction');
      guess=value;
      const p=projection(t);
      result={optimal:p.coefficient,optimalCost:p.squaredResidual,guessCost:cost(t,value),
        residualDot:p.normalDot};
      return getState();
    }
    function nextProof(){if(!result)throw new Error('predict first');step=Math.min(3,step+1);return getState();}
    function reset(){return setT(1);}
    return Object.freeze({getState,setT,predict,nextProof,reset});
  }
  function mount(doc){
    const byId=id=>doc.getElementById(id),form=byId('prediction-form');
    if(!form||form.dataset.mounted)return null;
    form.dataset.mounted='true';
    const lesson=createLesson(Number(byId('t').value));
    const ns='http://www.w3.org/2000/svg',svg=byId('drawing'),S=23;
    function elt(tag,attrs,parent,value){
      const n=doc.createElementNS(ns,tag);
      for(const [k,v] of Object.entries(attrs))n.setAttribute(k,String(v));
      if(value!==undefined)n.textContent=value;
      parent.appendChild(n);return n;
    }
    function xy(p){return [p[0]*S,-p[1]*S];}
    function line(group,p,q,color,width,dash){
      const a=xy(p),c=xy(q);
      elt('line',{x1:a[0],y1:a[1],x2:c[0],y2:c[1],stroke:color,'stroke-width':width||2,
        'stroke-dasharray':dash||''},group);
    }
    function point(group,p,color,text,dx=8,dy=-8){
      const q=xy(p);
      elt('circle',{cx:q[0],cy:q[1],r:4,fill:color},group);
      elt('text',{x:q[0]+dx,y:q[1]+dy,fill:color,'font-size':12,'font-weight':700},group,text);
    }
    function draw(){
      const old=svg.querySelector('[data-scene]');if(old)old.remove();
      const state=lesson.getState();
      if(!state.result)return;
      const t=state.t,alpha=state.guess,p=projection(t).point,q=[alpha,t*alpha];
      const scene=elt('g',{'data-scene':''},svg);
      line(scene,[-7.3,0],[7.3,0],'#a5b0ba',1);
      line(scene,[0,-7.3],[0,7.3],'#a5b0ba',1);
      line(scene,[-3.3,-3.3*t],[3.3,3.3*t],'#326f9c',2.5);
      line(scene,q,b,'#c27a28',2.3,'6 4');
      line(scene,p,b,'#1a845d',3);
      point(scene,[0,0],'#536271','O',8,16);
      point(scene,b,'#263c57','b',10,-8);
      point(scene,q,'#c27a28','q',10,17);
      point(scene,p,'#1a845d','p',10,-10);
      const desc=svg.querySelector('desc');
      if(desc)desc.textContent='直線 span((1,'+t.toFixed(1)+')) 上の候補点 q と直交射影 p、固定ベクトル b=(2,1)。緑色の線分は直交残差、橙色の破線は候補残差です。';
    }
    function render(){
      const s=lesson.getState(),show=!!s.result;
      byId('t').value=String(s.t);
      byId('t-output').textContent=s.t.toFixed(1);
      byId('guess').value=show?String(s.guess):'0';
      byId('guess-output').textContent=Number(byId('guess').value).toFixed(1);
      byId('observation').hidden=!show;
      byId('proof').hidden=!show;
      byId('confirm').disabled=show;
      byId('guess').disabled=show;
      byId('optimal').textContent=show?s.result.optimal.toFixed(4):'';
      byId('cost-guess').textContent=show?s.result.guessCost.toFixed(4):'';
      byId('cost-best').textContent=show?s.result.optimalCost.toFixed(4):'';
      byId('orthogonality').textContent=show?s.result.residualDot.toExponential(2):'';
      for(const el of doc.querySelectorAll('.proof-step'))el.hidden=!show||Number(el.dataset.step)>s.proofStep;
      byId('proof-next').disabled=!show||s.proofStep===3;
      byId('proof-progress').textContent=show?'証明 '+s.proofStep+'/3 段階':'';
      if(show)draw();
      else{const old=svg.querySelector('[data-scene]');if(old)old.remove();}
    }
    function restart(message){lesson.setT(Number(byId('t').value));render();byId('status').textContent=message;}
    byId('t').addEventListener('input',()=>restart('tを変更しました。新しい値で予想してください。'));
    byId('guess').addEventListener('input',()=>{byId('guess-output').textContent=Number(byId('guess').value).toFixed(1);});
    byId('reset').addEventListener('click',()=>{lesson.reset();render();byId('status').textContent='初期値 t=1 に戻しました。';});
    form.addEventListener('submit',e=>{
      e.preventDefault();
      lesson.predict(Number(byId('guess').value));
      render();
      byId('status').textContent='予想を確定しました。観察と証明へ進みましょう。';
      byId('observation-title').focus();
    });
    byId('proof-next').addEventListener('click',()=>{lesson.nextProof();render();});
    render();
    return lesson;
  }
  const api=Object.freeze({parameter,coefficient,cost,projection,createLesson,mount});
  if(typeof module!=='undefined'&&module.exports)module.exports=api;
  if(root){
    root.ProjectionLesson=api;
    const ready=()=>mount(root.document);
    if(root.document.readyState==='loading')root.document.addEventListener('DOMContentLoaded',ready);
    else ready();
  }
})(typeof window!=='undefined'?window:undefined);
