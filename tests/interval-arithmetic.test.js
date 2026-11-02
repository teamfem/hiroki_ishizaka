'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const {intervalSubtract,dependency,wrapping,createLesson}=require('../blog/demos/interval-arithmetic.js');
const near=(a,b,e=1e-10)=>assert.ok(Math.abs(a-b)<=e,a+' != '+b);
test('interval subtraction is the hull of independent differences',()=>{
 assert.deepEqual(intervalSubtract([0,1],[0,1]),[-1,1]);
 assert.deepEqual(intervalSubtract([-2,1],[3,4]),[-6,-2]);
});
test('same-variable x-x has true range {0} but natural interval result [-r,r]',()=>{
 for(let k=0;k<=8;k++){
  const r=k/4,d=dependency(r);
  assert.deepEqual(d.input,[0,r]);
  near(d.independent[0],-r);
  near(d.independent[1],r); // +0 と -0 の符号差は集合としての区間に影響しない。
  assert.deepEqual(d.sameVariable,[0,0]);
  near(d.overestimationWidth,2*r);
 }
});
test('invalid interval endpoints are refused',()=>{
 for(const v of [[],[1],[2,1,0],[NaN,1],Array(2),[undefined,2],[0,Infinity]]){
  assert.throws(()=>intervalSubtract(v,[0,1]),TypeError);
 }
 assert.throws(()=>intervalSubtract([2,1],[0,1]),RangeError);
 assert.throws(()=>dependency(-1),RangeError);
 assert.throws(()=>dependency(NaN),TypeError);
});
test('wrapping box area grows by 2 each step while true area stays 4',()=>{
 for(let n=0;n<=4;n++){
  const w=wrapping(n);
  near(w.halfWidth,Math.sqrt(2)**n);
  assert.equal(w.trueArea,4);
  assert.equal(w.boxArea,4*2**n);
  assert.equal(w.ratio,2**n);
 }
});
test('rotated true square has area 4 and lies inside computed box',()=>{
 for(let n=0;n<=4;n++){
  const w=wrapping(n),poly=w.corners;
  const doubleArea=poly.reduce((sum,p,i)=>{const q=poly[(i+1)%4];return sum+p[0]*q[1]-p[1]*q[0];},0);
  near(doubleArea,8);
  for(const p of poly)for(const x of p)assert.ok(Math.abs(x)<=w.halfWidth+1e-12);
 }
});
test('wrapping step count accepts only 0..4 integers',()=>{
 for(const n of [undefined,NaN,Infinity,1.5,'1'])assert.throws(()=>wrapping(n),TypeError);
 for(const n of [-1,5])assert.throws(()=>wrapping(n),RangeError);
});
test('both predictions are hidden initially and become available only after confirmation',()=>{
 const l=createLesson();
 assert.equal(l.getState().dependencyResult,null);
 assert.equal(l.getState().wrapResult,null);
 l.predictDependency('wide');l.predictWrapping('increase');
 assert.equal(l.getState().dependencyResult.correct,true);
 assert.equal(l.getState().wrapResult.correct,true);
 assert.throws(()=>l.predictDependency('wide'));
 assert.throws(()=>l.predictWrapping('increase'));
});
test('each parameter reset invalidates its own answer; full reset invalidates both',()=>{
 const l=createLesson();
 l.predictDependency('wide');l.predictWrapping('increase');
 l.setRadius(0);
 assert.equal(l.getState().dependencyResult,null);
 assert.ok(l.getState().wrapResult);
 l.setSteps(0);
 assert.equal(l.getState().wrapResult,null);
 l.predictDependency('zero');l.predictWrapping('same');
 assert.equal(l.getState().dependencyResult.correct,true);
 assert.equal(l.getState().wrapResult.correct,true);
 l.reset();
 assert.equal(l.getState().r,1);assert.equal(l.getState().n,2);
 assert.equal(l.getState().dependencyResult,null);assert.equal(l.getState().wrapResult,null);
});
test('edge cases r=0 and n=0 are scored as current-value propositions',()=>{
 const d0=createLesson();d0.setRadius(0);d0.predictDependency('zero');
 assert.equal(d0.getState().dependencyResult.correct,true);
 const d1=createLesson();d1.setRadius(0);d1.predictDependency('wide');
 assert.equal(d1.getState().dependencyResult.correct,false);
 const d2=createLesson();d2.setRadius(.25);d2.predictDependency('wide');
 assert.equal(d2.getState().dependencyResult.correct,true);
 const w0=createLesson();w0.setSteps(0);w0.predictWrapping('same');
 assert.equal(w0.getState().wrapResult.correct,true);
 const w1=createLesson();w1.setSteps(0);w1.predictWrapping('increase');
 assert.equal(w1.getState().wrapResult.correct,false);
 const w2=createLesson();w2.setSteps(1);w2.predictWrapping('increase');
 assert.equal(w2.getState().wrapResult.correct,true);
});
test('prediction input validation is explicit',()=>{
 const l=createLesson();
 assert.throws(()=>l.predictDependency('incorrect'),TypeError);
 assert.throws(()=>l.predictWrapping('incorrect'),TypeError);
});
const browserChecks=process.env.INTERVAL_BROWSER_TESTS==='1';
let browser,server,base;
test.before(async()=>{
 if(!browserChecks)return;
 const fs=require('node:fs'),http=require('node:http'),path=require('node:path'),root=path.resolve(__dirname,'..');
 server=http.createServer((req,res)=>{
  const pathName=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
  const filename=path.resolve(root,'.'+pathName);
  if(!filename.startsWith(root+path.sep)){res.writeHead(403).end();return;}
  try{res.setHeader('Content-Type',filename.endsWith('.js')?'text/javascript':'text/html; charset=utf-8');res.end(fs.readFileSync(filename));}
  catch{res.writeHead(404);res.end();}
 });
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 base='http://127.0.0.1:'+server.address().port;
 const {chromium}=require('playwright');
 browser=await chromium.launch({executablePath:process.env.INTERVAL_CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox']});
});
test.after(async()=>{if(browser)await browser.close();if(server)await new Promise(r=>server.close(r));});
async function withPage(fn){
 const page=await browser.newPage(),errors=[];page.on('pageerror',err=>errors.push(err.message));
 try{await page.goto(base+'/blog/demos/interval-arithmetic.html');await fn(page);assert.deepEqual(errors,[]);}
 finally{await page.close();}
}
test('browser: answers remain hidden until each prediction',{skip:!browserChecks},async()=>{
 await withPage(async page=>{
  assert.equal(await page.locator('#dependency-answer').isVisible(),false);
  assert.equal(await page.locator('#wrapping-answer').isVisible(),false);
  await page.locator('#dependency-form input[value="wide"]').check();
  await page.locator('#dep-confirm').click();
  assert.equal(await page.locator('#dependency-answer').isVisible(),true);
  assert.equal(await page.locator('#wrapping-answer').isVisible(),false);
  await page.locator('#wrapping-form input[value="increase"]').check();
  await page.locator('#wrap-confirm').click();
  assert.equal(await page.locator('#wrapping-answer').isVisible(),true);
  await page.locator('#reset').click();
  assert.equal(await page.locator('#dependency-answer').isVisible(),false);
  assert.equal(await page.locator('#wrapping-answer').isVisible(),false);
 });
});
test('browser: interval radius cases and all wrapping steps at mobile and desktop widths',{skip:!browserChecks},async()=>{
 await withPage(async page=>{
  for(const width of [320,375,768,1440]){
   await page.setViewportSize({width,height:900});
   for(let k=0;k<=8;k++){
    const r=k/4;
    await page.locator('#r').evaluate((el,v)=>{el.value=String(v);el.dispatchEvent(new Event('input',{bubbles:true}));},r);
    assert.equal(await page.locator('#dependency-answer').isVisible(),false);
    await page.locator('#dependency-form input[value="'+(r===0?'zero':'wide')+'"]').check();
    await page.locator('#dep-confirm').click();
    assert.match(await page.locator('#dep-prediction').textContent(),/一致しました/);
    near(Number(await page.locator('#dep-width').textContent()),2*r);
    assert.ok(await page.locator('#dependency-svg [data-generated]').count());
    assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth)<=width);
   }
   for(let n=0;n<=4;n++){
    await page.locator('#n').evaluate((el,v)=>{el.value=String(v);el.dispatchEvent(new Event('input',{bubbles:true}));},n);
    assert.equal(await page.locator('#wrapping-answer').isVisible(),false);
    await page.locator('#wrapping-form input[value="'+(n===0?'same':'increase')+'"]').check();
    await page.locator('#wrap-confirm').click();
    assert.match(await page.locator('#wrap-prediction').textContent(),/一致しました/);
    assert.equal(Number(await page.locator('#wrap-area').textContent()),4*2**n);
    assert.match(await page.locator('#wrap-scale').textContent(),/縮尺が変わります/);
    assert.ok(await page.locator('#wrapping-svg polygon').count());
    assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth)<=width);
   }
  }
 });
});
