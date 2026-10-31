'use strict';
const test=require('node:test');
const assert=require('node:assert/strict');
const {matrix,apply,determinant,eigenspaceDimensionAtOne}=require('../blog/demos/linear-algebra-shear.js');
function close(x,y,eps=1e-12){assert.ok(Math.abs(x-y)<eps,String(x)+' !== '+String(y));}
test('matrix is precisely A(t)',()=>{
  for(const t of [-2,-.5,0,.3,2]) assert.deepEqual(matrix(t),[[1,t],[0,1]]);
});
test('standard-basis mapping matches mathematical definition',()=>{
  for(const t of [-2,-1,0,1,2]){
    assert.deepEqual(apply(t,[1,0]),[1,0]);
    assert.deepEqual(apply(t,[0,1]),[t,1]);
  }
});
test('determinant is 1, so unit area is preserved',()=>{
  for(const t of [-2,-1,.1,1,2])close(determinant(t),1);
});
test('t=0 has a 2D eigenspace; nonzero t has a 1D eigenspace',()=>{
  assert.equal(eigenspaceDimensionAtOne(0),2);
  for(const t of [-2,-.1,.1,2]) assert.equal(eigenspaceDimensionAtOne(t),1);
});
test('inverse shear: A(-t) A(t) x = x',()=>{
  for(const t of [-2,-.5,0,.5,2]) for(const x of [[1,2],[-3,4],[0,1]]){
    const y=apply(-t,apply(t,x));close(y[0],x[0]);close(y[1],x[1]);
  }
});
test('input errors are explicit',()=>{
  assert.throws(()=>matrix(Infinity),TypeError);
  assert.throws(()=>apply(1,[1,NaN]),TypeError);
});
test('all public functions reject invalid parameters',()=>{
  const functions=[matrix,determinant,eigenspaceDimensionAtOne,t=>apply(t,[1,2])];
  for(const t of [undefined,null,NaN,Infinity,-Infinity,'1',true]){
    for(const fn of functions) assert.throws(()=>fn(t),TypeError);
  }
});
test('apply rejects missing, non-array and incorrectly sized points',()=>{
  for(const point of [undefined,null,{},'12',[],[1],[1,2,3]]){
    assert.throws(()=>apply(1,point),TypeError);
  }
});
test('apply rejects sparse points even when a missing coordinate is inherited',()=>{
  const inherited=[,1];
  Object.setPrototypeOf(inherited,{0:2});
  for(const point of [Array(2),[,1],[1,,],inherited]){
    assert.throws(()=>apply(1,point),TypeError);
  }
});
test('apply rejects invalid values in either coordinate',()=>{
  for(const value of [undefined,null,NaN,Infinity,-Infinity,'1',true]){
    assert.throws(()=>apply(1,[value,1]),TypeError);
    assert.throws(()=>apply(1,[1,value]),TypeError);
  }
});
test('all 41 slider values agree with rank-nullity and preserve polygon area',()=>{
  const square=[[0,0],[1,0],[1,1],[0,1]];
  for(let step=-20;step<=20;step++){
    const t=step/10,A=matrix(t);
    const B=[[A[0][0]-1,A[0][1]],[A[1][0],A[1][1]-1]];
    const rank=B.every(row=>row.every(value=>value===0))?0:
      (B[0][0]*B[1][1]-B[0][1]*B[1][0]===0?1:2);
    assert.equal(eigenspaceDimensionAtOne(t),2-rank);
    const image=square.map(point=>apply(t,point));
    const doubledArea=image.reduce((sum,point,index)=>{
      const next=image[(index+1)%image.length];
      return sum+point[0]*next[1]-point[1]*next[0];
    },0);
    close(doubledArea/2,1);
    for(const point of square){
      const restored=apply(-t,apply(t,point));
      close(restored[0],point[0]);close(restored[1],point[1]);
    }
  }
});

