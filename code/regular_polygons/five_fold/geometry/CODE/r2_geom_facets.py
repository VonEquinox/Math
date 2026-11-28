#!/usr/bin/env python3
"""Convert Firsching's rational representatives to exact 9-vertex simplicial 4-polytope facets.
Usage: python r2_geom_facets.py input.txt [--minimum 25] > simplicial4.txt.
Original input SHA Git blob 8286c8307d414174b0fc8ccf42c5e79cbc729a9c.
Shared file with recipe available in ROUND2_GEOMETRY.md. Python stdlib only.
"""
from math import lcm
from fractions import Fraction
from itertools import combinations
import re,sys,argparse
def detsign(a):
    a=[row[:] for row in a]; n=len(a); s=1; den=1
    for k in range(n-1):
        if not a[k][k]:
            l=next((i for i in range(k+1,n) if a[i][k]),None)
            if l is None:return 0
            a[k],a[l]=a[l],a[k];s=-s
        piv=a[k][k]
        for i in range(k+1,n):
            v=a[i][k]
            for j in range(k+1,n):
                a[i][j]=(a[i][j]*piv-v*a[k][j])//den
        den=piv
    val=s*a[-1][-1];return (val>0)-(val<0)
def extract(line):
    id,txt=line.strip().split(':',1)
    pts=[]
    for group in re.findall(r'\[([^\[\]]+)\]',txt):
        a=[Fraction(x.strip()) for x in group.split(',')];assert len(a)==4
        D=lcm(*[x.denominator for x in a]);pts.append([D]+[int(D*x) for x in a])
    assert len(pts)==9
    orient={s:detsign([pts[j] for j in s]) for s in combinations(range(9),5)}
    facets=set()
    for s in combinations(range(9),4):
        signs={j:orient[tuple(sorted((*s,j)))]*(-1)**sum(j<i for i in s) for j in range(9) if j not in s}
        if set(signs.values()) in ({1},{-1}):facets.add(sum(1<<i for i in s))
        elif 1 not in signs.values() or -1 not in signs.values(): raise ValueError(('non-simplicial',id,s,signs))
    return id,sorted(facets)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('--minimum',type=int,default=25);args=p.parse_args()
    for l in open(args.input):
        if not l.strip():continue
        id,F=extract(l)
        if len(F)>=args.minimum: print(id,len(F),*F)
