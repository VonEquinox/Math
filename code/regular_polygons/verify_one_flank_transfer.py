#!/usr/bin/env python3
"""Exact arithmetic sanity check of the constructive one-flank identity.

This verifies a conditional transfer, not the existence of a deficient seed.
Only Python's standard library is required.
"""
from fractions import Fraction
import json


def trig_table(t, max_angle):
    """cos(k theta), sin(k theta), where tan(theta/2)=t."""
    c = (1-t*t)/(1+t*t)
    s = 2*t/(1+t*t)
    cs, ss = [Fraction(1)], [Fraction(0)]
    for _ in range(max_angle):
        cs.append(cs[-1]*c-ss[-1]*s)
        ss.append(ss[-1]*c+cs[-2]*s)
    return cs, ss


def slack(q, cs):
    return [[cs[1]-cs[abs(2*i-2*j-1)] for j in range(q)] for i in range(q)]


def product(u, v):
    return [[sum((a*b for a,b in zip(row,col)), Fraction(0))
             for col in zip(*v)] for row in u]


def step(u, v, ss):
    q = len(u)
    assert len(v[0]) == q
    Q = 2*q-1
    a = Q
    rho = [min(2*i,2*a-2*i)//2 for i in range(Q)]
    kappa = [(min(2*j+1,2*a-(2*j+1))-1)//2 for j in range(Q)]
    out_u = []
    for i in range(Q):
        x = 2*i
        out_u.append(u[rho[i]][:] + [2*ss[a-x] if x<a else Fraction(0),
                                     2*ss[x-a] if x>a else Fraction(0)])
    out_v = [[row[k] for k in kappa] for row in v]
    out_v.append([ss[(2*j+1)-a] if 2*j+1>a else Fraction(0) for j in range(Q)])
    out_v.append([ss[a-(2*j+1)] if 2*j+1<a else Fraction(0) for j in range(Q)])
    return out_u, out_v


def main():
    cases=[]
    for q0, iterations in [(2,4),(3,3),(4,3),(5,2),(7,2)]:
        Q=(q0-1)*2**iterations+1
        t=Fraction(1,100*Q)
        cs,ss=trig_table(t,2*Q+2)
        u=slack(q0,cs)
        v=[[Fraction(i==j) for j in range(q0)] for i in range(q0)]
        q=q0
        assert product(u,v)==slack(q,cs)
        for _ in range(iterations):
            u,v=step(u,v,ss)
            q=2*q-1
            assert product(u,v)==slack(q,cs)
            assert all(x>=0 for row in u+v for x in row)
        cases.append(dict(seed=q0,steps=iterations,result_order=q,
                          result_width=len(v),exact_identity=True,nonnegative=True))
    print(json.dumps(dict(status="PASS",claim="conditional transfer only",cases=cases),indent=2))


if __name__=="__main__":
    main()
