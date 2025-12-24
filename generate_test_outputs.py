"""
Generate test instance files and their outputs for Task 5 (GENERAL GRAPHS).

We model the monitoring requirement as Minimum Vertex Cover:
- cdps are vertices
- shared regions {u,v} are edges
- selecting a camera at u monitors all shared regions incident to u
- we need the smallest set of vertices that touches (covers) every edge
"""
import os
from vertex_cover_dp import solve_vertex_cover_dp, is_vertex_cover

# 7 functional test instances (white-box + black-box), including cycles.
test_instances = [
    {
        "name": "test_1_single_node",
        "description": "Single node (no edges)",
        "n": 1,
        "edges": [],
        "expected": 0
    },
    {
        "name": "test_2_two_nodes",
        "description": "Two nodes (single edge)",
        "n": 2,
        "edges": [(0, 1)],
        "expected": 1
    },
    {
        "name": "test_3_triangle_cycle",
        "description": "Triangle cycle 0-1-2-0 (cycle counterexample)",
        "n": 3,
        "edges": [(0, 1), (1, 2), (2, 0)],
        "expected": 2
    },
    {
        "name": "test_4_star_graph",
        "description": "Star graph (center covers all edges)",
        "n": 5,
        "edges": [(0, 1), (0, 2), (0, 3), (0, 4)],
        "expected": 1
    },
    {
        "name": "test_5_cycle_5",
        "description": "Cycle of 5 nodes (0-1-2-3-4-0)",
        "n": 5,
        "edges": [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)],
        "expected": 3
    },
    {
        "name": "test_6_forest_2_components",
        "description": "Disconnected graph: one edge + one triangle",
        "n": 5,
        "edges": [(0, 1), (2, 3), (3, 4), (4, 2)],
        "expected": 3
    },
    {
        "name": "test_7_complete_graph_k5",
        "description": "Complete graph K5 (dense case)",
        "n": 5,
        "edges": [(0,1),(0,2),(0,3),(0,4),(1,2),(1,3),(1,4),(2,3),(2,4),(3,4)],
        "expected": 4
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
        f.write(f"\nExpected minimum cameras (= min vertex cover size): {test['expected']}\n")
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
        f.write(f"Is valid vertex cover?: {is_vertex_cover(test['n'], test['edges'], result['cameras'])}\n")
        f.write(f"Expected: {test['expected']}\n")
        f.write(f"Status: {'PASS' if result['count'] == test['expected'] else 'FAIL'}\n")
    return filename

def main():
    """Generate all test instance files and outputs."""
    print("Generating test instance files and outputs...")
    test_dir = create_test_directory()
    
    for test in test_instances:
        print(f"Processing {test['name']}...")
        
        # Run algorithm (exact DP for general graphs)
        cnt, cams = solve_vertex_cover_dp(test['n'], test['edges'])
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

