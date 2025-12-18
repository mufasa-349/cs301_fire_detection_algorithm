"""
Dynamic programming solution for minimum camera placement on trees (forests).
Note: The problem is NP-hard for general graphs, but this solution works by
assuming each connected component is a tree with a designated root.
"""
from __future__ import annotations

from collections import defaultdict
from math import inf
from typing import Dict, Iterable, List, Set, Tuple, Optional


def build_adj(n: int, edges: Iterable[Tuple[int, int]]) -> List[List[int]]:
    """
    Helper function to build an adjacency list from edge list.
    I'm doing this because we need to traverse the graph efficiently,
    and adjacency lists are perfect for tree traversal.
    """
    adj: List[List[int]] = [[] for _ in range(n)]
    for u, v in edges:
        # Adding bidirectional edges since the graph is undirected
        adj[u].append(v)
        adj[v].append(u)
    return adj


def min_cameras_for_tree(adj: List[List[int]], root: int = 0) -> int:
    """
    Returns the minimum number of cameras needed to monitor all nodes in a tree.
    
    I'm using three states for each node to track different monitoring scenarios:
      State 0: Camera is placed at this node
      State 1: No camera here, but at least one child has a camera (node is monitored)
      State 2: No camera here, node is not yet monitored (must be covered by parent)
    
    The key insight: we need to ensure every node is either covered by itself,
    a child, or a parent. This DP formulation captures all these cases.
    """
    n = len(adj)
    # dp[v][state] stores the minimum cameras needed for subtree rooted at v
    # given that v is in the specified state
    dp: List[List[int]] = [[0, 0, 0] for _ in range(n)]

    def dfs(v: int, parent: int) -> None:
        """
        DFS traversal to compute DP values bottom-up.
        I'm doing post-order traversal so children are processed before parent.
        """
        # Base case: if we place a camera at v, cost is 1
        dp[v][0] = 1
        # Initially, state 1 is impossible (no children processed yet)
        dp[v][1] = inf
        # State 2: no camera at v, waiting for parent (cost 0 for v itself)
        dp[v][2] = 0

        # For state 1, I need to track the minimum "extra cost" of placing
        # a camera in at least one child. This is why I use base and gain.
        base = 0  # Base cost if all children are in state 0 or 1
        gain = inf  # Minimum extra cost to ensure at least one child has a camera
        
        for c in adj[v]:
            if c == parent:
                continue  # Skip parent to avoid going back up the tree
            
            # Process child first (post-order)
            dfs(c, v)

            # For state 0: if v has a camera, children can be in any state
            m02 = min(dp[c][0], dp[c][1], dp[c][2])
            # For state 2: if v waits for parent, children must be self-sufficient
            # (state 0 or 1, but not 2, since v can't help them)
            m01 = min(dp[c][0], dp[c][1])
            
            dp[v][0] += m02
            dp[v][2] += m01

            # For state 1: we need at least one child in state 0
            # base is the cost if we assume all children are in state 0 or 1
            base += m01
            # gain tracks the minimum extra cost to force one child into state 0
            gain = min(gain, dp[c][0] - m01)

        # If v has children, state 1 is achievable
        if gain < inf:
            dp[v][1] = base + gain

    dfs(root, -1)
    # Root must be monitored (can't wait for parent), so only states 0 and 1 are valid
    return min(dp[root][0], dp[root][1])


