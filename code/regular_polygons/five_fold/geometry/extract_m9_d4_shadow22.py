#!/usr/bin/env python3
"""Reconstruct every >=22 polygon support from exact signed-sweep records."""
from pathlib import Path
from itertools import combinations
from collections import Counter,defaultdict
import json,hashlib

H=Path(__file__).resolve().parent
types={}
for line in (H/"m9_d4_f22plus.txt").read_text().splitlines():
    ident,n,*F=line.split();F=list(map(int,F));assert len(F)==int(n)
    ridges=defaultdict(list)
    for i,f in enumerate(F):
        vs=[j for j in range(9) if f>>j&1]
        for t in combinations(vs,3):ridges[sum(1<<j for j in t)].append(i)
    assert all(len(v)==2 for v in ridges.values())
    types[ident]=(F,ridges)
templates=set();hist=Counter();labels={}
for line in (H/"m9_d4_shadow22_sweeps.txt").read_text().splitlines():
    ident,n,word,order=line.split();n=int(n);word=int(word);p=list(map(int,order));assert sorted(p)==list(range(9))
    F,ridges=types[ident];cross=[]
    for i,j,k in combinations(range(9),3):
        if ((word>>i)&1)==((word>>k)&1)!=((word>>j)&1):
            t=(1<<p[i])|(1<<p[j])|(1<<p[k])
            if t in ridges:cross.append(t)
    assert len(cross)==n
    graph=defaultdict(list);edge={}
    for t in cross:
        a,b=ridges[t];graph[a].append(b);graph[b].append(a);edge[a,b]=edge[b,a]=t
    assert len(graph)==n and all(len(v)==2 for v in graph.values())
    u=min(graph);start=u;prev=min(graph[u]);R=[];C=[]
    while True:
        R.append(511^F[u]);C.append(edge[prev,u]);v,=set(graph[u])-{prev};prev,u=u,v
        if u==start:break
    assert len(R)==n
    assert all((R[i]&C[j]==0)==(j in [i,(i+1)%n]) for i in range(n) for j in range(n))
    t=(n,*R,*C);templates.add(t);labels.setdefault(t,ident);hist[n]+=1
out=sorted(templates)
(H/"m9_d4_shadow22_templates.txt").write_text(''.join(' '.join(map(str,[k,*t]))+'\n' for k,t in enumerate(out)))
manifest={"sweep_histogram":dict(hist),"template_histogram":dict(Counter(t[0] for t in out)),
          "input_sha256":{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [H/"m9_d4_f22plus.txt",H/"m9_d4_shadow22_sweeps.txt"]},
          "template_type_ids":{k:labels[t] for k,t in enumerate(out)}}
(H/"m9_d4_shadow22_manifest.json").write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
