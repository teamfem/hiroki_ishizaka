#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const root = path.join(process.cwd(), 'blog', 'posts');
function strip(s){return s.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi,'').replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi,'').replace(/<pre\b[^>]*>[\s\S]*?<\/pre>/gi,'').replace(/<code\b[^>]*>[\s\S]*?<\/code>/gi,'');}
function realAt(s,i,q){return s.startsWith(q,i)&&(i===0||s[i-1]!=='\\');}
function find(s,q,from){for(let i=from;i<s.length;){const j=s.indexOf(q,i);if(j<0)return -1;if(realAt(s,j,q))return j;i=j+1;}return -1;}
function line(s,i){return s.slice(0,i).split('\n').length;}
for(const name of fs.readdirSync(root).filter(x=>x.endsWith('.html')).sort()){
  const s=strip(fs.readFileSync(path.join(root,name),'utf8'));
  const pairs=[]; let i=0;
  while(i<s.length){let o=null,c=null;if(realAt(s,i,'\\(')){o='\\(';c='\\)';}else if(realAt(s,i,'\\[')){o='\\[';c='\\]';}if(!o){i++;continue;}const e=find(s,c,i+2);if(e<0)break;pairs.push([i,e,o,c]);i=e+2;}
  for(const q of ['\\)','\\]']){let p=0;while((p=find(s,q,p))>=0){if(!pairs.some(x=>x[1]===p)){const ctx=s.slice(Math.max(0,p-140),Math.min(s.length,p+140)).replace(/\s+/g,' ');console.log(`${name}:${line(s,p)} unmatched ${q} :: ${ctx}`);}p+=2;}}
}
