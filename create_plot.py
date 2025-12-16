"""
Create performance plot from benchmark results.
I'm using matplotlib to visualize CPU time vs input size.
"""
import matplotlib.pyplot as plt
import numpy as np

# Read benchmark results
sizes = []
times = []

with open('benchmark_results.txt', 'r') as f:
    next(f)  # Skip header
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) == 2:
            sizes.append(int(parts[0]))
            times.append(float(parts[1]))

# Create plot
plt.figure(figsize=(10, 6))
plt.plot(sizes, times, 'b-', linewidth=2, label='Average CPU Time')
plt.scatter(sizes, times, s=20, alpha=0.6)

plt.xlabel('Input Size (n)', fontsize=12)
plt.ylabel('Average CPU Time (seconds)', fontsize=12)
plt.title('Algorithm Performance: CPU Time vs Input Size', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()

# Use log scale for better visualization
plt.xscale('log')
plt.yscale('log')

plt.tight_layout()
plt.savefig('performance_plot.png', dpi=300, bbox_inches='tight')
print("Plot saved to performance_plot.png")

# Also create linear scale version
plt.figure(figsize=(10, 6))
plt.plot(sizes, times, 'b-', linewidth=2, label='Average CPU Time')
plt.scatter(sizes, times, s=20, alpha=0.6)

plt.xlabel('Input Size (n)', fontsize=12)
plt.ylabel('Average CPU Time (seconds)', fontsize=12)
plt.title('Algorithm Performance: CPU Time vs Input Size (Linear Scale)', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.savefig('performance_plot_linear.png', dpi=300, bbox_inches='tight')
print("Linear scale plot saved to performance_plot_linear.png")

