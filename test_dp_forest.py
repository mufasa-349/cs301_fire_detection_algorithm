"""
Functional testing for the minimum camera placement algorithm.
I'm creating comprehensive test cases for both white-box and black-box testing.
"""
from dp_forest import min_cameras_forest, min_cameras_for_tree, build_adj


def test_instance_1():
    """
    Instance 1: Single node (isolated vertex)
    Purpose: Test base case - single node must have a camera
    Expected: 1 camera
    """
    n = 1
    edges = []
    result = min_cameras_forest(n, edges)
    return {
        "instance": "Single node",
        "n": n,
        "edges": edges,
        "description": "Isolated vertex (no edges)",
        "expected": 1,
        "actual": result,
        "passed": result == 1,
        "white_box": "Tests leaf node base case (dp[v][0]=1, dp[v][1]=inf, dp[v][2]=0)",
        "black_box": "Tests minimal input - single vertex must be monitored"
    }


def test_instance_2():
    """
    Instance 2: Two nodes (single edge)
    Purpose: Test minimal tree - one camera should cover both
    Expected: 1 camera (at either node)
    """
    n = 2
    edges = [(0, 1)]
    result = min_cameras_forest(n, edges)
    return {
        "instance": "Two nodes",
        "n": n,
        "edges": edges,
        "description": "Path: 0-1",
        "expected": 1,
        "actual": result,
        "passed": result == 1,
        "white_box": "Tests state transitions: one node in state 0 covers neighbor",
        "black_box": "Tests minimal connected graph - edge case"
    }


def test_instance_3():
    """
    Instance 3: Path of 3 nodes
    Purpose: Test simple path - optimal placement at middle
    Expected: 1 camera (at node 1)
    """
    n = 3
    edges = [(0, 1), (1, 2)]
    result = min_cameras_forest(n, edges)
    return {
        "instance": "Path (3 nodes)",
        "n": n,
        "edges": edges,
        "description": "Path: 0-1-2",
        "expected": 1,
        "actual": result,
        "passed": result == 1,
        "white_box": "Tests internal node with two children, state 1 calculation",
        "black_box": "Tests optimal placement in linear structure"
    }


def test_instance_4():
    """
    Instance 4: Star graph (center with multiple leaves)
    Purpose: Test high branching factor - center node covers all
    Expected: 1 camera (at center)
    """
    n = 5
    edges = [(0, 1), (0, 2), (0, 3), (0, 4)]
    result = min_cameras_forest(n, edges)
    return {
        "instance": "Star graph",
        "n": n,
        "edges": edges,
        "description": "Center 0 connected to leaves 1,2,3,4",
        "expected": 1,
        "actual": result,
        "passed": result == 1,
        "white_box": "Tests node with multiple children, gain calculation for state 1",
        "black_box": "Tests high-degree vertex scenario"
    }


def test_instance_5():
    """
    Instance 5: Binary tree (balanced)
    Purpose: Test balanced tree structure
    Expected: 2 cameras (optimal placement)
    """
    n = 7
    edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
    result = min_cameras_forest(n, edges)
    return {
        "instance": "Binary tree",
        "n": n,
        "edges": edges,
        "description": "Balanced binary tree: root 0, level-1: 1,2, level-2: 3,4,5,6",
        "expected": 2,
        "actual": result,
        "passed": result == 2,
        "white_box": "Tests recursive DP on balanced structure, multiple levels",
        "black_box": "Tests hierarchical tree structure"
    }


def test_instance_6():
    """
    Instance 6: Forest with multiple components
    Purpose: Test algorithm on disconnected components
    Expected: Sum of cameras for each component
    """
    n = 6
    edges = [(0, 1), (1, 2), (3, 4), (4, 5)]
    result = min_cameras_forest(n, edges)
    return {
        "instance": "Forest (2 components)",
        "n": n,
        "edges": edges,
        "description": "Component 1: 0-1-2, Component 2: 3-4-5",
        "expected": 2,  # 1 per component
        "actual": result,
        "passed": result == 2,
        "white_box": "Tests component detection and independent processing",
        "black_box": "Tests disconnected graph handling"
    }


def test_instance_7():
    """
    Instance 7: Complex tree structure (from Task 3 example)
    Purpose: Test comprehensive scenario with known optimal solution
    Expected: 3 cameras
    """
    n = 5
    edges = [(0, 1), (1, 2), (1, 3), (3, 4)]
    result = min_cameras_forest(n, edges)
    return {
        "instance": "Complex tree",
        "n": n,
        "edges": edges,
        "description": "Tree: 0-1-2, 1-3-4 (root at 1)",
        "expected": 2,  # Optimal: cameras at nodes 1 and 3 (or 1 and 4)
        "actual": result,
        "passed": result == 2,
        "white_box": "Tests complex state transitions, gain calculation with multiple children",
        "black_box": "Tests realistic scenario with multiple branching points"
    }


def run_all_tests():
    """Run all test instances and collect results."""
    tests = [
        test_instance_1(),
        test_instance_2(),
        test_instance_3(),
        test_instance_4(),
        test_instance_5(),
        test_instance_6(),
        test_instance_7()
    ]
    
    print("=" * 80)
    print("FUNCTIONAL TESTING RESULTS")
    print("=" * 80)
    print()
    
    all_passed = True
    for i, test in enumerate(tests, 1):
        status = "✓ PASS" if test["passed"] else "✗ FAIL"
        print(f"Test {i}: {test['instance']} - {status}")
        print(f"  Description: {test['description']}")
        print(f"  Expected: {test['expected']} cameras, Actual: {test['actual']} cameras")
        print(f"  White-box: {test['white_box']}")
        print(f"  Black-box: {test['black_box']}")
        print()
        if not test["passed"]:
            all_passed = False
    
    print("=" * 80)
    if all_passed:
        print("ALL TESTS PASSED ✓")
    else:
        print("SOME TESTS FAILED ✗")
    print("=" * 80)
    
    return tests


if __name__ == "__main__":
    results = run_all_tests()
    
    # Print summary table
    print("\n" + "=" * 80)
    print("SUMMARY TABLE")
    print("=" * 80)
    print(f"{'Instance':<25} {'Expected':<10} {'Actual':<10} {'Status':<10}")
    print("-" * 80)
    for test in results:
        status = "PASS" if test["passed"] else "FAIL"
        print(f"{test['instance']:<25} {test['expected']:<10} {test['actual']:<10} {status:<10}")

