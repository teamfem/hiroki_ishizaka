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
