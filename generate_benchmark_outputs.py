"""
Generate benchmark instance files and their outputs for Task 6.
I'm creating directories for each input size, with instance files and outputs.
"""
import os
from benchmark_dp_forest import generate_benchmark_instances
from dp_forest import min_cameras_forest_with_solution

def create_benchmark_directory():
    """Create benchmark_suite directory structure."""
    base_dir = "benchmark_suite"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    return base_dir

def write_benchmark_instance(base_dir, size_dir, instance_id, name, n, edges):
    """Write a benchmark instance file."""
    filename = os.path.join(size_dir, f"instance_{instance_id:04d}_input.txt")
    with open(filename, 'w') as f:
        f.write(f"Benchmark Instance: {name}\n")
        f.write(f"Instance ID: {instance_id}\n")
        f.write(f"Number of nodes (n): {n}\n")
        f.write(f"Number of edges (m): {len(edges)}\n")
        f.write(f"Edges:\n")
        for u, v in edges:
            f.write(f"  {u} {v}\n")
    return filename

def write_benchmark_output(size_dir, instance_id, name, n, result):
    """Write benchmark output file."""
    filename = os.path.join(size_dir, f"instance_{instance_id:04d}_output.txt")
    with open(filename, 'w') as f:
        f.write(f"Benchmark Instance: {name}\n")
        f.write(f"Instance ID: {instance_id}\n")
        f.write(f"Number of nodes (n): {n}\n")
        f.write(f"\nAlgorithm Result:\n")
        f.write(f"Minimum number of cameras: {result['count']}\n")
        f.write(f"Selected camera cdps (nodes): {sorted(result['cameras'])}\n")
    return filename

def main():
    """Generate benchmark suite files and outputs."""
    print("Generating benchmark instances...")
    instances = generate_benchmark_instances()
    print(f"Total instances: {len(instances)}")
    
    base_dir = create_benchmark_directory()
    
    # Group instances by input size
    instances_by_size = {}
    for name, n, edges in instances:
        if n not in instances_by_size:
            instances_by_size[n] = []
        instances_by_size[n].append((name, n, edges))
    
    print(f"\nProcessing {len(instances_by_size)} different input sizes...")
    
    total_processed = 0
    for size in sorted(instances_by_size.keys()):
        size_dir = os.path.join(base_dir, f"size_{size}")
        if not os.path.exists(size_dir):
            os.makedirs(size_dir)
        
        size_instances = instances_by_size[size]
        print(f"\nProcessing size {size} ({len(size_instances)} instances)...")
        
        for idx, (name, n, edges) in enumerate(size_instances, 1):
            instance_id = total_processed + idx
            
            # Run algorithm
            cnt, cams = min_cameras_forest_with_solution(n, edges)
            result = {"count": cnt, "cameras": cams}
            
            # Write input file
            input_file = write_benchmark_instance(base_dir, size_dir, instance_id, name, n, edges)
            
            # Write output file
            output_file = write_benchmark_output(size_dir, instance_id, name, n, result)
            
            if idx % 50 == 0 or idx == len(size_instances):
                print(f"  Processed {idx}/{len(size_instances)} instances...")
        
        total_processed += len(size_instances)
        print(f"  Completed size {size}: {len(size_instances)} instances in '{size_dir}/'")
    
    print(f"\nAll benchmark instances generated in '{base_dir}/' directory")
    print(f"Total: {total_processed} instances across {len(instances_by_size)} sizes")

if __name__ == "__main__":
    main()

