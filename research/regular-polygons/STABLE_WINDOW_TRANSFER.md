# Stable angular windows and transfer to unrestricted regular polygons

This reading note reconstructs the transfer mechanism from the 22:00 archive. It uses exact positive-angle reflections and makes no assumption that an arbitrary optimum is a folded lift. The result is conditional on the existence of a deficient seed; the seed is not supplied.

## Definition

For $s\ge2$ and sufficiently small $\theta>0$, let

$$
A_{2s}(\theta)_{ij}=\cos\theta-\cos((i-j)\theta),
\quad i\in\{0,2,\ldots,2s\},\quad j\in\{1,3,\ldots,2s-1\}.
$$

This is a rectangular true slack window with $s+1$ prices and $s$ sites; both exterior flanks are present. Define $u(s)$ to be its eventual nonnegative rank as $\theta\downarrow0$ through positive angles.

For a fixed $s$, putting $t=\tan(\theta/2)$ makes every entry rational in $t$, with denominators nonvanishing near zero. For each fixed width $r$, the equations $A_{2s}(\theta)=UV$, $U,V\ge0$, give a semialgebraic feasibility set of $t$ after clearing positive denominators and eliminating the finitely many factor variables. A semialgebraic subset of the real line is a finite union of intervals and points. Thus feasibility is constant for all sufficiently small positive $t$. The rank takes finitely many integer values, which proves that $u(s)$ is well-defined. No rank at $t=0$ is substituted.

## True same-angle folding lemma

Consider the alternating grid on an integer interval $[0,e]$. Reflect the shorter side of the integer midpoint $a=\lfloor e/2\rfloor$ onto the longer side. The map on indices preserves parity (and translating the interval may interchange the roles of the two shores). On a pair of indices from the same side, their cosine difference is unchanged. On a pair on opposite sides, with distances $x=|i-a|$ and $y=|j-a|$, the slack difference is exactly

$$
\cos((x-y)\theta)-\cos((x+y)\theta)
=2\sin(x\theta)\sin(y\theta).
$$

For arm lengths at most $\pi/\theta$, it is nonnegative. The opposite-side pairs split into the two orientations, and each orientation's correction is a nonnegative rank-one outer product: on the row and column banks, restrict the sine factors to the specified sides. Therefore a factorization of the reflected window can be copied back and extended by at most two genuine nonnegative summands.

The retained integer interval has length $\lceil e/2\rceil$. Reversal, translation and transposition account for the alternating phase. With $\theta=\pi/N$, the full regular table is the alternating grid of length $2N$ with the endpoint price duplicated. This duplication does not change nonnegative rank. The first reflection is valid even when an arm has length $N$; every subsequent one has shorter arms. After $h$ reflections the retained length is $\lceil 2N/2^h\rceil$, by repeated integer ceiling composition.

Consequently for fixed $s$, whenever $N\le2^h s$ and $N$ is sufficiently large for the stable positive-angle value at $s$,

$$
r_N\le 2h+u(s).
\tag{1}
$$

The final window embeds in $A_{2s}(\pi/N)$, up to the phase operations just described. Restricting or repeating rows and columns never increases nonnegative rank.

For fixed $s$ and a sufficiently small common positive parameter, restriction gives $u(s)\le u(2s)$ and the same-angle fold gives $u(2s)\le u(s)+2$.

## A single strict seed disproves the conjecture

Write $\beta(s)=\min\{q:B(q)\ge s\}$ with $\beta(2)=2$. The ordinary constructive folding bound gives $u(s)\le\beta(s)$.

If $u(33)\le10$, take any integer $N$ with

$$
32\cdot2^h<N\le33\cdot2^h.
$$

Equation (1) implies $r_N\le10+2h$, while the candidate formula is $\beta(N)=11+2h$. For sufficiently large $h$ the stability threshold is satisfied for every integer in the interval. This is an infinite family of genuine counterexamples, not just a dyadic sequence. The lower and upper natural densities of this guaranteed family are respectively $1/32$ and $2/33$; its logarithmic density is $\log_2(33/32)$. These are densities of a conditional certified subset, not observed frequencies of counterexamples.

No such stable 33-site factorization has yet been constructed or ruled out in the 22:00 proof chain.

## Accumulated gains and all-order capacity

Put $d(s)=\beta(s)-u(s)\ge0$ and $D=\sup_{s\ge3}d(s)$. For any fixed seed $s$, choose $h=\lceil\log_2(N/s)\rceil$. For all sufficiently large $N$,

$$
2^{h-1}s<N\le2^hs,\qquad r_N\le2h+u(s).
$$

For the two parity plateaux of $B$, this implies $\beta(N)\ge\beta(s)+2h-2$: a smaller candidate width would force $N\le2^{h-1}B(\beta(s)-1)<2^{h-1}s$. The case $s=3$ follows directly from the starting values. Along $N=2^hs$, the candidate width is exactly $\beta(s)+2h$. Hence

$$
\liminf_{N\to\infty}(\beta(N)-r_N)\ge\max(0,D-2),\qquad
\limsup_{N\to\infty}(\beta(N)-r_N)\ge D.
$$

Since $d(2s)-d(s)=2-(u(2s)-u(s))$, all lost stable increments along a dyadic ray telescope. If infinitely many increments are less than two on any one ray, then $D=\infty$, and the unrestricted deficit tends to infinity over all sufficiently large integer orders. Conversely, any unbounded sequence with deficit at most a fixed $C_0$ forces $d(s)\le C_0+2$ for every seed. This converse does not assert that such a subsequence exists.

Let $C(q)=\max\{s\ge2:u(s)\le q\}$ and $F_{\rm all}(r)=\max\{m:r_n\le r\text{ for every }3\le n\le m\}$. The doubling inequality gives the limits $\alpha_p=\lim_{k\to\infty}2^{-k}C(2k+p)$, $p=0,1$, in the extended reals. Applying (1) to a fixed maximal stable seed and treating the finitely many small physical orders separately shows

$$
\liminf_{k\to\infty}2^{-k}F_{\rm all}(2k+p)\ge\alpha_p.
$$

This is an unrestricted lower envelope on *solid capacity*. It is not an upper bound on the unrestricted capacity, and it does not assume monotonicity of complete regular ranks.

## Source and limits

The original proofs are in the frozen archive:

- `capacity_program/INFINITESIMAL_ARC_CAPACITY.md`
- `capacity_program/EVERY_LOST_STABLE_LOCAL_DOUBLING_ACCUMULATES_AS_A_PERSISTENT_UNRESTRICTED_WIDTH_SAVING_ON_ONE_ENTIRE_ACTUAL_DYADIC_REGULAR_RAY.md`
- `capacity_program/UNBOUNDED_STABLE_WINDOW_SAVINGS_FORCE_DIVERGING_UNRESTRICTED_WIDTH_GAINS_AT_EVERY_LARGE_REGULAR_ORDER_AND_THE_SOLID_CAPACITY_HAS_TWO_PARITY_LOWER_ENVELOPES.md`

The 22:00 archive reports exact stable ranks 11 for sites 37–42, with 37 obtained from the separate general polygon capacity theorem. Its 33–36 stable sites remain open. Resolving a single stable plateau against improvement would not, by itself, establish the unrestricted general conjecture.
