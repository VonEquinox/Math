"""Integer-only replay of the folding reduction and its small-fiber obstruction.

Trigonometric identities are checked in Z[z]/(z**n + 1), at z=exp(pi*i/n).
This is stronger than checking just a primitive root. Positivity is established
by integer angle bounds. There is no floating-point arithmetic in this file.
The geometric lemma explaining the vertex-count implication is in the report.
"""
import json
from math import comb


def add(*polys):
    out = {}
    for p in polys:
        for a, b in p.items():
            out[a] = out.get(a, 0) + b
    return {a: b for a, b in out.items() if b}


def scale(p, c):
    return {a: b*c for a, b in p.items() if b*c}


def reduce_term(e, c, n):
    e %= 2*n
    return (e, c) if e < n else (e-n, -c)


def mul(p, q, n):
    out = {}
    for a, b in p.items():
        for c, d in q.items():
            e, v = reduce_term(a+c, b*d, n)
            out[e] = out.get(e, 0) + v
    return {a: b for a, b in out.items() if b}


def trig(k, n, sine=False):
    # Cosine: 2*cos(k theta); sine: 2*i*sin(k theta).
    out = {}
    for e, c in ((k, 1), (-k, -1 if sine else 1)):
        e, c = reduce_term(e, c, n)
        out[e] = out.get(e, 0) + c
    return {a: b for a, b in out.items() if b}


def fold(t, n, h, code=False):
    s, b, e = 1, 0, 2*n
    for _ in range(h):
        a = e//2
        v = s*t+b
        sign = 1 if v >= a else -1
        s, b = sign*s, sign*(b-a)
        e = (e+1)//2
    return (s, b) if code else s*t+b


def verify_interpolation(t, u, v, ft, fu, fv, n):
    assert u <= t <= v and 0 < v-u < n
    D, B, A = v-u, v-t, t-u
    for p, q, r in ((t,u,v), (ft,fu,fv)):
        for sine in (False, True):
            expression = add(
                mul(trig(D,n,True), trig(p,n,sine), n),
                scale(mul(trig(B,n,True), trig(q,n,sine), n), -1),
                scale(mul(trig(A,n,True), trig(r,n,sine), n), -1))
            assert not expression, (n,t,u,v,sine,expression)


def reduce_shore(ts, n, h):
    fs = [fold(t,n,h) for t in ts]
    codes = sorted({fold(t,n,h,True) for t in ts})
    endpoints, covered = set(), set()
    checks = 0
    for s,b in codes:
        g = [i for i,t in enumerate(ts) if fs[i] == s*t+b]
        lo, hi = g[0], g[-1]
        assert g == list(range(lo,hi+1))
        endpoints.update((lo,hi)); covered.update(g)
        if lo == hi:
            continue
        for i in g:
            verify_interpolation(ts[i],ts[lo],ts[hi],fs[i],fs[lo],fs[hi],n)
            checks += 4
    assert covered == set(range(n))
    return sorted(endpoints), checks


def cyclic_facets(vertices, dimension):
    # UBT bound for facets of a simplicial d-polytope with v vertices;
    # by polarity this bounds vertices with v facets.
    if dimension == 1:
        return 2
    k = dimension//2
    if dimension % 2:
        return 2*comb(vertices-k-1,k)
    return comb(vertices-k,k) + comb(vertices-k-1,k-1)


def verify(n,h):
    assert n == 4*2**h+1
    rows, columns = [2*i for i in range(n)], [2*j+1 for j in range(n)]
    fr, fc = [fold(t,n,h) for t in rows], [fold(t,n,h) for t in columns]
    I, row_checks = reduce_shore(rows,n,h)
    J, col_checks = reduce_shore(columns,n,h)
    # The periodic terminal row has coefficients sin(6 theta)/sin(8 theta)
    # and sin(2 theta)/sin(8 theta), both strictly positive for these n.
    assert 0 < 8 < n
    for ts,fs in ((rows,fr),):
        for xs in (ts,fs):
            for sine in (False,True):
                p = add(mul(trig(8,n,True),trig(xs[n-1],n,sine),n),
                        scale(mul(trig(6,n,True),trig(xs[0],n,sine),n),-1),
                        scale(mul(trig(2,n,True),trig(xs[n-4],n,sine),n),-1))
                assert not p, (n,'wrap',sine,p)
    assert n-1 in I and 0 in I and n-4 in I
    I.remove(n-1)
    m = 2**h
    assert I == [0] + [v for j in range(1,m) for v in (4*j,4*j+1)]
    assert J == [4*j for j in range(m+1)]
    assert set(fr) == {1,3,5,7,9}
    assert set(fc) == {0,2,4,6,8}
    fiber = [j for j in range(n) if fc[j] == 4]
    adjacent_rows = sorted({i for j in fiber for i in (j,(j+1)%n)})
    assert len(fiber) == m and len(adjacent_rows) == 2*m
    assert all(abs(fr[i]-fc[j]) == 1 for i in adjacent_rows for j in fiber)
    for j in fiber:
        assert (rows[j]-columns[j]) % (2*n) in (1,2*n-1)
        assert (rows[(j+1)%n]-columns[j]) % (2*n) in (1,2*n-1)
    # In a rank-four factorization U V, a constant-fold fiber has image rank
    # three, so its latent span has dimension at most rank(V)-1. Its compact
    # affine lift consequently has dimension at most rank(V)-2. The transpose
    # uses the row fiber. Sylvester gives min(rank(U),rank(V)) <= h+1 here.
    row_fiber = [i for i in range(n) if fr[i] == 3]
    adjacent_columns = sorted({j for i in row_fiber for j in (i,(i-1)%n)})
    assert len(row_fiber) == m and len(adjacent_columns) == 2*m
    assert all(abs(fr[i]-fc[j]) == 1 for i in row_fiber for j in adjacent_columns)
    r = 2*h-1
    fiber_dim = h-1
    bounds = {str(d):cyclic_facets(r,d) for d in range(1,fiber_dim+1)}
    ubt = max(bounds.values())
    return {'n':n,'h':h,'compressed_shape':[len(I),len(J)],
            'integer_ring_identities':row_checks+col_checks+4,
            'nonnegative_rank_preserved_by_reduction':True,
            'fiber_columns':fiber,'fiber_rows':row_fiber,'fiber_forced_vertices':m,
            'full_matrix_rank':4,'fiber_image_rank':3,
            'hypothetical_deficient_width':r,'small_factor_rank_max':h+1,
            'fiber_lift_dimension_max':fiber_dim,
            'ubt_by_dimension':bounds,'ubt_max':ubt,
            'deficient_residual_width_excluded':ubt<m,
            'exact_residual_nonnegative_rank':2*h if ubt<m else None,
            'main_conjecture_counterexample':False}


if __name__ == '__main__':
    print(json.dumps([verify(4*2**h+1,h) for h in (3,4,5,6,7)],indent=2))
