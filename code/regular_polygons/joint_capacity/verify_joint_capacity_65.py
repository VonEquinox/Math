#!/usr/bin/env python3
"""Strict replay of the 10-private-cell obstruction. Standard library only.

No stored trigonometric bounds or optimizer output are trusted. Endpoints are
constructed using the Machin identity and rational alternating-series bounds.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from math import factorial, prod
from pathlib import Path
import json

N = 65
PRIVATE = {6: [(10, 0), (10, 25), (11, 25)],
           7: [(26, 41), (56, 7)],
           8: [(11, 8), (12, 8), (12, 7), (18, 0), (26, 57)]}
PAIRS = [(16, 18), (16, 14), (49, 40), (48, 39),
         (5, 10), (17, 19), (31, 19), (32, 25)]


def atn_bnd(n):
    terms = [F((-1)**j, (2*j+1)*n**(2*j+1)) for j in range(26)]
    upper = sum(terms[:-1])
    return upper + terms[-1], upper


def pi_bnd():
    # 4*atan(1/5)-atan(1/239)=pi/4; the tangent addition formula gives 1
    # and the left side lies in (0,pi/2).
    a, b = atn_bnd(5), atn_bnd(239)
    lo = F('3.141592653589793238462643')
    hi = F('3.141592653589793238462644')
    assert lo < 16*a[0] - 4*b[1] < 16*a[1] - 4*b[0] < hi
    return lo, hi


@lru_cache(None)
def sine(k):
    lo, hi = pi_bnd()
    assert 0 < k < N
    x, eps = k*(lo+hi)/(2*N), k*(hi-lo)/(2*N)
    # Starting at term 21 the terms strictly decrease in magnitude (x<4).
    # The residual after terms 0..20 is negative and bounded by term 21.
    assert 0 < x < 4
    upper = sum((-1)**j * x**(2*j+1) / factorial(2*j+1) for j in range(21))
    lower = upper - x**43 / factorial(43)
    assert lower - eps > 0
    # sin is 1-Lipschitz: account for replacing pi by its rational midpoint.
    return lower - eps, upper + eps


def mul(*intervals):
    return tuple(prod(v[i] for v in intervals) for i in range(2))


def ratio(a, b):
    assert a[0] > 0 and b[0] > 0
    return a[0]/b[1], a[1]/b[0]


def minus(a, b):
    return a[0] - b[1], a[1] - b[0]


def scale(c, a):
    assert c > 0
    return c*a[0], c*a[1]


def S(a, b):
    d = a-b
    assert d not in (0, 1)
    return scale(2, mul(sine(abs(d)), sine(abs(d-1))))


def endpoint():
    f = ratio(mul(S(11, 25), S(10, 0)), S(10, 25))
    p = ratio(mul(S(11, 8), S(12, 7)), S(12, 8))
    a = mul(S(26, 41), S(56, 7))
    b = mul(p, S(18, 0), S(26, 57))
    d = minus(S(11, 0), f)
    assert d[0] > 0
    return ratio(scale(4, mul(a,b)), mul(d,S(18,57),S(56,41),S(26,7),S(26,7)))[0]


def laurent_product(a,b):
    result = Counter()
    for i, u in [(a,1),(-a,-1)]:
        for j, v in [(b,1),(-b,-1)]:
            result[i+j] += u*v
    return result


def frequencies(cells):
    return Counter(t for i,j in cells for t in (abs(i-j),abs(i-j-1)))


def uniform_squared():
    # When T_k is X^k-X^-k, this identity proves the stated sine identity.
    laurent = laurent_product(11,16)
    laurent.subtract(laurent_product(9,14))
    assert laurent == laurent_product(25,2)
    # Express the post-elimination ratio as a product of eight sine ratios.
    lhs = frequencies([(26,41),(56,7),(11,8),(12,7),(18,0),(26,57)])
    lhs[16] += 1             # cancellation D^-1 supplies sin(16*theta)
    rhs = frequencies([(12,8),(18,57),(56,41),(26,7),(26,7)])
    rhs.update([2,25,10])    # the three sine factors in D
    lhs.subtract(rhs)
    paired = Counter(a for a,b in PAIRS)
    paired.subtract(b for a,b in PAIRS)
    assert lhs == paired
    factors = []
    for a,b in PAIRS:
        assert 0 < a < N and 0 < b < N
        ratio_lo = F(a,b) if a <= b else ratio(sine(a),sine(b))[0]
        factors.append(ratio_lo**2)
    return 16*prod(factors)


def support():
    raw = Path(__file__).with_name('support_65.json').read_bytes()
    expected = '2ff9e3e0a93e50114782a43dd13be132f5674c5fd876d64369910d36ecb74dd3'
    assert sha256(raw).hexdigest() == expected
    data = json.loads(raw)
    r, c = data['row_masks'], data['column_masks']
    assert len(r) == len(c) == N and data['sites'] == N and data['labels'] == 12
    assert all(0 < v < 2**12 for v in r+c)
    assert all(bool(r[i]&c[j]) == ((i-j)%N not in (0,1))
               for i in range(N) for j in range(N))
    for label, cells in PRIVATE.items():
        assert all(r[i]&c[j] == 1 << label for i,j in cells)
    return expected


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without python -O: assertions are proof checks.')
    digest = support()
    u, v = F(1493949855057, 10**12), F(1369, 1000)
    assert endpoint() > u > 1
    assert uniform_squared() > v**2 > 1
    print(json.dumps({'result':'PASS', 'private_premises':sum(map(len,PRIVATE.values())),
                      'endpoint_strict_lower':str(u), 'uniform_strict_lower':str(v),
                      'support_sha256':digest}, indent=2))
