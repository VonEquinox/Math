"""Replay the integer upper-bound-theorem comparisons for two RRCB examples."""

from math import comb


def vertex_bound(facets: int, dimension: int) -> int:
    j, odd = divmod(dimension, 2)
    if odd:
        return 2 * comb(facets - j - 1, j)
    return comb(facets - j, j) + comb(facets - j - 1, j - 1)


def main() -> None:
    cases = (
        (206, 298, 149, 3966404813120491092040276628019041113607480833218161237020350),
        (200, 290, 145, 88246276606414660070871224857153407812857771196300484462570),
    )
    for m, width, expected_d, expected_bound in cases:
        n = comb(m, m // 2)
        cap, d = max((vertex_bound(width, d), d) for d in range(2, (width + 1)//2 + 1))
        if (cap, d) != (expected_bound, expected_d) or not cap < n:
            raise ValueError((m, width, cap, d, n))
        print(f"m={m} facets={width} d={d} Max={cap} n={n}: PASS")


if __name__ == "__main__":
    main()

