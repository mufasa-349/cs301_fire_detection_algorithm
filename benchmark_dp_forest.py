"""
Performance benchmarking for the minimum camera placement algorithm.
I'm generating diverse benchmark instances and measuring CPU time to evaluate
computational performance and verify asymptotic complexity.
"""
import time
import random
import statistics
from typing import List, Tuple, Dict
from dp_forest import min_cameras_forest


def generate_path_tree(n: int) -> Tuple[int, List[Tuple[int, int]]]:
    """
    Generate a path graph (linear tree).
    I'm creating this because paths are simple structures that test basic DP.
    """
    edges = [(i, i + 1) for i in range(n - 1)]
    return n, edges


def generate_star_tree(n: int) -> Tuple[int, List[Tuple[int, int]]]:
    """
    Generate a star graph (center connected to all others).
    I'm using this to test high-degree vertex handling.
    """
    edges = [(0, i) for i in range(1, n)]
    return n, edges


def generate_binary_tree(n: int) -> Tuple[int, List[Tuple[int, int]]]:
    """
    Generate a balanced binary tree.
    I'm creating this to test hierarchical structures.
    """
    edges = []
    for i in range(n):
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n:
            edges.append((i, left))
        if right < n:
            edges.append((i, right))
    return n, edges


def generate_random_tree(n: int, seed: int = None) -> Tuple[int, List[Tuple[int, int]]]:
    """
    Generate a random tree using Prüfer sequence method.
    I'm using this to test algorithm on diverse tree structures.
    """
    if seed is not None:
        random.seed(seed)
    
    if n <= 1:
        return n, []
    if n == 2:
        return n, [(0, 1)]
    
    # Generate Prüfer sequence for random tree
    prufer = [random.randint(0, n - 1) for _ in range(n - 2)]
    
    # Build tree from Prüfer sequence
    degree = [1] * n
    for node in prufer:
        degree[node] += 1
    
    edges = []
    for node in prufer:
        for i in range(n):
            if degree[i] == 1:
                edges.append((node, i))
                degree[node] -= 1
                degree[i] -= 1
                break
    
    # Add last edge
    remaining = [i for i in range(n) if degree[i] == 1]
    if len(remaining) == 2:
        edges.append((remaining[0], remaining[1]))
    
    return n, edges


