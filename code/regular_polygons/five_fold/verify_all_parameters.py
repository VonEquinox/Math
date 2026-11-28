#!/usr/bin/env python3
"""Replay the all-q exclusion using only integer arithmetic and support masks.

The default templates are the checked-in output of the separate geometry replay.
This program reconstructs *all* marked layouts and searches for a private
four-cycle itself; it does not read stored witnesses or optimizer results.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from math import gcd
from pathlib import Path
import argparse
import json

K = 22
AXES = ((64, 1), (16, 1), (24, 0), (12, 0), (6, 0))
A = (2, 4, 8, 10, 14, 16, 20, 22, 26, 28, 32,
     32, 36, 38, 42, 44, 48, 50, 54, 56, 60, 62)
B = (
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    (-1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1),
)
TEMPLATE_SHA256 = '309b10cde959596a7af145aeacadcda5c3bff56a916adb8837ffdd133908479f'


def nonnegative(a, b):
    """Exact sign of a*q+b for every integer q >= 1."""
    return a >= 0 and a + b >= 0


def fold(a, b):
    """Apply every fold to an affine form, certifying each absolute sign."""
    for c, d in AXES:
        a, b = a - c, b - d
        if not nonnegative(a, b):
            assert nonnegative(-a, -b), (a, b)
            a, b = -a, -b
    return a, b


def alignments():
    """All index lists D=a-64*b, over both shores and dihedral alignments."""
    out = []
    for shore, bs in enumerate(B):
        for i, (a, b) in enumerate(zip(A, bs)):
            # Avoid wrap, including both real neighboring angles.
            assert nonnegative(a, b - 1) and nonnegative(64 - a, -b - 1)
            if i:
                assert nonnegative(a - A[i - 1], b - bs[i - 1] - 1)
            assert fold(2*a, 2*b + shore) == (2, shore)
        assert fold(0, shore) == (6, -shore)
        fixed = [a - 64*b for a, b in zip(A, bs)]
        for reverse in (-1, 1):
            for shift in range(K):
                d = [fixed[(shift + reverse*i) % K] for i in range(K)]
                out.append((shore, d))
    return out


def layouts(path):
    records = []
    raw = path.read_bytes()
    assert sha256(raw).hexdigest() == TEMPLATE_SHA256
    seen = set()
    for line in raw.decode().splitlines():
        ident, m, *masks = map(int, line.split())
        assert ident not in seen and m in (22, 23, 24) and len(masks) == 2*m
        assert all(0 < a < 512 for a in masks)
        seen.add(ident)
        r, c = masks[:m], masks[m:]
        assert all((r[i] & c[j] == 0) == (j in (i, (i+1) % m))
                   for i in range(m) for j in range(m))
        records.append((m, r, c))
    assert Counter(m for m, _, _ in records) == {22: 357, 23: 4, 24: 3}
    for m, rs, cs in records:
        for r, c in ((rs, cs), (cs[1:] + cs[:1], rs)):
            for marks in combinations(range(m), K):
                # A missing selected-to-selected edge contributes no constraint.
                yield ([r[i] if marks[(j+1) % K] == (i+1) % m else 0
                        for j, i in enumerate(marks)], [c[i] for i in marks])


def cycles(rows, cols):
    """Return (edge1, edge2, endpoint1, endpoint2) for private four-cycles."""
    for colour in (1 << k for k in range(9)):
        by_row = {}
        for i, r in enumerate(rows):
            if r & colour:
                by_row[i] = {j for j, c in enumerate(cols) if r & c == colour}
                assert i not in by_row[i] and (i+1) % K not in by_row[i]
        for i, j in combinations(by_row, 2):
            # Only six-distinct-endpoint cycles are needed.
            if len({i, (i+1) % K, j, (j+1) % K}) != 4:
                continue
            for x, y in combinations(sorted(by_row[i] & by_row[j]), 2):
                yield i, j, x, y


def verify(path):
    configurations = alignments()
    tested, histogram, count_layouts = Counter(), Counter(), 0
    for rows, cols in layouts(path):
        count_layouts += 1
        remaining = set(range(len(configurations)))
        for i, j, x, y in cycles(rows, cols):
            survivors = set()
            for index in remaining:
                shore, d = configurations[index]
                p = d[i] + d[(i+1) % K]
                g = gcd(d[j] + d[(j+1) % K] - p, d[x] + d[y] - p)
                if g:
                    odd = g // (g & -g)
                    if odd < 65:
                        histogram[odd] += 1
                        tested[shore] += 1
                        continue
                survivors.add(index)
            remaining = survivors
            if not remaining:
                break
        assert not remaining, (count_layouts, sorted(remaining))
    assert count_layouts == 2554 and tested == {0: 112376, 1: 112376}
    return {'result': 'PASS', 'layouts': count_layouts,
            'alignments_per_layout': len(configurations),
            'exclusions_per_shore': dict(tested),
            'max_odd_part_of_selected_gcd': max(histogram),
            'geometry_input_sha256': TEMPLATE_SHA256}


if __name__ == '__main__':
    assert __debug__, 'Run without python -O: assertions are proof checks.'
    parser = argparse.ArgumentParser()
    parser.add_argument('templates', nargs='?', type=Path,
                        default=Path(__file__).with_name('templates.txt'))
    print(json.dumps(verify(parser.parse_args().templates), indent=2))
