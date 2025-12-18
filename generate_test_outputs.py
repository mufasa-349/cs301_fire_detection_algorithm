"""
Generate test instance files and their outputs for Task 5.
I'm creating input files describing each test instance and output files
with the results from running the algorithm.
"""
import os
from dp_forest import min_cameras_forest_with_solution

# Test instances from test_dp_forest.py
test_instances = [
    {
        "name": "test_1_single_node",
        "description": "Single node (isolated vertex)",
        "n": 1,
        "edges": [],
        "expected": 1
    },
    {
        "name": "test_2_two_nodes",
        "description": "Two nodes (single edge)",
        "n": 2,
        "edges": [(0, 1)],
        "expected": 1
    },
    {
        "name": "test_3_path_3_nodes",
        "description": "Path of 3 nodes",
        "n": 3,
        "edges": [(0, 1), (1, 2)],
        "expected": 1
    },
    {
        "name": "test_4_star_graph",
        "description": "Star graph (center with multiple leaves)",
        "n": 5,
        "edges": [(0, 1), (0, 2), (0, 3), (0, 4)],
        "expected": 1
    },
    {
        "name": "test_5_binary_tree",
        "description": "Binary tree (balanced)",
        "n": 7,
        "edges": [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)],
        "expected": 2
    },
    {
        "name": "test_6_forest_2_components",
        "description": "Forest with multiple components",
        "n": 6,
        "edges": [(0, 1), (1, 2), (3, 4), (4, 5)],
        "expected": 2
    },
    {
        "name": "test_7_complex_tree",
        "description": "Complex tree structure",
        "n": 5,
        "edges": [(0, 1), (1, 2), (1, 3), (3, 4)],
        "expected": 2
    }
]

def create_test_directory():
    """Create test_instances directory structure."""
    base_dir = "test_instances"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    return base_dir

def write_instance_file(test_dir, test):
    """Write input file describing the test instance."""
    filename = os.path.join(test_dir, f"{test['name']}_input.txt")
    with open(filename, 'w') as f:
        f.write(f"Test Instance: {test['name']}\n")
        f.write(f"Description: {test['description']}\n")
        f.write(f"Number of nodes (n): {test['n']}\n")
        f.write(f"Number of edges (m): {len(test['edges'])}\n")
        f.write(f"Edges:\n")
        for u, v in test['edges']:
            f.write(f"  {u} {v}\n")
        f.write(f"\nExpected minimum cameras: {test['expected']}\n")
    return filename

def write_output_file(test_dir, test, result):
    """Write output file with algorithm result."""
    filename = os.path.join(test_dir, f"{test['name']}_output.txt")
    with open(filename, 'w') as f:
        f.write(f"Test Instance: {test['name']}\n")
        f.write(f"Description: {test['description']}\n")
        f.write(f"\nAlgorithm Result:\n")
        f.write(f"Minimum number of cameras: {result['count']}\n")
        f.write(f"Selected camera cdps (nodes): {sorted(result['cameras'])}\n")
        f.write(f"Expected: {test['expected']}\n")
        f.write(f"Status: {'PASS' if result['count'] == test['expected'] else 'FAIL'}\n")
    return filename

def main():
    """Generate all test instance files and outputs."""
    print("Generating test instance files and outputs...")
    test_dir = create_test_directory()
    
    for test in test_instances:
        print(f"Processing {test['name']}...")
        
        # Run algorithm
        cnt, cams = min_cameras_forest_with_solution(test['n'], test['edges'])
        result = {"count": cnt, "cameras": cams}
        
        # Write input file
        input_file = write_instance_file(test_dir, test)
        print(f"  Created: {input_file}")
        
        # Write output file
        output_file = write_output_file(test_dir, test, result)
        print(f"  Created: {output_file}")
    
    print(f"\nAll test instances generated in '{test_dir}/' directory")
    print(f"Total: {len(test_instances)} test instances")

if __name__ == "__main__":
    main()

