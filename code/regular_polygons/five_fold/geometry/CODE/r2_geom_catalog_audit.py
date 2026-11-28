#!/usr/bin/env python3
"""Construct all simplicial D5/9-vertex types from the certificate's small integer Gale points.
Only external logical dependency: FMM Theorem 1.2(b), exactly 322 such types.
Identify nonisomorphic types by complete backtracking (a 9! superset is avoided using
vertex incidence counts, and pair counts but none are assumed complete).
"""
from itertools import combinations
from collections import defaultdict,Counter
import sys
def det(a,b,c):
 return (a[0]*(b[1]*c[2]-b[2]*c[1])+a[1]*(b[2]*c[0]-b[0]*c[2])+a[2]*(b[0]*c[1]-b[1]*c[0]))
def facets(g):
 sign={s:det(*[g[i] for i in s]) for s in combinations(range(9),3)}
 assert all(sign.values()),'uniformity'
 F=set()
 for t in combinations(range(9),4):
  w=[(-1)**j*sign[t[:j]+t[j+1:]] for j in range(4)]
  if all(x>0 for x in w) or all(x<0 for x in w):F.add(511^sum(1<<i for i in t))
 # For every i, a positive circuit avoiding i: origin lies in the interior of
 # conv{g_j:j != i}. Thus the Gale dual is an affine polytope with all nine
 # labels as vertices, all facets simplicial, and precisely these five-sets.
 assert all(any(f&(1<<i) for f in F) for i in range(9))
 return tuple(sorted(F))
def faceprofile(F):
 pair=[[sum(bool(f&(1<<i)) and bool(f&(1<<j)) for f in F) for j in range(9)] for i in range(9)]
 # Incorporating all pair values by row does not lose any genuine isomorphism.
 sig=tuple((pair[i][i],tuple(sorted(pair[i]))) for i in range(9))
 return tuple(sorted(sig)),sig,pair
def isomorphic(F1,F2,p1,p2):
 if len(F1)!=len(F2):return False
 key,sa,da=p1;key2,sb,db=p2
 if key!=key2:return False
 choices=[[j for j in range(9) if sb[j]==sa[i]] for i in range(9)]
 order=sorted(range(9),key=lambda i:len(choices[i]));mp=[-1]*9;Z=set(F2)
 def dfs(k,used):
  if k==9:
   return all(sum(1<<mp[i] for i in range(9) if f>>i&1) in Z for f in F1)
  i=order[k]
  for j in choices[i]:
   if used>>j&1:continue
   if any(da[i][i0]!=db[j][mp[i0]] for i0 in order[:k]):continue
   mp[i]=j
   if dfs(k+1,used|1<<j):return True
  return False
 return dfs(0,0)
def audit(data):
 seen=defaultdict(list);ids=[]; counts=Counter()
 for id,F in data:
  ids.append(id);p=faceprofile(F);k=(len(F),p[0])
  for oid,G,q in seen[k]:assert not isomorphic(F,G,p,q),(id,oid,'duplicate abstract type')
  seen[k].append((id,F,p));counts[len(F)]+=1
 return counts
def readgales(path):
 d=[]
 for line in open(path):
  a=list(map(int,line.split()));assert len(a)==28;id,*a=a;g=[a[3*i:3*i+3]for i in range(9)];d.append((id,facets(g)))
 assert [id for id,_ in d]==list(range(1,323))
 return d
if __name__=='__main__':
 data=readgales(sys.argv[1]);counts=audit(data);assert sum(counts.values())==322
 print('322 realized, pairwise nonisomorphic, simplicial 5-polytopes; facet distribution: '+str(sorted(counts.items())),file=sys.stderr)
 for id,F in data:
  if len(F)>=25:print('P'+str(id),len(F),*F)
