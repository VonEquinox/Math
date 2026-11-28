#!/usr/bin/env python3
"""Complete 4D catalog audit: independently verifiable *integer* realizations.
Optional --convert Firsching.txt rounds the original rational input and checks
facets after rounding. Default recomputes all supporting simplices and audits
every type for pairwise non-isomorphism, then outputs the 262 large facet lists.
"""
from itertools import combinations
from fractions import Fraction
import re,sys
from r2_geom_catalog_audit import audit
from r2_geom_facets import detsign,extract
def supports(g):
 orient={t:detsign([[1]+g[i] for i in t]) for t in combinations(range(9),5)}
 F=set()
 for t in combinations(range(9),4):
  signs=[orient[tuple(sorted((*t,j)))]*(-1)**sum(i>j for i in t) for j in range(9) if j not in t]
  if min(signs)>0 or max(signs)<0:F.add(sum(1<<i for i in t))
  elif min(signs)>=0 or max(signs)<=0: return None
 return tuple(sorted(F))
if __name__=='__main__':
 if sys.argv[1]=='--convert':
  for l in open(sys.argv[2]):
   id,raw=l.split(':');positions=[[Fraction(x.strip()) for x in group.split(',')]for group in re.findall(r'\[([^\[\]]+)\]',raw)]
   _,F=extract(l);scale=16
   while 1:
    g=[[round(x*scale) for x in p]for p in positions]
    if supports(g)==tuple(F):break
    scale*=2
   print(id,*[v for p in g for v in p])
 else:
  D=[]
  for l in open(sys.argv[1]):
   id,*vals=l.split();assert len(vals)==36
   g=[[int(v) for v in vals[4*i:4*i+4]] for i in range(9)];F=supports(g);assert F and all(any(f&(1<<i) for f in F) for i in range(9));D.append((id,F))
  assert len(D)==1142;cs=audit(D);print('1,142 integer realizations, pairwise distinct; facet distribution: '+str(sorted(cs.items())),file=sys.stderr)
  for id,F in D:
   if len(F)>=25: print(id,len(F),*F)
