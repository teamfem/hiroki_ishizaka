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
