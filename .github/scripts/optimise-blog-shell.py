from pathlib import Path
import re

posts=sorted(Path('blog/posts').glob('*.html'))
changed=0

legacy='''<link rel="stylesheet" href="../../css/base.css">
<link rel="stylesheet" href="../../css/rwd.css">'''
modern='''<link rel="stylesheet" href="../../css/modern.css">
<link rel="stylesheet" href="../../css/blog-post-modern.css">
<noscript>
<link rel="stylesheet" href="../../css/base.css">
<link rel="stylesheet" href="../../css/rwd.css">
</noscript>'''

for p in posts:
    text=p.read_text(encoding='utf-8')
    original=text
    if legacy in text:
        text=text.replace(legacy,modern,1)
    elif '../../css/modern.css' not in text or '../../css/blog-post-modern.css' not in text:
        raise RuntimeError(f'Unexpected stylesheet block in {p}')
    if text!=original:
        p.write_text(text,encoding='utf-8')
        changed+=1

u=Path('js/utility.js')
text=u.read_text(encoding='utf-8')

old='''  var file=(path.split('/').pop()||'').replace(/\\.html$/,'');
  var titleNode=source.querySelector('h1.section-title, h1');
  var title=titleNode ? titleNode.textContent.trim() : document.title.split('|')[0].trim();
  if(title) document.title=title+' | Hiroki Ishizaka';'''
new='''  var originalTitle=document.title;
  var file=(path.split('/').pop()||'').replace(/\\.html$/,'');
  var titleNode=source.querySelector('h1.section-title, h1');
  var title=titleNode ? titleNode.textContent.trim() : originalTitle.split('|')[0].trim();
  if(title) document.title=title+' | Hiroki Ishizaka';'''
if old not in text:
    raise RuntimeError('Title block not found in utility.js')
text=text.replace(old,new,1)

old_date='''  var metaCandidate=titleNode ? titleNode.nextElementSibling : null;
  var metaTime=metaCandidate && metaCandidate.querySelector ? metaCandidate.querySelector('time') : null;
  var metaStatus=metaCandidate && metaCandidate.querySelector ? metaCandidate.querySelector('.cat') : null;
  var metaSeries=metaCandidate && metaCandidate.querySelector ? metaCandidate.querySelector('b,strong') : null;
  var date=metaTime ? metaTime.textContent.trim() : '';
  if(!date){
    var dm=document.title.match(/from\\s+([^|]+?)\\s*\\|/i);
    if(dm) date=dm[1].trim();
  }'''
new_date='''  var metaCandidate=titleNode ? titleNode.nextElementSibling : null;
  var metaTime=metaCandidate && metaCandidate.querySelector ? metaCandidate.querySelector('time[datetime]') : null;
  if(!metaTime) metaTime=source.querySelector('time[datetime]');
  var metaStatus=metaCandidate && metaCandidate.querySelector ? metaCandidate.querySelector('.cat') : null;
  var metaSeries=metaCandidate && metaCandidate.querySelector ? metaCandidate.querySelector('b,strong') : null;

  function publishedDateFromStructuredData(){
    try{
      var node=document.getElementById('site-structured-data');
      if(!node) return '';
      var data=JSON.parse(node.textContent||'{}');
      var graph=data['@graph']||[];
      for(var i=0;i<graph.length;i++){
        var type=graph[i]['@type'];
        if((type==='BlogPosting'||(Array.isArray(type)&&type.indexOf('BlogPosting')>=0))&&graph[i].datePublished) return graph[i].datePublished;
      }
    }catch(e){}
    return '';
  }
  function formatISODate(iso){
    var m=String(iso||'').match(/^(\\d{4})-(\\d{2})-(\\d{2})$/);
    if(!m) return iso||'';
    var day=parseInt(m[3],10), mod100=day%100, suffix='th';
    if(mod100<11||mod100>13){if(day%10===1)suffix='st';else if(day%10===2)suffix='nd';else if(day%10===3)suffix='rd';}
    var months=['January','February','March','April','May','June','July','August','September','October','November','December'];
    return day+suffix+' '+months[parseInt(m[2],10)-1]+' '+m[1];
  }

  var date=metaTime ? metaTime.textContent.trim() : '';
  if(!date) date=formatISODate(publishedDateFromStructuredData());
  if(!date){
    var dm=originalTitle.match(/from\\s+([^|]+?)\\s*\\|/i);
    if(dm) date=dm[1].trim();
  }'''
if old_date not in text:
    raise RuntimeError('Date block not found in utility.js')
text=text.replace(old_date,new_date,1)
u.write_text(text,encoding='utf-8')

# Validation.
for p in posts:
    t=p.read_text(encoding='utf-8')
    if t.count('href="../../css/modern.css"')!=1: raise RuntimeError(f'{p}: modern.css count wrong')
    if t.count('href="../../css/blog-post-modern.css"')!=1: raise RuntimeError(f'{p}: blog modern CSS count wrong')
    if '<noscript>' not in t or 'href="../../css/base.css"' not in t or 'href="../../css/rwd.css"' not in t:
        raise RuntimeError(f'{p}: no-JS legacy CSS fallback missing')

uc=u.read_text(encoding='utf-8')
for marker in ('var originalTitle=document.title;','publishedDateFromStructuredData','formatISODate(publishedDateFromStructuredData())'):
    if marker not in uc: raise RuntimeError(f'utility.js missing {marker}')

print(f'BLOG_POSTS {len(posts)}')
print(f'HEADS_CHANGED {changed}')
print('BLOG_SHELL_OPTIMISATION VALIDATED')
