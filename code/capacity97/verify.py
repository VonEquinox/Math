"""Exact rational replay for the N=97 residual capacity obstruction."""

from fractions import Fraction as F
from functools import lru_cache
from math import factorial
import json
from pathlib import Path


def arctan_recip(k, terms=40):
    s = sum((F((-1)**j, (2*j+1)*k**(2*j+1)) for j in range(terms)), F(0))
    next_term = F((-1)**terms, (2*terms+1)*k**(2*terms+1))
    return min(s, s+next_term), max(s, s+next_term)


a,b = arctan_recip(5)
c,d = arctan_recip(239)
PI = 16*a-4*d, 16*b-4*c


@lru_cache(None)
def cosine_near(k, n):
    lo, hi = (k*p/n for p in PI)
    x = (lo+hi)/2
    rad = (hi-lo)/2
    # Lagrange remainder after the degree-70 Taylor polynomial.
    s = sum(((-1)**j*x**(2*j)/factorial(2*j) for j in range(36)), F(0))
    err = x**71/factorial(71) + rad  # |cos'| <= 1
    return s-err, s+err


def slack(i, j, n):
    k = (2*(i-j)-1)%(2*n)
    k = min(k, 2*n-k)
    a,b=cosine_near(1,n)
    c,d=cosine_near(k,n)
    assert a-d>0
    return a-d,b-c


def main():
    data=json.loads(Path(__file__).with_name("support.json").read_text())
    n,r=data["sites"],data["labels"]
    rows,cols=data["row_masks"],data["column_masks"]
    assert (n,r,len(rows),len(cols))==(97,13,97,97)
    assert all(0<=m < 1<<r for m in rows+cols)

    def owner(i,j):
        return rows[i]&cols[j]

    assert all(bool(owner(i,j))==((i-j)%n not in (0,1)) for i in range(n) for j in range(n))

    def private(k,i,j):
        assert owner(i,j)==1<<k
        return slack(i,j,n)

    def path_lower(k, path, target):
        assert len(path)%2==1
        assert (path[0][0],path[-1][1])==target
        for t,(a,b) in enumerate(zip(path,path[1:])):
            assert a[1-t%2]==b[1-t%2]
        ans=F(1)
        for t,cell in enumerate(path):
            lo,hi=private(k,*cell)
            ans=ans*lo if t%2==0 else ans/hi
        return ans

    required=((84,86),(90,8),(12,14))
    budget=((84,14),(90,86),(12,8))
    assert sorted(i for i,j in required)==sorted(i for i,j in budget)
    assert sorted(j for i,j in required)==sorted(j for i,j in budget)
    left=F(1)
    for cell in required:
        left*=private(2,*cell)[0]
    path_a=((84,12),(83,12),(83,13),(82,13),(82,14))
    path_b=((90,84),(89,84),(89,85),(88,85),(88,86))
    right=F(1)
    for cell, forced in zip(budget,(path_lower(12,path_a,budget[0]),path_lower(3,path_b,budget[1]),F(0))):
        assert owner(*cell)&(1<<2)
        hi=slack(*cell,n)[1]-forced
        assert hi>0
        right*=hi
    assert left>F(18454202,1000000)*right
    print("PASS: required/residual capacity > 18.454202; one specified support excluded")


if __name__=="__main__":
    main()
