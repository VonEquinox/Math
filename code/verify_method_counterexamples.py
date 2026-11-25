"""Exact replays of finite witnesses, using only the Python standard library."""
from collections import Counter
from fractions import Fraction as F
from itertools import permutations
from math import factorial, prod


def atan_bounds(q, terms=36):
    s = sum((-1)**j * F(1, (2*j+1)*q**(2*j+1)) for j in range(terms))
    a = s + (-1)**terms * F(1, (2*terms+1)*q**(2*terms+1))
    return min(s, a), max(s, a)


a, b = atan_bounds(5)
c, d = atan_bounds(239)
# Machin's identity and alternating-series bounds.
p, q = 16*a - 4*d, 16*b - 4*c
assert 3 < p < q < F(22, 7)
B = 2**128


def enclose(lo, hi):
    return F(lo*B // 1, B), F(-((-hi*B) // 1), B)


p, q = enclose(p, q)


def cos_bounds(a, n, k=32):
    a %= 2*n
    m = F(min(a, 2*n-a), n)
    x, r = (p+q)*m/2, (q-p)*m/2
    s = sum((-1)**j * x**(2*j) / factorial(2*j) for j in range(k+1))
    # Lagrange remainder and the global Lipschitz constant of cosine.
    e = x**(2*k+1) / factorial(2*k+1) + r
    return enclose(s-e, s+e)


def verify_cycles():
    n = 25
    c0, c1 = cos_bounds(1, n)
    values = []
    for d in range(n):
        l, u = cos_bounds(2*d+1, n)
        values.append((c0-u, c1-l))
    for i, j, shift, lo, hi in [
        ((0, 7, 17), (21, 3, 11), 1, F(68,1000), F(69,1000)),
        ((0, 8, 14, 18), (22, 3, 12, 16), 1, F(150,1000), F(151,1000)),
        ((0, 5, 10, 15, 20), (4, 8, 13, 18, 23), -1, F(175,1000), F(176,1000))
    ]:
        m = len(i)
        assert len(set(i)) == len(set(j)) == m
        assert all(values[(a-b) % n][0] > 0 for a in i for b in j)

        def bound(perm):
            entries = [values[(i[h]-j[t]) % n] for h, t in enumerate(perm)]
            return prod(i[0] for i in entries), prod(i[1] for i in entries)

        diag_lo, diag_hi = bound(range(m))
        tested = 0
        for perm in permutations(range(m)):
            if 0 < sum(h != t for h, t in enumerate(perm)) < m:
                assert bound(perm)[0] > diag_hi
                tested += 1
        cross_lo, cross_hi = bound([(h+shift) % m for h in range(m)])
        assert lo < cross_lo/diag_hi <= cross_hi/diag_lo < hi < 1
        print(f'S25 m={m}: {tested} smaller-support permutations pass; full cycle fails.')


def verify_equivariant_cover():
    # 13 phase labels and 10 fixed labels, regular S169 with zeros at j=i,i+1.
    p = m = 13
    n = p*m
    rows = [83]*9 + [339, 279, 295, 167]
    cols = [4012] + [8108]*8 + [7852, 7848, 7880, 7768]
    fixed = [(7780,274), (450,7225), (240,7695), (6279,1648), (4897,2204),
             (19,8136), (2456,1095), (62,8065), (1804,4323), (1097,4900)]
    assert len(rows) == len(cols) == m and len(set(fixed)) == 10
    assert all(0 <= a < (1 << p) for a in rows+cols)
    assert all(0 < r < (1 << m) and 0 < c < (1 << m) for r, c in fixed)
    full = (1 << p) - 1

    def rot(x, d):
        d %= p
        return ((x << d) | (x >> (p-d))) & full

    def label_mask(reps, t, side):
        h, z = divmod(t, m)
        f = sum(1 << (p+k) for k, x in enumerate(fixed) if (x[side] >> z) & 1)
        return rot(reps[z], h) | f

    R = [label_mask(rows, i, 0) for i in range(n)]
    C = [label_mask(cols, j, 1) for j in range(n)]
    for masks in (R, C):
        for t, x in enumerate(masks):
            assert masks[(t+m) % n] == rot(x & full, 1) | (x & ~full)
    hist = Counter()
    for i, r in enumerate(R):
        for j, c in enumerate(C):
            k = (r & c).bit_count()
            assert (k == 0 if (j-i) % n in (0, 1) else k >= 2), (i, j, k)
            hist[k] += 1
    assert hist == {0:338, 2:1755, 3:4797, 4:4511, 5:14417, 6:2249, 7:494}
    print(f'C13 / S169: all {n*n} entries checked; 23 equivariant rectangles.')


if __name__ == '__main__':
    verify_cycles()
    verify_equivariant_cover()