const {createLesson}=require('../blog/demos/linear-algebra-shear.js');
test('a lesson starts without a prediction, answer or proof',()=>{
  const lesson=createLesson();
  assert.deepEqual(lesson.getState(),{t:1,prediction:null,result:null,proofStep:0});
});
test('dimension and diagonalizability predictions are assessed independently',()=>{
  for(const t of [0,1]) for(const dimension of [1,2]) for(const diagonalizable of [false,true]){
    const lesson=createLesson(t);
    lesson.predict(dimension,diagonalizable);
    const state=lesson.getState(),expectedDimension=t===0?2:1;
    assert.deepEqual(state.prediction,{dimension,diagonalizable});
    assert.deepEqual(state.result,{
      dimension:expectedDimension,diagonalizable:t===0,
      dimensionCorrect:dimension===expectedDimension,
      diagonalizableCorrect:diagonalizable===(t===0)
    });
  }
});
test('incomplete or invalid predictions do not reveal an answer',()=>{
  const lesson=createLesson();
  for(const dimension of [undefined,null,0,3,'1',NaN]){
    assert.throws(()=>lesson.predict(dimension,false),TypeError);
  }
  for(const diagonalizable of [undefined,null,'yes',0,1,NaN]){
    assert.throws(()=>lesson.predict(1,diagonalizable),TypeError);
  }
  assert.deepEqual(lesson.getState(),{t:1,prediction:null,result:null,proofStep:0});
});
test('proof is gated by prediction and advances through exactly three steps',()=>{
  const lesson=createLesson();
  assert.throws(()=>lesson.nextProofStep());
  lesson.predict(1,false);
  assert.throws(()=>lesson.predict(2,true));
  for(const step of [1,2,3,3]){
    lesson.nextProofStep();assert.equal(lesson.getState().proofStep,step);
  }
});
test('changing the parameter invalidates prediction, result and proof',()=>{
  const lesson=createLesson(0);
  lesson.predict(2,true);lesson.nextProofStep();
  lesson.setParameter(-.1);
  assert.deepEqual(lesson.getState(),{t:-.1,prediction:null,result:null,proofStep:0});
  lesson.predict(1,false);
  assert.equal(lesson.getState().result.dimensionCorrect,true);
});
test('reset returns to zero and starts a new unanswered prediction',()=>{
  const lesson=createLesson(2);
  lesson.predict(2,false);lesson.nextProofStep();
  lesson.reset();
  assert.deepEqual(lesson.getState(),{t:0,prediction:null,result:null,proofStep:0});
  assert.throws(()=>lesson.nextProofStep());
});
test('lesson snapshots cannot mutate a recorded prediction or result',()=>{
  const lesson=createLesson();lesson.predict(1,false);
  const snapshot=lesson.getState();
  for(const mutate of [()=>{snapshot.t=0;},()=>{snapshot.prediction.dimension=2;},()=>{snapshot.result.dimension=2;}]){
    try{mutate();}catch(error){assert.ok(error instanceof TypeError);}
  }
  assert.equal(lesson.getState().t,1);
  assert.equal(lesson.getState().prediction.dimension,1);
  assert.equal(lesson.getState().result.dimension,1);
  lesson.setParameter(0);
  assert.equal(snapshot.result.dimension,1);
});
test('lesson parameters must be finite numbers in the teaching interval',()=>{
  for(const value of [undefined,null,NaN,Infinity,-Infinity,'1',true]){
    if(value!==undefined)assert.throws(()=>createLesson(value),TypeError);
    assert.throws(()=>createLesson().setParameter(value),TypeError);
  }
  for(const value of [-2.1,2.1]){
    assert.throws(()=>createLesson(value),RangeError);
    assert.throws(()=>createLesson().setParameter(value),RangeError);
  }
  for(const value of [-2,0,2])assert.equal(createLesson(value).getState().t,value);
});

