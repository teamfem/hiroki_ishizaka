'use strict';
const test=require('node:test');
const assert=require('node:assert/strict');
const {parameter,coefficient,cost,projection,createLesson}=require('../blog/demos/linear-algebra-projection.js');
const near=(a,b,e=1e-10)=>assert.ok(Math.abs(a-b)<=e, a+' not close to '+b);
test('projection formula is (2+t)/(1+t^2)',()=>{
 for(const t of [-2,-.5,0,.5,2])near(coefficient(t),(2+t)/(1+t*t));
});
test('residual is orthogonal to the line for all slider values',()=>{
 for(let k=-20;k<=20;k++){
  const t=k/10,p=projection(t);
  near(p.residual[0]+t*p.residual[1],0);
  near(p.point[0],p.coefficient);
  near(p.point[1],t*p.coefficient);
 }
});
test('Pythagorean identity checks the global minimum, not just stationary point',()=>{
 for(let k=-20;k<=20;k++){
  const t=k/10,p=projection(t);
  for(const x of [-1,0,.2,1,2,3]){
   near(cost(t,x),p.squaredResidual+(x-p.coefficient)**2*(1+t*t));
   assert.ok(cost(t,x)+1e-10>=p.squaredResidual);
  }
 }
});
test('t=1/2 reproduces b exactly, t=-2 projects to origin',()=>{
 near(projection(.5).squaredResidual,0);
 near(projection(.5).coefficient,2);
 near(projection(-2).coefficient,0);
});
test('invalid parameters and guesses are refused',()=>{
 for(const x of [NaN,Infinity,'1',undefined,null])assert.throws(()=>parameter(x),TypeError);
 for(const x of [-2.1,2.1])assert.throws(()=>parameter(x),RangeError);
 for(const x of [NaN,Infinity,'2',undefined,null])assert.throws(()=>cost(0,x),TypeError);
 assert.throws(()=>createLesson().predict(4),RangeError);
});
test('prediction cannot be answered without the student committing',()=>{
 const s=createLesson();
 assert.equal(s.getState().result,null);
 assert.throws(()=>s.nextProof());
 s.predict(1.2);
 near(s.getState().guess,1.2);
 assert.throws(()=>s.predict(1));
});
test('t change resets prediction, answer, proof progress',()=>{
 const s=createLesson(.5);
 s.predict(2);s.nextProof();s.nextProof();
 s.setT(1);
 assert.equal(s.getState().guess,null);
 assert.equal(s.getState().result,null);
 assert.equal(s.getState().proofStep,0);
 assert.throws(()=>s.nextProof());
});
test('three proof stages terminate; reset starts at t=1',()=>{
 const s=createLesson(-1);
 s.predict(0);
 for(let i=0;i<5;i++)s.nextProof();
 assert.equal(s.getState().proofStep,3);
 s.reset();
 assert.equal(s.getState().t,1);
 assert.equal(s.getState().result,null);
});
const browserChecks=process.env.PROJECTION_BROWSER_TESTS==='1';
let browser,server,base;
test.before(async()=>{
 if(!browserChecks)return;
 const fs=require('node:fs'),http=require('node:http'),path=require('node:path');
 const root=path.resolve(__dirname,'..');
 server=http.createServer((req,res)=>{
  const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
  const file=path.resolve(root,'.'+pathname);
  if(!file.startsWith(root+path.sep)){res.writeHead(403).end();return;}
  try{res.setHeader('Content-Type',file.endsWith('.js')?'text/javascript':'text/html; charset=utf-8');res.end(fs.readFileSync(file));}
  catch{res.writeHead(404);res.end();}
 });
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 base='http://127.0.0.1:'+server.address().port;
 const {chromium}=require('playwright');
 browser=await chromium.launch({executablePath:process.env.PROJECTION_CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox']});
});
test.after(async()=>{if(browser)await browser.close();if(server)await new Promise(r=>server.close(r));});
async function pageTest(fn){
 const page=await browser.newPage(),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 try{await page.goto(base+'/blog/demos/linear-algebra-projection.html');await fn(page);assert.deepEqual(errors,[]);}
 finally{await page.close();}
}
test('browser: prediction gates answers and proof, reset clears them',{skip:!browserChecks},async()=>{
 await pageTest(async page=>{
  assert.equal(await page.locator('#observation').isVisible(),false);
  assert.equal(await page.locator('#proof').isVisible(),false);
  await page.locator('#confirm').click();
  assert.equal(await page.locator('#observation').isVisible(),true);
  assert.equal(await page.locator('#proof').isVisible(),true);
  assert.equal(await page.locator('.proof-step:not([hidden])').count(),0);
  await page.locator('#proof-next').click();
  assert.equal(await page.locator('.proof-step:not([hidden])').count(),1);
  await page.locator('#reset').click();
  assert.equal(await page.locator('#observation').isVisible(),false);
  assert.equal(await page.locator('.proof-step:not([hidden])').count(),0);
 });
});
test('browser: all 41 parameters preserve layout and math',{skip:!browserChecks},async()=>{
 await pageTest(async page=>{
  for(const width of [320,375,768,1440]){
   await page.setViewportSize({width,height:1000});
   for(let k=-20;k<=20;k++){
    const t=k/10;
    await page.locator('#t').evaluate((el,value)=>{el.value=String(value);el.dispatchEvent(new Event('input',{bubbles:true}));},t);
    assert.equal(await page.locator('#observation').isVisible(),false);
    await page.locator('#confirm').click();
    assert.equal(await page.locator('#observation').isVisible(),true);
    assert.ok(await page.locator('svg [data-scene]').count());
    near(Number(await page.locator('#optimal').textContent()),coefficient(t),.0001);
    const scroll=await page.evaluate(()=>document.documentElement.scrollWidth);
    assert.ok(scroll<=width,'horizontal overflow at t='+t+' width='+width);
   }
  }
 });
});
test('browser: keyboard slider and proof progression',{skip:!browserChecks},async()=>{
 await pageTest(async page=>{
  await page.locator('#t').focus();await page.keyboard.press('ArrowRight');
  assert.equal(await page.locator('#t').inputValue(),'1.1');
  await page.locator('#guess').focus();await page.keyboard.press('ArrowRight');
  assert.equal(await page.locator('#guess').inputValue(),'0.1');
  await page.locator('#confirm').focus();await page.keyboard.press('Enter');
  await page.locator('#proof-next').focus();
  for(let i=1;i<=3;i++){await page.keyboard.press('Enter');assert.equal(await page.locator('.proof-step:not([hidden])').count(),i);}
  assert.equal(await page.locator('#proof-next').isDisabled(),true);
 });
});