def generate_forest(n: int, num_components: int, seed: int = None) -> Tuple[int, List[Tuple[int, int]]]:
    """
    Generate a forest with multiple tree components.
    I'm creating this to test component detection and independent processing.
    """
    if seed is not None:
        random.seed(seed)
    
    if num_components > n:
        num_components = n
    
    # Distribute nodes among components
    component_sizes = [n // num_components] * num_components
    remainder = n % num_components
    for i in range(remainder):
        component_sizes[i] += 1
    
    edges = []
    node_offset = 0
    
    for size in component_sizes:
        if size > 1:
            # Generate a random tree for this component
            _, comp_edges = generate_random_tree(size, seed=(seed + node_offset) if seed else None)
            # Adjust node indices
            for u, v in comp_edges:
                edges.append((u + node_offset, v + node_offset))
        node_offset += size
    
    return n, edges


def generate_benchmark_instances() -> List[Tuple[str, int, List[Tuple[int, int]]]]:
    """
    Generate diverse benchmark instances.
    I'm creating instances ranging from small (seconds) to large (hours) to test scalability.
    """
    instances = []
    instance_id = 0
    
    # Small instances (10-100 nodes) - should solve in seconds
    for n in range(10, 101, 5):
        for i in range(10):  # 10 instances per size
            # Path trees
            _, edges = generate_path_tree(n)
            instances.append((f"path_{n}_{i}", n, edges))
            
            # Star trees
            _, edges = generate_star_tree(n)
            instances.append((f"star_{n}_{i}", n, edges))
            
            # Binary trees
            _, edges = generate_binary_tree(n)
            instances.append((f"binary_{n}_{i}", n, edges))
            
            # Random trees
            _, edges = generate_random_tree(n, seed=instance_id)
            instances.append((f"random_{n}_{i}", n, edges))
            instance_id += 1
            
            # Forests (2-5 components)
            num_comp = random.randint(2, min(5, n // 10 + 1))
            _, edges = generate_forest(n, num_comp, seed=instance_id)
            instances.append((f"forest_{n}_{i}", n, edges))
            instance_id += 1
    
    # Medium instances (100-1000 nodes) - should solve in minutes
    for n in range(100, 1001, 50):
        for i in range(10):
            _, edges = generate_random_tree(n, seed=instance_id)
            instances.append((f"random_{n}_{i}", n, edges))
            instance_id += 1
            
            # Some forests
            if i % 3 == 0:
                num_comp = random.randint(2, min(10, n // 50 + 1))
                _, edges = generate_forest(n, num_comp, seed=instance_id)
                instances.append((f"forest_{n}_{i}", n, edges))
                instance_id += 1
    
    # Large instances (1000-10000 nodes) - should solve in hours for largest
    for n in range(1000, 10001, 500):
        for i in range(10):
            _, edges = generate_random_tree(n, seed=instance_id)
            instances.append((f"random_{n}_{i}", n, edges))
            instance_id += 1
    
    return instances


def run_benchmark(instances: List[Tuple[str, int, List[Tuple[int, int]]]]) -> Dict[int, List[float]]:
    """
    Run benchmark and collect CPU times.
    I'm measuring CPU time for each instance and grouping by input size.
    """
    times_by_size: Dict[int, List[float]] = {}
    
    print("=" * 80)
    print("BENCHMARKING ALGORITHM PERFORMANCE")
    print("=" * 80)
    print(f"Total instances: {len(instances)}")
    print()
    
    for idx, (name, n, edges) in enumerate(instances, 1):
        # Measure CPU time
        start_time = time.perf_counter()
        result = min_cameras_forest(n, edges)
        end_time = time.perf_counter()
        
        cpu_time = end_time - start_time
        
        # Group by input size
        if n not in times_by_size:
            times_by_size[n] = []
        times_by_size[n].append(cpu_time)
        
        # Progress update
        if idx % 50 == 0 or idx == len(instances):
            print(f"Processed {idx}/{len(instances)} instances...")
    
    print()
    print("=" * 80)
    print("BENCHMARK COMPLETE")
    print("=" * 80)
    
    return times_by_size


def analyze_results(times_by_size: Dict[int, List[float]]) -> Tuple[List[int], List[float]]:
    """
    Analyze benchmark results and compute average times per input size.
    I'm computing averages to see the trend as input size increases.
    """
    sizes = sorted(times_by_size.keys())
    avg_times = [statistics.mean(times_by_size[n]) for n in sizes]
    
    print("\n" + "=" * 80)
    print("PERFORMANCE ANALYSIS")
    print("=" * 80)
    print(f"{'Input Size (n)':<20} {'Instances':<15} {'Avg CPU Time (s)':<20} {'Min Time (s)':<15} {'Max Time (s)':<15}")
    print("-" * 80)
    
    for n in sizes:
        times = times_by_size[n]
        avg = statistics.mean(times)
        min_t = min(times)
        max_t = max(times)
        print(f"{n:<20} {len(times):<15} {avg:<20.6f} {min_t:<15.6f} {max_t:<15.6f}")
    
    return sizes, avg_times


def save_results_for_plotting(sizes: List[int], avg_times: List[float], filename: str = "benchmark_results.txt"):
    """
    Save results to file for plotting.
    I'm saving this so we can create plots in LaTeX or Python.
    """
    with open(filename, 'w') as f:
        f.write("Input_Size\tAvg_CPU_Time\n")
        for n, t in zip(sizes, avg_times):
            f.write(f"{n}\t{t}\n")
    print(f"\nResults saved to {filename}")


if __name__ == "__main__":
    print("Generating benchmark instances...")
    instances = generate_benchmark_instances()
    print(f"Generated {len(instances)} instances")
    print(f"Input sizes range: {min(n for _, n, _ in instances)} to {max(n for _, n, _ in instances)}")
    print()
    
    # Run benchmark
    times_by_size = run_benchmark(instances)
    
    # Analyze results
    sizes, avg_times = analyze_results(times_by_size)
    
    # Save for plotting
    save_results_for_plotting(sizes, avg_times)
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total instances tested: {len(instances)}")
    print(f"Number of different input sizes: {len(sizes)}")
    print(f"Smallest input size: {min(sizes)}")
    print(f"Largest input size: {max(sizes)}")
    print(f"Fastest average time: {min(avg_times):.6f} seconds (n={sizes[avg_times.index(min(avg_times))]})")
    print(f"Slowest average time: {max(avg_times):.6f} seconds (n={sizes[avg_times.index(max(avg_times))]})")