def min_cameras_for_tree_with_solution(adj: List[List[int]], root: int = 0) -> Tuple[int, Set[int]]:
    """
    Same DP as `min_cameras_for_tree`, but also reconstructs *which* nodes (cdps)
    should get cameras.

    I'm doing this because the assignment's wording asks for the smallest set of cdps,
    not just the size of that set.

    Returns:
      (min_camera_count, camera_nodes_set)
    """
    n = len(adj)
    dp: List[List[float]] = [[0.0, 0.0, 0.0] for _ in range(n)]
    # For state 1, we must force at least one child into state 0.
    # This array remembers *which* child provides the minimal "gain".
    best_child_for_state1: List[Optional[int]] = [None] * n

    def dfs(v: int, parent: int) -> None:
        dp[v][0] = 1.0
        dp[v][1] = inf
        dp[v][2] = 0.0

        base = 0.0
        gain = inf
        best_child = None

        for c in adj[v]:
            if c == parent:
                continue
            dfs(c, v)

            m02 = min(dp[c][0], dp[c][1], dp[c][2])
            m01 = min(dp[c][0], dp[c][1])

            dp[v][0] += m02
            dp[v][2] += m01

            base += m01
            child_gain = dp[c][0] - m01
            if child_gain < gain:
                gain = child_gain
                best_child = c

        if best_child is not None:
            dp[v][1] = base + gain
            best_child_for_state1[v] = best_child

    def argmin_state(values: List[float], allowed_states: Tuple[int, ...]) -> int:
        """Deterministic tie-breaking: pick the smallest state index among minima."""
        best_s = allowed_states[0]
        best_v = values[best_s]
        for s in allowed_states[1:]:
            if values[s] < best_v - 1e-12 or (abs(values[s] - best_v) <= 1e-12 and s < best_s):
                best_s = s
                best_v = values[s]
        return best_s

    cameras: Set[int] = set()

    def recon(v: int, parent: int, state: int) -> None:
        # State 0 => camera at v
        if state == 0:
            cameras.add(v)
            for c in adj[v]:
                if c == parent:
                    continue
                cs = argmin_state(dp[c], (0, 1, 2))
                recon(c, v, cs)
            return

        # State 2 => v is waiting for parent, so children must be self-sufficient (0 or 1)
        if state == 2:
            for c in adj[v]:
                if c == parent:
                    continue
                cs = argmin_state(dp[c], (0, 1))
                recon(c, v, cs)
            return

        # State 1 => v is dominated by at least one child camera
        # We enforce exactly one "forced" child into state 0 (chosen during DP),
        # and the remaining children can be in min(0,1).
        forced = best_child_for_state1[v]
        for c in adj[v]:
            if c == parent:
                continue
            if forced is not None and c == forced:
                recon(c, v, 0)
            else:
                cs = argmin_state(dp[c], (0, 1))
                recon(c, v, cs)

    dfs(root, -1)
    root_state = argmin_state(dp[root], (0, 1))  # root cannot be in state 2
    recon(root, -1, root_state)

    return int(min(dp[root][0], dp[root][1])), cameras


def min_cameras_forest_with_solution(
    n: int, edges: Iterable[Tuple[int, int]], roots: Iterable[int] | None = None
) -> Tuple[int, Set[int]]:
    """
    Forest version that also returns the selected camera cdps.

    Returns:
      (total_min_camera_count, set_of_camera_nodes)
    """
    adj = build_adj(n, edges)
    seen: Set[int] = set()
    total = 0
    cameras: Set[int] = set()
    root_map: Dict[int, int] = defaultdict(int)
    if roots is not None:
        for r in roots:
            root_map[r] = r

    def collect_component(start: int) -> List[int]:
        stack = [start]
        comp = []
        seen.add(start)
        while stack:
            v = stack.pop()
            comp.append(v)
            for nb in adj[v]:
                if nb not in seen:
                    seen.add(nb)
                    stack.append(nb)
        return comp

    for v in range(n):
        if v in seen:
            continue
        component = collect_component(v)
        root = next((r for r in component if r in root_map), component[0])
        cnt, cams = min_cameras_for_tree_with_solution(adj, root)
        total += cnt
        cameras |= cams

    return total, cameras


def min_cameras_forest(
    n: int, edges: Iterable[Tuple[int, int]], roots: Iterable[int] | None = None
) -> int:
    """
    Computes minimum cameras for a forest (multiple connected components).
    
    I'm handling forests by processing each connected component separately.
    Since components are independent, I can just sum up the results.
    
    Parameters:
      n      : number of nodes (0..n-1)
      edges  : list of edges
      roots  : optional list of root nodes for each component. If not provided,
               I'll pick the first node in each component as root.
    """
    adj = build_adj(n, edges)
    seen: Set[int] = set()  # Track visited nodes to find components
    total = 0
    root_map: Dict[int, int] = defaultdict(int)
    if roots is not None:
        # If user specified roots, I'll use them when available
        for r in roots:
            root_map[r] = r

    def collect_component(start: int) -> List[int]:
        """
        BFS to collect all nodes in the same connected component.
        I'm using iterative BFS with a stack to avoid recursion depth issues.
        """
        stack = [start]
        comp = []
        seen.add(start)
        while stack:
            v = stack.pop()
            comp.append(v)
            for nb in adj[v]:
                if nb not in seen:
                    seen.add(nb)
                    stack.append(nb)
        return comp

    # Process each connected component separately
    for v in range(n):
        if v in seen:
            continue  # Already processed this component
        
        # Find all nodes in this component
        component = collect_component(v)
        # Use specified root if available, otherwise use first node
        root = next((r for r in component if r in root_map), component[0])
        # Add cameras needed for this component
        total += min_cameras_for_tree(adj, root)

    return total


if __name__ == "__main__":
    # Example usage: forest with 6 nodes in two components
    # Component 1: path 0-1-2 (needs 1 camera, e.g., at node 1)
    # Component 2: path 3-4-5 (needs 1 camera, e.g., at node 4)
    # Total: 2 cameras
    edges = [(0, 1), (1, 2), (3, 4), (4, 5)]
    n = 6
    result = min_cameras_forest(n, edges)
    result_with_set, cams = min_cameras_forest_with_solution(n, edges)
    print(f"Minimum number of cameras needed: {result}")
    print(f"Selected camera cdps (nodes): {sorted(cams)}")

