import re,os
R='/workspace/js-notes-site/raw/'; D='/workspace/js-notes-site/docs/'
M={ # id: (path, title)
'1XEQKf6cYXMK7J2vkUVyzF5IWMIwzrIRzFAdHkh7Iemg':('objects/prototype.md','[[Prototype]] і __proto__'),
'1ECb4KNDqoIRhggYd3mNR0SC5uxVIIsXkW3_rx41PwFo':('objects/freeze-seal.md','preventExtensions, seal, freeze'),
'1IPD0Xf_3264VjnGyazG-1ji1dIhqwlnuMO2mQ3O4QdA':('objects/getters-setters.md','Гетери і сетери в об’єктах'),
'1umJN9MWkPIn9WUXMBy5JPLrGgoGb-GM_sY5PbzLDbZ4':('objects/proxy-reflect.md',None),
'1kNh8ffqgLlE5fWaB5Aom01uudj2aLYWcZU8-Xu_UW-g':('async/async-await.md',None),
'192LWKs_NWEBv1v-ZM87RE5epsNkdghJJ7FPm9Hp30n0':('async/promisification.md',None),
'1pKebTIv5h0evE1bzWg22pwQF_WORpznXz9u-xkpMae0':('browser/async-defer.md',None),
'1LRuCMysz64IrsZScZ537E2gG1xkBSl3fAR3oKfDGaKY':('browser/mutation-observer.md','MutationObserver'),
'1JMTGXLpdzOpK2PRi-8DaPSE6k7bO6VxqxFRIL7ViwiU':('browser/websocket-sse-workers.md','WebSocket, SSE, Web Worker, Service Worker'),
'1gwYVlC36EpP57lsNCjFxYIG2uiKTbQtcVPcvydeWOQ8':('browser/websocket-vue-react.md',None),
'1O19OvKHfdS2fBFyx5H4h7JtwJUknSYEXLZGpLePQAlw':('functions/closures.md',None),
'1xOV9x82cNQUeS28hJxuRt4qbdDQGyLDqePfEK9d8bN8':('functions/throttle.md',None),
'1u7mMsYTgtqy0uxRaq5VDg0lJv3MXAgZrPQmeWhHy4f8':('checklist.md',None),
}
INL=re.compile(r'^(\s*)\*?`(.*)`\*?\s*$')
def unesc(s): return re.sub(r'\\([\\`*_{}\[\]()#+\-.!|<>~=])',r'\1',s)
def conv(t,md_doc):
    t=re.sub('[\ue000-\uf8ff]','',t)
    L=t.split('\n'); out=[]
    if md_doc:
        for l in L:
            if re.match(r'^\s*````\s*```\w*\s*````\s*$',l): l=l.strip().strip('`').strip(); pass
            elif re.match(r'^\s*``.*``\s*$',l): l=l.strip()[2:-2]
            else:
                m=INL.match(l)
                if m: l=m.group(1)+m.group(2)
            l=re.sub(r'^````\s*(```\w*)\s*````\s*$',r'\1',l.strip()) if l.strip().startswith('````') else l.rstrip()
            l=re.sub(r'\*\*\\\*\\\*(.*?)\\\*\\\*\*\*',r'**\1**',l)
            l=unesc(l)
            l=re.sub(r'^(#+) #+ ',r'\1 ',l)
            out.append(l)
        return '\n'.join(out)
    i=0; infence=False
    while i<len(L):
        l=L[i]; s=l.strip()
        if s.startswith('```'):
            if not infence and s=='```': l='```js'
            infence=not infence; out.append(l); i+=1; continue
        if not infence and s in ('`JavaScript`','JavaScript','`None`','None','`Plain text`'): i+=1; continue
        if not infence and INL.match(l) and s.count('`')>=2 and not re.search(r'`[^`]*`[^`]+`',s.strip('*')):
            blk=[]
            while i<len(L):
                m=INL.match(L[i])
                if m and L[i].strip() not in ('`JavaScript`',): blk.append(m.group(1)+unesc(m.group(2).replace('\u00a0',' ')).rstrip()); i+=1
                elif L[i].strip()=='' and i+1<len(L) and INL.match(L[i+1]): blk.append(''); i+=1
                else: break
            if len(blk)==1 and not re.search(r'[;{}()=]',blk[0]): out.append(l)
            else: out+=['```js']+blk+['```']
            continue
        out.append(l); i+=1
    return '\n'.join(out)
for id,(p,title) in M.items():
    t=open(R+id+'.md').read()
    c=conv(t, id.startswith('1gwY')).strip()+'\n'
    first=c.split('\n')[0]
    if title and not first.startswith('# '): c='# '+title+'\n\n'+c
    elif not first.startswith('# '): pass
    c=re.sub(r'^\* # ',r'# ',c)
    h,_,b=c.partition('\n'); c=h+'\n\n::: v-pre\n'+b.strip()+'\n\n:::\n'
    os.makedirs(os.path.dirname(D+p) or D,exist_ok=True); open(D+p,'w').write(c)
