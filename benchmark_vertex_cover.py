"""
Benchmark generator + runner for Minimum Vertex Cover DP (general graphs).

Important: This is exponential-time in worst case (O(2^n)), so we keep n modest.
We generate:
- at least 200 instances
- at least 20 different input sizes
- at least 10 instances per size
"""

from __future__ import annotations

import random
import time
import statistics
from typing import Dict, Iterable, List, Tuple

from vertex_cover_dp import solve_vertex_cover_dp


Edge = Tuple[int, int]


def normalize_edges(edges: Iterable[Edge]) -> List[Edge]:
    s = set()
    for u, v in edges:
        if u == v:
            continue
        if u > v:
            u, v = v, u
        s.add((u, v))
    return sorted(s)


def gen_cycle(n: int) -> List[Edge]:
    return [(i, (i + 1) % n) for i in range(n)]


def gen_path(n: int) -> List[Edge]:
    return [(i, i + 1) for i in range(n - 1)]


def gen_random_gnp(n: int, p: float, seed: int) -> List[Edge]:
    rnd = random.Random(seed)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if rnd.random() < p:
                edges.append((i, j))
    # Ensure not empty too often: if empty, add one random edge
    if n >= 2 and not edges:
        edges.append((0, 1))
    return normalize_edges(edges)


def gen_bipartite(n_left: int, n_right: int, p: float, seed: int) -> List[Edge]:
    rnd = random.Random(seed)
    edges = []
    offset = n_left
    for i in range(n_left):
        for j in range(n_right):
            if rnd.random() < p:
                edges.append((i, offset + j))
    if (n_left + n_right) >= 2 and not edges:
        edges.append((0, offset))
    return normalize_edges(edges)


def generate_benchmark_instances(
    sizes: List[int],
    instances_per_size: int = 10,
    seed: int = 12345,
) -> List[Tuple[str, int, List[Edge]]]:
    """
    Produce a diverse benchmark suite per size:
    - cycle
    - path
    - random G(n,p) with multiple p
    - bipartite random
    """
    rnd = random.Random(seed)
    instances: List[Tuple[str, int, List[Edge]]] = []
    inst_id = 0

    for n in sizes:
        for k in range(instances_per_size):
            inst_id += 1
            # Mix types
            t = k % 5
            if t == 0:
                edges = gen_cycle(n) if n >= 3 else gen_path(n)
                name = f"cycle_{n}_{k}"
            elif t == 1:
                edges = gen_path(n)
                name = f"path_{n}_{k}"
            elif t == 2:
                p = rnd.choice([0.10, 0.15, 0.20, 0.25])
                edges = gen_random_gnp(n, p, seed=seed + inst_id)
                name = f"gnp_{n}_p{int(p*100)}_{k}"
            elif t == 3:
                p = rnd.choice([0.20, 0.30, 0.40])
                left = n // 2
                right = n - left
                edges = gen_bipartite(left, right, p, seed=seed + inst_id)
                name = f"bip_{n}_p{int(p*100)}_{k}"
            else:
                # Slightly denser random
                p = rnd.choice([0.30, 0.35])
                edges = gen_random_gnp(n, p, seed=seed + inst_id)
                name = f"gnp_dense_{n}_p{int(p*100)}_{k}"

            instances.append((name, n, edges))

    return instances


def time_solve(n: int, edges: List[Edge]) -> float:
    start = time.perf_counter()
    solve_vertex_cover_dp(n, edges)
    end = time.perf_counter()
    return end - start


def run_benchmark(instances: List[Tuple[str, int, List[Edge]]]) -> Dict[int, List[float]]:
    times_by_size: Dict[int, List[float]] = {}
    for idx, (_name, n, edges) in enumerate(instances, 1):
        t = time_solve(n, edges)
        times_by_size.setdefault(n, []).append(t)
        if idx % 50 == 0:
            print(f"Processed {idx}/{len(instances)} instances...")
    return times_by_size


def write_results(times_by_size: Dict[int, List[float]], out_path: str = "benchmark_results_vc.txt") -> None:
    sizes = sorted(times_by_size.keys())
    with open(out_path, "w") as f:
        f.write("n\tk\tavg_s\tmin_s\tmax_s\n")
        for n in sizes:
            ts = times_by_size[n]
            f.write(f"{n}\t{len(ts)}\t{statistics.mean(ts)}\t{min(ts)}\t{max(ts)}\n")


if __name__ == "__main__":
    # 20 different input sizes, 10 instances each => 200 instances
    sizes = list(range(10, 30))  # 10..29 (20 sizes)
    instances = generate_benchmark_instances(sizes, instances_per_size=10)
    print(f"Total instances: {len(instances)} (sizes: {len(sizes)})")
    times = run_benchmark(instances)
    write_results(times)
    print("Wrote benchmark_results_vc.txt")


