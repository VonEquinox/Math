"""Independent pure-Python integer replay of the finite support lemma.

Generate the combinatorics from tuples, not the C++ bit construction.  The
default replays the three small tiers and checks a size-18 positive control.
--all also replays the size-16 tier.  This script has no numerical optimizer.
"""
import argparse
import itertools as it
import json
import time
from pathlib import Path

WORDS = list(it.product(range(3), repeat=4))
INDEX = {w: i for i, w in enumerate(WORDS)}
ALL = (1 << 81) - 1
def mask(ws):
    return sum(1 << INDEX[w] for w in ws)

CUBES = []
for fixed in range(4):
    varying = [j for j in range(4) if j != fixed]
    for a in range(3):
        for pairs in it.product(list(it.combinations(range(3), 2)), repeat=3):
            CUBES.append(mask(w for w in WORDS if w[fixed] == a and
                              all(w[j] in p for j, p in zip(varying, pairs))))
assert len(set(CUBES)) == 324 and all(c.bit_count() == 8 for c in CUBES)

PARTITIONS = []
for j, k in it.combinations(range(4), 2):
    fs = [mask(w for w in WORDS if (w[j], w[k]) == (a, b))
          for a, b in it.product(range(3), repeat=2)]
    assert sum(fs) == ALL and all(f.bit_count() == 9 for f in fs)
    PARTITIONS.append(fs)

def search(cap, missing):
    clauses = []
    for fs in PARTITIONS:
        for comb in it.combinations(fs, missing + 1):
            clauses.append(sum(comb))
    nodes = 0
    def dfs(true, false):
        nonlocal nodes
        nodes += 1
        while True:
            if true & false or true.bit_count() > cap:
                return None
            free = ALL ^ (true | false)
            yes = no = 0
            needs = []
            for c in CUBES:
                count = (c & true).bit_count()
                u = c & free
                if count == 1:
                    if not u:
                        return None
                    if u & (u-1):
                        needs.append(u)
                    else:
                        yes |= u
                elif count == 0 and u and not (u & (u-1)):
                    no |= u
            for c in clauses:
                if c & true:
                    continue
                u = c & free
                if not u:
                    return None
                if u & (u-1):
                    needs.append(u)
                else:
                    yes |= u
            if not (yes | no):
                break
            true |= yes
            false |= no
        if not needs:
            assert all((c & true).bit_count() != 1 for c in CUBES)
            assert all(c & true for c in clauses)
            return true
        remaining = cap - true.bit_count()
        if remaining <= 0:
            return None
        # A packing of disjoint positive clauses gives an integer lower bound.
        needs.sort(key=lambda c: (c.bit_count(), c))
        used = count = 0
        for c in needs:
            if not (c & used):
                used |= c
                count += 1
                if count > remaining:
                    return None
        # Deliberately different from C++: branch in ascending native index,
        # without its weighted-occurrence variable heuristic.
        choices = needs[0]
        while choices:
            bit = choices & -choices
            choices ^= bit
            found = dfs(true | bit, false)
            if found is not None:
                return found
            false |= bit
        return None

    for distance in (1, 2, 3):
        q = (0,) * (4-distance) + (1,) * distance
        false = mask(w for w in WORDS if w != (0,0,0,0) and
                     sum(a != 0 for a in w) < distance)
        found = dfs(1 | (1 << INDEX[q]), false)
        if found is not None:
            return {'cap':cap,'missing':missing,'status':'SAT','nodes':nodes,
                    'support':[w for i,w in enumerate(WORDS) if found>>i&1]}
    return {'cap':cap,'missing':missing,'status':'UNSAT','nodes':nodes}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--all',action='store_true')
    args=ap.parse_args(); out=[]
    control = [(a,b,c,d) for a,b,c,d in WORDS if
               (a==0 and b==0 and c in (0,2)) or
               (a in (1,2) and b in (1,2) and c==1)]
    H=mask(control)
    assert H.bit_count()==18
    assert all((H & c).bit_count()!=1 for c in CUBES)
    assert all(any(sum(x!=y for x,y in zip(v,w))<=1 for w in control)
               for v in WORDS)
    print('positive control: 18 ghosts, no-single and all stars hit',flush=True)
    for cap,missing in [(7,3),(10,2),(13,1)] + ([(16,0)] if args.all else []):
        started=time.perf_counter(); row=search(cap,missing)
        row['elapsed_seconds']=time.perf_counter()-started
        print(row,flush=True);out.append(row)
    Path(__file__).with_name('outside_triangle4_python_replay.json').write_text(
        json.dumps({'positive_control':control,'cases':out},indent=2))
if __name__=='__main__':main()
