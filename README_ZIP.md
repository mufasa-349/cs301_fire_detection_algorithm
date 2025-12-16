# ZIP File Structure Guide

This document explains how to create the ZIP file for submission.

## Required Structure

```
submission.zip
├── dp_forest.py                    # Python implementation (Task 4)
├── test_instances/                  # Test instances directory (Task 5)
│   ├── test_1_single_node_input.txt
│   ├── test_1_single_node_output.txt
│   ├── test_2_two_nodes_input.txt
│   ├── test_2_two_nodes_output.txt
│   ├── test_3_path_3_nodes_input.txt
│   ├── test_3_path_3_nodes_output.txt
│   ├── test_4_star_graph_input.txt
│   ├── test_4_star_graph_output.txt
│   ├── test_5_binary_tree_input.txt
│   ├── test_5_binary_tree_output.txt
│   ├── test_6_forest_2_components_input.txt
│   ├── test_6_forest_2_components_output.txt
│   ├── test_7_complex_tree_input.txt
│   └── test_7_complex_tree_output.txt
└── benchmark_suite/                 # Benchmark suite directory (Task 6)
    ├── size_10/
    │   ├── instance_0001_input.txt
    │   ├── instance_0001_output.txt
    │   ├── instance_0002_input.txt
    │   ├── instance_0002_output.txt
    │   └── ...
    ├── size_15/
    │   └── ...
    ├── size_20/
    │   └── ...
    └── ... (one directory per input size)
```

## Steps to Create ZIP File

### Step 1: Generate Test Instance Files
Run the script to generate test instance files and outputs:
```bash
python3 generate_test_outputs.py
```
This creates the `test_instances/` directory with all test files.

### Step 2: Generate Benchmark Suite Files
Run the script to generate benchmark instance files and outputs:
```bash
python3 generate_benchmark_outputs.py
```
**Note:** This may take some time as it processes 1,406 instances. The script will create the `benchmark_suite/` directory with subdirectories for each input size.

### Step 3: Create ZIP File
After both scripts complete, create the ZIP file:
```bash
zip -r submission.zip dp_forest.py test_instances/ benchmark_suite/
```

Or manually:
1. Select these items:
   - `dp_forest.py`
   - `test_instances/` directory (with all contents)
   - `benchmark_suite/` directory (with all contents)
2. Right-click and select "Compress" (Mac) or use your ZIP tool
3. Name it `submission.zip`

## File Descriptions

### dp_forest.py
- Main Python implementation of the DP algorithm
- Contains `min_cameras_forest()` and `min_cameras_for_tree()` functions

### test_instances/
- Contains 7 test instances (Task 5)
- Each test has:
  - `*_input.txt`: Description of the test instance (graph structure, edges, expected result)
  - `*_output.txt`: Algorithm result for that instance

### benchmark_suite/
- Contains benchmark instances organized by input size (Task 6)
- Each size has its own directory: `size_10/`, `size_15/`, `size_20/`, etc.
- Each instance has:
  - `instance_XXXX_input.txt`: Graph description
  - `instance_XXXX_output.txt`: Algorithm result

## Verification

After creating the ZIP, verify it contains:
- ✅ `dp_forest.py` (1 file)
- ✅ `test_instances/` with 14 files (7 inputs + 7 outputs)
- ✅ `benchmark_suite/` with subdirectories for each input size

You can check with:
```bash
unzip -l submission.zip | head -20
```

