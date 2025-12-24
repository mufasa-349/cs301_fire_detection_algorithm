"""
Exact DP for Minimum Vertex Cover on a GENERAL undirected graph (can have cycles).

Why this file exists:
- The original `dp_forest.py` implements a tree/forest DP (3-state DFS) which is NOT valid
  for general graphs (cycles break the parent-child assumption).
- The assignment statement says the graph does NOT have to be a tree.

Modeling note:
Monitoring every shared region {u,v} means every edge (u,v) must be "covered" by at least
one selected endpoint. This is exactly the Minimum Vertex Cover problem.

This solver is exponential-time in the worst case (as expected for NP-hard problems),
but it is an *exact* dynamic programming algorithm with memoization.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Iterable, List, Set, Tuple


def solve_vertex_cover_dp(n: int, edges: Iterable[Tuple[int, int]]) -> Tuple[int, Set[int]]:
    """
    Exact minimum vertex cover via DP over vertex-subset masks.

    State definition:
      R_mask = bitmask of "remaining" vertices (vertices NOT yet chosen).
      The uncovered edges at this state are exactly the edges induced by R_mask,
      i.e., edges (u,v) where both u and v are still in R_mask.

    Recurrence:
      If there is no edge inside R_mask -> cost 0, choose empty set.
      Otherwise pick any uncovered edge (u,v) inside R_mask.
      In any vertex cover, at least one of u or v must be chosen,
      i.e., removed from R_mask:
        solve(R) = 1 + min( solve(R \\ {u}), solve(R \\ {v}) )

    Returns:
      (min_size, chosen_set)
    """
    # Build adjacency bitmasks
    adj: List[int] = [0] * n
    for u, v in edges:
        if u == v:
            # Self-loop must be covered by selecting u (or v), but u==v.
            # We'll just set adjacency bit so it is detected as an "edge inside R".
            adj[u] |= 1 << u
            continue
        adj[u] |= 1 << v
        adj[v] |= 1 << u

    full_mask = (1 << n) - 1

    def find_any_edge_in_induced_subgraph(r_mask: int) -> Tuple[int, int] | None:
        """Return (u,v) such that u-v is an uncovered edge inside r_mask, else None."""
        # Scan vertices; if u has any neighbor within r_mask, we found an uncovered edge.
        rm = r_mask
        while rm:
            lsb = rm & -rm
            u = (lsb.bit_length() - 1)
            rm ^= lsb
            neigh_in_r = adj[u] & r_mask
            # For self-loop u-u, neigh_in_r includes u bit. For normal edges, any neighbor bit.
            if neigh_in_r:
                v_bit = neigh_in_r & -neigh_in_r
                v = v_bit.bit_length() - 1
                if u == v and not (adj[u] & (1 << u)):
                    continue
                return u, v
        return None

    choice: dict[int, int] = {}  # r_mask -> chosen vertex at this state (remove from R)

    @lru_cache(maxsize=None)
    def dp(r_mask: int) -> int:
        edge = find_any_edge_in_induced_subgraph(r_mask)
        if edge is None:
            return 0
        u, v = edge

        # Branch: choose u or choose v (remove from remaining set)
        r_without_u = r_mask & ~(1 << u)
        r_without_v = r_mask & ~(1 << v)

        cu = 1 + dp(r_without_u)
        cv = 1 + dp(r_without_v)

        # Deterministic tie-break: choose smaller vertex id
        if cu < cv or (cu == cv and u <= v):
            choice[r_mask] = u
            return cu
        else:
            choice[r_mask] = v
            return cv

    best = dp(full_mask)

    # Reconstruct chosen set by replaying decisions from full_mask
    chosen: Set[int] = set()
    r = full_mask
    while True:
        edge = find_any_edge_in_induced_subgraph(r)
        if edge is None:
            break
        picked = choice[r]
        chosen.add(picked)
        r &= ~(1 << picked)

    return best, chosen


def is_vertex_cover(n: int, edges: Iterable[Tuple[int, int]], cover: Set[int]) -> bool:
    """Utility: verify cover correctness."""
    for u, v in edges:
        if u not in cover and v not in cover:
            return False
    return True


if __name__ == "__main__":
    # Quick sanity checks
    # Triangle: minimum vertex cover size is 2
    n = 3
    edges = [(0, 1), (1, 2), (2, 0)]
    k, cover = solve_vertex_cover_dp(n, edges)
    print("triangle:", k, sorted(cover), "valid:", is_vertex_cover(n, edges, cover))