// The mathematical tests above need only Node.js. Set SHEAR_BROWSER_TESTS=1
// to additionally run real DOM/keyboard checks with Playwright and Chromium.
const browserChecks=process.env.SHEAR_BROWSER_TESTS==='1';
let browser,context,server,base;
test.before(async()=>{
  if(!browserChecks)return;
  const fs=require('node:fs'),http=require('node:http'),path=require('node:path');
  const root=path.resolve(__dirname,'..');
  server=http.createServer((request,response)=>{
    const pathname=decodeURIComponent(new URL(request.url,'http://localhost').pathname);
    const file=path.resolve(root,'.'+pathname);
    if(!file.startsWith(root+path.sep)){response.writeHead(403);response.end();return;}
    try{
      response.setHeader('Content-Type',file.endsWith('.js')?'text/javascript':file.endsWith('.css')?'text/css':'text/html; charset=utf-8');
      response.end(fs.readFileSync(file));
    }catch{response.writeHead(404);response.end();}
  });
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  base='http://127.0.0.1:'+server.address().port;
  const {chromium}=require('playwright');
  browser=await chromium.launch({executablePath:process.env.SHEAR_CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox']});
  context=await browser.newContext({viewport:{width:375,height:900}});
});
test.after(async()=>{
  if(browser)await browser.close();
  if(server)await new Promise(resolve=>server.close(resolve));
});
async function withLessonPage(check){
  const page=await context.newPage(),errors=[];
  page.on('pageerror',error=>errors.push(error.message));
  try{
    await page.goto(base+'/blog/demos/linear-algebra-shear.html');
    await check(page);
    assert.deepEqual(errors,[],'the lesson must not throw browser errors');
  }finally{await page.close();}
}
async function expectUnanswered(page){
  assert.equal(await page.locator('#observation').isVisible(),false);
  assert.equal(await page.locator('#proof').isVisible(),false);
  assert.equal(await page.locator('#dimension').textContent(),'');
  assert.equal(await page.locator('#verdict').textContent(),'');
  assert.equal(await page.locator('#prediction-form input:checked').count(),0);
  assert.equal(await page.locator('#prediction-form input:disabled').count(),0);
  assert.equal(await page.locator('[data-eigenspace]').count(),0);
  assert.equal(await page.locator('.proof-step:not([hidden])').count(),0);
}
async function predict(page,dimension,diagonalizable){
  await page.locator('input[name="dimension"][value="'+dimension+'"]').check();
  await page.locator('input[name="diagonalizable"][value="'+(diagonalizable?'yes':'no')+'"]').check();
  await page.locator('#confirm-prediction').click();
}
test('browser: prediction gates the answer and validates required accessible controls',{skip:!browserChecks},async()=>{
  await withLessonPage(async page=>{
    await expectUnanswered(page);
    assert.equal(await page.locator('#activity-status').getAttribute('role'),'status');
    for(const name of ['dimension','diagonalizable']){
      const radios=page.locator('input[name="'+name+'"]');
      assert.equal(await radios.count(),2);
      assert.equal(await radios.first().evaluate(e=>e.required),true);
      assert.ok(await radios.first().evaluate(e=>e.closest('fieldset').querySelector('legend').textContent.trim()));
    }
    await page.locator('#confirm-prediction').click();
    await expectUnanswered(page);
    assert.equal(await page.locator('#prediction-form').evaluate(e=>e.checkValidity()),false);
    assert.equal(await page.evaluate(()=>document.activeElement.name),'dimension');
    await predict(page,2,true);
    assert.equal(await page.locator('#observation').isVisible(),true);
    assert.equal(await page.locator('#proof').isVisible(),true);
    assert.equal(await page.locator('#dimension').textContent(),'1');
    assert.equal(await page.locator('#verdict').textContent(),'不可能');
    assert.ok((await page.locator('#prediction-feedback').textContent()).trim());
    assert.equal(await page.locator('#prediction-form input:disabled').count(),4);
    assert.equal(await page.locator('#confirm-prediction').isDisabled(),true);
  });
});
test('browser: parameter changes and reset clear prediction, geometry and proof',{skip:!browserChecks},async()=>{
  await withLessonPage(async page=>{
    await predict(page,1,false);
    await page.locator('#proof-next').click();
    await page.locator('#proof-next').click();
    assert.equal(await page.locator('.proof-step:not([hidden])').count(),2);
    await page.evaluate(()=>{const slider=document.getElementById('parameter');slider.value='0';slider.dispatchEvent(new Event('input',{bubbles:true}));});
    await expectUnanswered(page);
    await predict(page,2,true);
    assert.equal(await page.locator('#dimension').textContent(),'2');
    assert.equal(await page.locator('#verdict').textContent(),'可能');
    assert.equal(await page.locator('[data-eigenspace="plane"]').count(),1);
    await page.locator('#reset').click();
    assert.equal(await page.locator('#parameter').inputValue(),'0');
    await expectUnanswered(page);
  });
});
test('browser: arrow keys, Tab and Enter complete the prediction and proof flow',{skip:!browserChecks},async()=>{
  await withLessonPage(async page=>{
    await page.locator('#parameter').focus();
    await page.keyboard.press('ArrowLeft');
    assert.equal(await page.locator('#parameter').inputValue(),'0.9');
    await page.keyboard.press('Home');
    assert.equal(await page.locator('#parameter').inputValue(),'-2');
    await page.keyboard.press('End');
    assert.equal(await page.locator('#parameter').inputValue(),'2');
    await expectUnanswered(page);
    await page.locator('input[name="dimension"][value="1"]').focus();
    await page.keyboard.press('ArrowRight');
    assert.equal(await page.locator('input[name="dimension"][value="2"]').isChecked(),true);
    await page.keyboard.press('Tab');
    assert.equal(await page.evaluate(()=>document.activeElement.name),'diagonalizable');
    await page.keyboard.press('ArrowRight');
    assert.equal(await page.locator('input[name="diagonalizable"][value="no"]').isChecked(),true);
    await page.keyboard.press('Tab');
    assert.equal(await page.evaluate(()=>document.activeElement.id),'confirm-prediction');
    await page.keyboard.press('Enter');
    assert.equal(await page.locator('#observation').isVisible(),true);
    await page.locator('#proof-next').focus();
    for(const count of [1,2,3]){
      await page.keyboard.press('Enter');
      assert.equal(await page.locator('.proof-step:not([hidden])').count(),count);
    }
    assert.equal(await page.locator('#proof-next').isDisabled(),true);
    assert.equal(await page.getByRole('group',{name:'図の凡例'}).isVisible(),true);
    assert.equal(await page.getByRole('math').isVisible(),true);
    await page.locator('#reset').focus();await page.keyboard.press('Enter');
    await expectUnanswered(page);
  });
});
test('browser: all 41 parameters at four widths retain correct labels, eigenspaces and margins',{skip:!browserChecks},async()=>{
  await withLessonPage(async page=>{
    for(const width of [320,375,768,1440]){
      await page.setViewportSize({width,height:1000});
      const rows=await page.evaluate(()=>{
        const rows=[];
        for(let step=-20;step<=20;step++){
          const t=step/10,slider=document.getElementById('parameter'),form=document.getElementById('prediction-form');
          slider.value=String(t);slider.dispatchEvent(new Event('input',{bubbles:true}));
          const cleared=document.getElementById('observation').hidden&&document.getElementById('proof').hidden&&
            !form.querySelector('input:checked')&&!document.querySelector('[data-eigenspace]')&&
            !document.getElementById('dimension').textContent&&!document.getElementById('verdict').textContent;
          form.querySelector('input[name="dimension"][value="2"]').checked=true;
          form.querySelector('input[name="diagonalizable"][value="yes"]').checked=true;
          form.requestSubmit();
          const diagrams=['diagram-in','diagram-out'].map(id=>{
            const svg=document.getElementById(id),v=svg.viewBox.baseVal,polygon=svg.querySelector('polygon');
            const margins=[...polygon.points].flatMap(p=>[p.x-v.x,v.x+v.width-p.x,p.y-v.y,v.y+v.height-p.y]);
            return {id,margin:Math.min(...margins),title:!!svg.querySelector('title'),desc:!!svg.querySelector('desc'),
              vectors:[...svg.querySelectorAll('line[data-vector]')].map(e=>({name:e.dataset.vector,x:Number(e.getAttribute('x2')),y:Number(e.getAttribute('y2'))})),
              labels:[...svg.querySelectorAll('text')].map(e=>({text:e.textContent,box:{x:e.getBBox().x,y:e.getBBox().y,width:e.getBBox().width,height:e.getBBox().height}})),
              view:{x:v.x,y:v.y,width:v.width,height:v.height}};
          });
          rows.push({t,cleared,dimension:document.getElementById('dimension').textContent,verdict:document.getElementById('verdict').textContent,
            eigenspace:document.querySelector('[data-eigenspace]').dataset.eigenspace,pageWidth:document.documentElement.scrollWidth,diagrams});
        }
        return rows;
      });
      assert.equal(rows.length,41);
      for(const row of rows){
        assert.equal(row.cleared,true,'stale answer at '+row.t);
        assert.equal(row.dimension,row.t===0?'2':'1');
        assert.equal(row.verdict,row.t===0?'可能':'不可能');
        assert.equal(row.eigenspace,row.t===0?'plane':'line');
        assert.equal(row.pageWidth,width,'page overflow at '+width+' / '+row.t);
        for(const diagram of row.diagrams){
          assert.ok(diagram.margin>=24,'polygon margin at '+row.t);
          assert.equal(diagram.title,true);assert.equal(diagram.desc,true);
          assert.equal(diagram.vectors.length,2);
          const first=diagram.vectors.find(v=>v.name===(diagram.id==='diagram-in'?'e1':'Ae1'));
          const second=diagram.vectors.find(v=>v.name===(diagram.id==='diagram-in'?'e2':'Ae2'));
          assert.deepEqual([first.x,first.y],[48,0]);
          close(second.x,diagram.id==='diagram-in'?0:48*row.t);close(second.y,-48);
          assert.ok(diagram.labels.some(label=>/e[₁1]/.test(label.text)));
          assert.ok(diagram.labels.some(label=>/e[₂2]/.test(label.text)));
          for(const label of diagram.labels){
            assert.ok(label.box.x>=diagram.view.x&&label.box.y>=diagram.view.y,'label starts outside: '+label.text);
            assert.ok(label.box.x+label.box.width<=diagram.view.x+diagram.view.width&&label.box.y+label.box.height<=diagram.view.y+diagram.view.height,'label ends outside: '+label.text);
          }
        }
      }
    }
  });
});
