#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Maximum Subset Sum problem - Analysis of 2 approximation algorithms experimental
data
1- A 2-approximation greed algorithm
2- A trim scheme algorithm with a approximation ratio of (1+epsilon)

Several instances of sets containing positive integers number, with different
sizes are created and tested for different target values, M, and epsilon values

@author: Andre Wemans, 48432
@author: Pedro Lopes, 57514
"""

#%%imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy import stats
#%% Constants and global variables
file_name = 'mss-data.txt'
lines_to_remove = 2
#%% Read data from file
data = pd.read_csv(file_name, sep= '\t')

#Reomve the last lines due to incomplete data
data = data.iloc[:- lines_to_remove]

#Changing information from 'U' to 'E' in the cases that one of the algorithms
#did obtained a solution with the target value, and in this way it is possible
#to know the optimal value
#Done manually since it only happens in instances of size 10 and for some values
data.iloc[:4, 5] = 'E'
data.iloc[12:16, 5] = 'E'
#%% Plot comparing algorithms ratio value / M for the different M values
# Code obtained from Claude IA
# Convert epsilon to numeric, '-' becomes NaN
data['epsilon'] = pd.to_numeric(data['epsilon'], errors='coerce')

# Calculate approximation gap (distance from optimal)
data['Gap'] = 1 - data['Value / M']

# Create the plot with dimensions optimized for A4 report
fig, ax = plt.subplots(figsize=(7.5, 5))

# Define colors for each algorithm/epsilon combination
colors = {
    'Greedy': '#1f77b4',      # Blue
    'SchemeSS ε=0.5': '#ff7f0e',  # Orange
    'SchemeSS ε=1': '#2ca02c',    # Green
    'SchemeSS ε=2': '#d62728'     # Red
}

# Define markers for exact vs unknown
markers_exact = {'E': 's', 'U': 'o'}  # square for exact, circle for unknown
marker_sizes = {'E': 80, 'U': 50}     # slightly larger squares

# For perfect solutions (Gap = 0), we'll plot them at a very small value
# Find the minimum non-zero gap to determine appropriate placement
min_nonzero_gap = data[data['Gap'] > 0]['Gap'].min()
perfect_gap_display = min_nonzero_gap / 10  # Plot perfect solutions even lower

# Plot Greedy algorithm
greedy_data = data[data['Algorithm'] == 'G']
for exact_type in ['E', 'U']:
    subset = greedy_data[greedy_data['Exact?'] == exact_type]
    if not subset.empty:
        # Separate perfect and non-perfect solutions
        subset_nonzero = subset[subset['Gap'] > 0]
        subset_perfect = subset[subset['Gap'] == 0]
        
        # Plot non-zero gaps
        if not subset_nonzero.empty:
            label = 'Greedy' if exact_type == 'U' else None
            ax.scatter(subset_nonzero['M'], subset_nonzero['Gap'], 
                      color=colors['Greedy'], 
                      marker=markers_exact[exact_type],
                      s=marker_sizes[exact_type],
                      alpha=0.7,
                      label=label,
                      edgecolors='black',
                      linewidths=0.5)
        
        # Plot perfect solutions with star marker
        if not subset_perfect.empty:
            ax.scatter(subset_perfect['M'], 
                      [perfect_gap_display] * len(subset_perfect), 
                      color=colors['Greedy'], 
                      marker='*',
                      s=200,
                      alpha=0.9,
                      edgecolors='black',
                      linewidths=0.8,
                      zorder=10)

# Plot SchemeSS for each epsilon value
epsilon_values = [0.5, 1, 2]
for eps in epsilon_values:
    scheme_data = data[(data['Algorithm'] == 'S') & (data['epsilon'] == eps)]
    label_base = f'SchemeSS ε={eps}'
    
    for exact_type in ['E', 'U']:
        subset = scheme_data[scheme_data['Exact?'] == exact_type]
        if not subset.empty:
            # Separate perfect and non-perfect solutions
            subset_nonzero = subset[subset['Gap'] > 0]
            subset_perfect = subset[subset['Gap'] == 0]
            
            # Plot non-zero gaps
            if not subset_nonzero.empty:
                label = label_base if exact_type == 'U' else None
                ax.scatter(subset_nonzero['M'], subset_nonzero['Gap'], 
                          color=colors[label_base], 
                          marker=markers_exact[exact_type],
                          s=marker_sizes[exact_type],
                          alpha=0.7,
                          label=label,
                          edgecolors='black',
                          linewidths=0.5)
            
            # Plot perfect solutions with star marker
            if not subset_perfect.empty:
                ax.scatter(subset_perfect['M'], 
                          [perfect_gap_display] * len(subset_perfect), 
                          color=colors[label_base], 
                          marker='*',
                          s=200,
                          alpha=0.9,
                          edgecolors='black',
                          linewidths=0.8,
                          zorder=10)

# Set logarithmic scale for both axes
ax.set_xscale('log')
ax.set_yscale('log')

# Invert y-axis so better performance (smaller gaps) is at the top
ax.invert_yaxis()

# Add labels and title
ax.set_xlabel('Target Value (M)', fontsize=11, fontweight='bold')
ax.set_ylabel('Approximation Gap (1 - Value/M)', fontsize=11, fontweight='bold')
ax.set_title('Algorithm Performance: Approximation Gap vs Target Value', 
             fontsize=12, fontweight='bold', pad=15)

# Add grid for better readability
ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

# Create legend
legend1 = ax.legend(loc='lower right', fontsize=9, framealpha=0.9, 
                   title='Algorithm', title_fontsize=10)

# Create a second legend for marker types
marker_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', 
           markersize=7, label='Unknown optimal', markeredgecolor='black', markeredgewidth=0.5),
    Line2D([0], [0], marker='s', color='w', markerfacecolor='gray', 
           markersize=8, label='Exact optimal', markeredgecolor='black', markeredgewidth=0.5),
    Line2D([0], [0], marker='*', color='w', markerfacecolor='gold', 
           markersize=12, label='Perfect (Gap = 0)', markeredgecolor='black', markeredgewidth=0.8)
]
legend2 = ax.legend(handles=marker_elements, loc='upper center', 
                   fontsize=9, framealpha=0.9, 
                   title='Optimality', title_fontsize=10,
                   ncol=3)  # 3 columns to make it horizontal
ax.add_artist(legend1)  # Add back the first legend

# Adjust layout
plt.tight_layout()

# Save the figure
plt.savefig('mss_algorithm_gap_report_with_perfect.png', 
            dpi=300, 
            bbox_inches='tight',
            facecolor='white',
            edgecolor='none')

print("Plot saved successfully!")
print("File: mss_algorithm_gap_report_with_perfect.png")
print(f"Dimensions: 7.5 x 5 inches @ 300 dpi (2250 x 1500 pixels)")
print("\nPerfect solutions (Gap = 0) are shown with gold star markers (★)")

# Optional: Also save as pdf
plt.savefig('mss_algorithm_gap_report_with_perfect.pdf', 
            bbox_inches='tight',
            facecolor='white',
            edgecolor='none')
print("Also saved as Pdf: mss_algorithm_gap_report_with_perfect.pdf")

plt.show()

# Print detailed info about perfect solutions
print("\n" + "="*60)
print("PERFECT SOLUTIONS (Gap = 0)")
print("="*60)
perfect = data[data['Gap'] == 0]
print(perfect[['Sample', 'Size', 'M', 'Algorithm', 'epsilon', 'Value']].to_string(index=False))

print("\n" + "="*60)
print("APPROXIMATION GAP STATISTICS (excluding perfect solutions)")
print("="*60)
print("\nGreedy algorithm:")
greedy_data = data[data['Algorithm'] == 'G']
greedy_gaps = greedy_data[greedy_data['Gap'] > 0]['Gap']
print(f"  Mean gap: {greedy_gaps.mean():.6f} ({greedy_gaps.mean()*100:.4f}%)")
print(f"  Min gap:  {greedy_gaps.min():.6f} ({greedy_gaps.min()*100:.4f}%)")
print(f"  Max gap:  {greedy_gaps.max():.6f} ({greedy_gaps.max()*100:.4f}%)")
print(f"  Perfect solutions: {(greedy_data['Gap'] == 0).sum()}")

for eps in epsilon_values:
    scheme_data = data[(data['Algorithm'] == 'S') & (data['epsilon'] == eps)]
    scheme_gaps = scheme_data[scheme_data['Gap'] > 0]['Gap']
    print(f"\nSchemeSS ε={eps}:")
    print(f"  Mean gap: {scheme_gaps.mean():.6f} ({scheme_gaps.mean()*100:.4f}%)")
    print(f"  Min gap:  {scheme_gaps.min():.6f} ({scheme_gaps.min()*100:.4f}%)")
    print(f"  Max gap:  {scheme_gaps.max():.6f} ({scheme_gaps.max()*100:.4f}%)")
    print(f"  Perfect solutions: {(scheme_data['Gap'] == 0).sum()}")

print("\n" + "="*60)

#%% Plot comparing running time with N
# Code obtained from Claude IA
# Create the plot with dimensions optimized for A4 report
fig, ax = plt.subplots(figsize=(7.5, 5))

# Define colors for each algorithm/epsilon combination
colors = {
    'Greedy': '#1f77b4',      # Blue
    'SchemeSS ε=0.5': '#ff7f0e',  # Orange
    'SchemeSS ε=1': '#2ca02c',    # Green
    'SchemeSS ε=2': '#d62728'     # Red
}

# Define markers for each algorithm
markers = {
    'Greedy': 'o',
    'SchemeSS ε=0.5': 's',
    'SchemeSS ε=1': '^',
    'SchemeSS ε=2': 'D'
}

# Plot Greedy algorithm - individual points
greedy_data = data[data['Algorithm'] == 'G']
ax.errorbar(greedy_data['Size'], greedy_data['t'], 
            yerr=greedy_data['t stdv'],
            color=colors['Greedy'], 
            marker=markers['Greedy'],
            markersize=8,
            linewidth=0,  # No connecting line
            linestyle='',  # No line style
            elinewidth=1.5,  # Error bar line width
            capsize=5,
            capthick=1.5,
            label='Greedy',
            alpha=0.7)

# Plot SchemeSS for each epsilon value - individual points
epsilon_values = [0.5, 1, 2]
for eps in epsilon_values:
    scheme_data = data[(data['Algorithm'] == 'S') & (data['epsilon'] == eps)]
    label_base = f'SchemeSS ε={eps}'
    
    ax.errorbar(scheme_data['Size'], scheme_data['t'], 
                yerr=scheme_data['t stdv'],
                color=colors[label_base], 
                marker=markers[label_base],
                markersize=8,
                linewidth=0,  # No connecting line
                linestyle='',  # No line style
                elinewidth=1.5,  # Error bar line width
                capsize=5,
                capthick=1.5,
                label=label_base,
                alpha=0.7)

# Set logarithmic scale for both axes
ax.set_xscale('log')
ax.set_yscale('log')

# Add labels and title
ax.set_xlabel('Instance Size (n)', fontsize=11, fontweight='bold')
ax.set_ylabel('Execution Time (seconds)', fontsize=11, fontweight='bold')
ax.set_title('Algorithm Scalability: Execution Time vs Instance Size (Individual Points)', 
             fontsize=12, fontweight='bold', pad=15)

# Add grid for better readability
ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
ax.grid(True, which='minor', alpha=0.15, linestyle=':', linewidth=0.3)

# Create legend
ax.legend(loc='upper left', fontsize=9, framealpha=0.9, 
          title='Algorithm', title_fontsize=10)

# Adjust layout
plt.tight_layout()

# Save the figure
plt.savefig('mss_time_vs_size_individual.png', 
            dpi=300, 
            bbox_inches='tight',
            facecolor='white',
            edgecolor='none')

print("Plot saved successfully!")
print("File: mss_time_vs_size_individual.png")
print(f"Dimensions: 7.5 x 5 inches @ 300 dpi (2250 x 1500 pixels)")
print("\nShowing ALL individual data points (no aggregation)")

# Optional: Also save as PDF
plt.savefig('mss_time_vs_size_individual.pdf', 
            bbox_inches='tight',
            facecolor='white',
            edgecolor='none')
print("Also saved as PDF: mss_time_vs_size_individual.pdf")

plt.show()

# Print count of points per algorithm and size
print("\n" + "="*70)
print("NUMBER OF INDIVIDUAL POINTS PLOTTED")
print("="*70)

for size in sorted(data['Size'].unique()):
    print(f"\nSize n = {size}:")
    greedy_count = len(data[(data['Size'] == size) & (data['Algorithm'] == 'G')])
    print(f"  Greedy: {greedy_count} points")
    for eps in epsilon_values:
        scheme_count = len(data[(data['Size'] == size) & (data['Algorithm'] == 'S') & (data['epsilon'] == eps)])
        print(f"  SchemeSS ε={eps}: {scheme_count} points")

print("\n" + "="*70)
print("Each point represents one combination of (Size, Instance, M value)")
print("Error bars show standard deviation from 10 repetitions of each run")
print("="*70)
#%% Plot comparing running time with N
# Code obtained from Claude IA
# Create the plot with dimensions optimized for A4 report

print("="*80)
print("LINEAR REGRESSION IN LOG-LOG SPACE FOR TIME COMPLEXITY ANALYSIS")
print("="*80)
print("\nFitting model: t = c × n^b")
print("In log-log space: log(t) = log(c) + b × log(n)")
print("Where: slope = b (exponent), intercept = log(c)")
print("="*80)

# Store results for later plotting
regression_results = {}

# Greedy algorithm
print("\n" + "="*80)
print("GREEDY ALGORITHM")
print("="*80)
greedy_data = data[data['Algorithm'] == 'G'].copy()

# For regression, exclude N=10 data points
greedy_regression = greedy_data[greedy_data['Size'] > 10].copy()

print(f"\nTotal data points: {len(greedy_data)}")
print(f"Data points used for regression (excluding n=10): {len(greedy_regression)}")

# Take logarithms
log_n = np.log10(greedy_regression['Size'].values)
log_t = np.log10(greedy_regression['t'].values)

# Perform linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(log_n, log_t)

# Calculate the constant c
c = 10**intercept

print(f"\nRegression results:")
print(f"  Slope (b):       {slope:.4f}")
print(f"  Intercept:       {intercept:.4f}")
print(f"  Constant (c):    {c:.4e}")
print(f"  R² value:        {r_value**2:.6f}  (goodness of fit, 1.0 = perfect)")
print(f"  P-value:         {p_value:.6e}")
print(f"  Std error:       {std_err:.6f}")

print(f"\n✓ Time complexity: t ≈ {c:.2e} × n^{slope:.2f}")
print(f"✓ Big-O notation:  O(n^{slope:.2f})")

# Store for plotting
regression_results['Greedy'] = {
    'slope': slope,
    'intercept': intercept,
    'c': c,
    'r2': r_value**2,
    'color': '#1f77b4'
}

# SchemeSS for each epsilon value
epsilon_values = [0.5, 1, 2]
colors = {0.5: '#ff7f0e', 1: '#2ca02c', 2: '#d62728'}

for eps in epsilon_values:
    print("\n" + "="*80)
    print(f"SCHEMESS ε={eps}")
    print("="*80)
    
    scheme_data = data[(data['Algorithm'] == 'S') & (data['epsilon'] == eps)].copy()
    
    # Take logarithms
    log_n = np.log10(scheme_data['Size'].values)
    log_t = np.log10(scheme_data['t'].values)
    
    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(log_n, log_t)
    
    # Calculate the constant c
    c = 10**intercept
    
    print(f"\nNumber of data points: {len(scheme_data)}")
    print(f"\nRegression results:")
    print(f"  Slope (b):       {slope:.4f}")
    print(f"  Intercept:       {intercept:.4f}")
    print(f"  Constant (c):    {c:.4e}")
    print(f"  R² value:        {r_value**2:.6f}  (goodness of fit, 1.0 = perfect)")
    print(f"  P-value:         {p_value:.6e}")
    print(f"  Std error:       {std_err:.6f}")
    
    print(f"\n✓ Time complexity: t ≈ {c:.2e} × n^{slope:.2f}")
    print(f"✓ Big-O notation:  O(n^{slope:.2f})")
    
    # Store for plotting
    regression_results[f'SchemeSS ε={eps}'] = {
        'slope': slope,
        'intercept': intercept,
        'c': c,
        'r2': r_value**2,
        'color': colors[eps]
    }

# Summary comparison
print("\n" + "="*80)
print("SUMMARY: TIME COMPLEXITY COMPARISON")
print("="*80)
print(f"\n{'Algorithm':<20} {'Formula':<35} {'Big-O':<15} {'R²':<10}")
print("-"*80)

# Greedy
result = regression_results['Greedy']
big_o_str = f"O(n^{result['slope']:.2f})"
print(f"{'Greedy':<20} t ≈ {result['c']:.2e} × n^{result['slope']:.2f}  {big_o_str:<15} {result['r2']:.6f}")

# SchemeSS variants
for eps in epsilon_values:
    result = regression_results[f'SchemeSS ε={eps}']
    algo_name = f'SchemeSS ε={eps}'
    big_o_str = f"O(n^{result['slope']:.2f})"
    print(f"{algo_name:<20} t ≈ {result['c']:.2e} × n^{result['slope']:.2f}  {big_o_str:<15} {result['r2']:.6f}")

print("\n" + "="*80)
print("INTERPRETATION:")
print("="*80)
print("• Slope < 1:     Sublinear growth (better than O(n))")
print("• Slope ≈ 1:     Linear growth O(n)")
print("• Slope ≈ 2:     Quadratic growth O(n²)")
print("• Slope ≈ 3:     Cubic growth O(n³)")
print("• R² close to 1: Data fits power law model very well")
print("="*80)

# Create visualization with regression lines
print("\nCreating visualization with fitted regression lines...")

fig, ax = plt.subplots(figsize=(7.5, 5))

# Define markers
markers = {
    'Greedy': 'o',
    'SchemeSS ε=0.5': 's',
    'SchemeSS ε=1': '^',
    'SchemeSS ε=2': 'D'
}

# Plot individual data points
greedy_data = data[data['Algorithm'] == 'G']
ax.scatter(greedy_data['Size'], greedy_data['t'],
          color=regression_results['Greedy']['color'],
          marker=markers['Greedy'],
          s=50,
          alpha=0.6,
          label='Greedy (data)',
          zorder=3)

for eps in epsilon_values:
    scheme_data = data[(data['Algorithm'] == 'S') & (data['epsilon'] == eps)]
    label_base = f'SchemeSS ε={eps}'
    ax.scatter(scheme_data['Size'], scheme_data['t'],
              color=regression_results[label_base]['color'],
              marker=markers[label_base],
              s=50,
              alpha=0.6,
              label=f'{label_base} (data)',
              zorder=3)

# Plot regression lines
n_range = np.logspace(0.8, 4.2, 100)  # From ~6 to ~16000

for algo_name, result in regression_results.items():
    # Calculate fitted values: t = c × n^b
    t_fitted = result['c'] * (n_range ** result['slope'])
    
    ax.plot(n_range, t_fitted,
           color=result['color'],
           linestyle='--',
           linewidth=2,
           alpha=0.8,
           label=f'{algo_name} (fit: N^{result["slope"]:.2f})',
           zorder=2)

# Set logarithmic scale for both axes
ax.set_xscale('log')
ax.set_yscale('log')

# Add labels and title
ax.set_xlabel('Instance Size (N)', fontsize=11, fontweight='bold')
ax.set_ylabel('Execution Time (seconds)', fontsize=11, fontweight='bold')
ax.set_title('Time Complexity: Data Points and Fitted Power Laws', 
             fontsize=12, fontweight='bold', pad=15)

# Add grid
ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
ax.grid(True, which='minor', alpha=0.15, linestyle=':', linewidth=0.3)

# Create legend (place outside to avoid covering data)
ax.legend(loc='center left', bbox_to_anchor=(1.02, 0.5),
         fontsize=8, framealpha=0.9)

# Adjust layout to accommodate legend
plt.tight_layout()

# Save the figure
plt.savefig('mss_time_complexity_regression.png', 
            dpi=300, 
            bbox_inches='tight',
            facecolor='white',
            edgecolor='none')

plt.savefig('mss_time_complexity_regression.pdf', 
            bbox_inches='tight',
            facecolor='white',
            edgecolor='none')

print("\nPlot saved successfully!")
print("Files:")
print("  - mss_time_complexity_regression.png")
print("  - mss_time_complexity_regression.pdf")

plt.show()

print("\n" + "="*80)
print("Analysis complete!")
print("="*80)

#%% Plot comparing approximation gap with N
# Code obtained from Claude IA
# Calculate approximation gap (distance from optimal)
data['Gap'] = 1 - data['Value / M']

# Create the plot with dimensions optimized for A4 report
fig, ax = plt.subplots(figsize=(7.5, 5))

# Define colors for each algorithm/epsilon combination
colors = {
    'Greedy': '#1f77b4',      # Blue
    'SchemeSS ε=0.5': '#ff7f0e',  # Orange
    'SchemeSS ε=1': '#2ca02c',    # Green
    'SchemeSS ε=2': '#d62728'     # Red
}

# Define markers for exact vs unknown
markers_exact = {'E': 's', 'U': 'o'}  # square for exact, circle for unknown
marker_sizes = {'E': 80, 'U': 50}     # slightly larger squares

# For perfect solutions (Gap = 0), we'll plot them at a very small value
min_nonzero_gap = data[data['Gap'] > 0]['Gap'].min()
perfect_gap_display = min_nonzero_gap / 10

# Plot Greedy algorithm
greedy_data = data[data['Algorithm'] == 'G']
for exact_type in ['E', 'U']:
    subset = greedy_data[greedy_data['Exact?'] == exact_type]
    if not subset.empty:
        # Separate perfect and non-perfect solutions
        subset_nonzero = subset[subset['Gap'] > 0]
        subset_perfect = subset[subset['Gap'] == 0]
        
        # Plot non-zero gaps
        if not subset_nonzero.empty:
            label = 'Greedy' if exact_type == 'U' else None
            ax.scatter(subset_nonzero['Size'], subset_nonzero['Gap'], 
                      color=colors['Greedy'], 
                      marker=markers_exact[exact_type],
                      s=marker_sizes[exact_type],
                      alpha=0.7,
                      label=label,
                      edgecolors='black',
                      linewidths=0.5)
        
        # Plot perfect solutions with star marker
        if not subset_perfect.empty:
            ax.scatter(subset_perfect['Size'], 
                      [perfect_gap_display] * len(subset_perfect), 
                      color=colors['Greedy'], 
                      marker='*',
                      s=200,
                      alpha=0.9,
                      edgecolors='black',
                      linewidths=0.8,
                      zorder=10)

# Plot SchemeSS for each epsilon value
epsilon_values = [0.5, 1, 2]
for eps in epsilon_values:
    scheme_data = data[(data['Algorithm'] == 'S') & (data['epsilon'] == eps)]
    label_base = f'SchemeSS ε={eps}'
    
    for exact_type in ['E', 'U']:
        subset = scheme_data[scheme_data['Exact?'] == exact_type]
        if not subset.empty:
            # Separate perfect and non-perfect solutions
            subset_nonzero = subset[subset['Gap'] > 0]
            subset_perfect = subset[subset['Gap'] == 0]
            
            # Plot non-zero gaps
            if not subset_nonzero.empty:
                label = label_base if exact_type == 'U' else None
                ax.scatter(subset_nonzero['Size'], subset_nonzero['Gap'], 
                          color=colors[label_base], 
                          marker=markers_exact[exact_type],
                          s=marker_sizes[exact_type],
                          alpha=0.7,
                          label=label,
                          edgecolors='black',
                          linewidths=0.5)
            
            # Plot perfect solutions with star marker
            if not subset_perfect.empty:
                ax.scatter(subset_perfect['Size'], 
                          [perfect_gap_display] * len(subset_perfect), 
                          color=colors[label_base], 
                          marker='*',
                          s=200,
                          alpha=0.9,
                          edgecolors='black',
                          linewidths=0.8,
                          zorder=10)

# Set logarithmic scale for both axes
ax.set_xscale('log')
ax.set_yscale('log')

# Invert y-axis so better performance (smaller gaps) is at the top
ax.invert_yaxis()

# Add labels and title
ax.set_xlabel('Instance Size (n)', fontsize=11, fontweight='bold')
ax.set_ylabel('Approximation Gap (1 - Value/M)', fontsize=11, fontweight='bold')
ax.set_title('Algorithm Performance: Approximation Gap vs Instance Size', 
             fontsize=12, fontweight='bold', pad=15)

# Add grid for better readability
ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

# Create legend
legend1 = ax.legend(loc='lower right', fontsize=9, framealpha=0.9, 
                   title='Algorithm', title_fontsize=10)

# Create a second legend for marker types
marker_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', 
           markersize=7, label='Unknown optimal', markeredgecolor='black', markeredgewidth=0.5),
    Line2D([0], [0], marker='s', color='w', markerfacecolor='gray', 
           markersize=8, label='Exact optimal', markeredgecolor='black', markeredgewidth=0.5),
    Line2D([0], [0], marker='*', color='w', markerfacecolor='gold', 
           markersize=12, label='Perfect (Gap = 0)', markeredgecolor='black', markeredgewidth=0.8)
]
legend2 = ax.legend(handles=marker_elements, loc='upper center', 
                   fontsize=9, framealpha=0.9, 
                   title='Optimality', title_fontsize=10,
                   ncol=3)
ax.add_artist(legend1)  # Add back the first legend

# Adjust layout
plt.tight_layout()

# Save the figure
plt.savefig('mss_algorithm_gap_vs_size.png', 
            dpi=300, 
            bbox_inches='tight',
            facecolor='white',
            edgecolor='none')

plt.savefig('mss_algorithm_gap_vs_size.pdf', 
            bbox_inches='tight',
            facecolor='white',
            edgecolor='none')

print("Plot saved successfully!")
print("Files:")
print("  - mss_algorithm_gap_vs_size.png")
print("  - mss_algorithm_gap_vs_size.pdf")

plt.show()

#%% Plot Time-Quality Trade-of
# Code obtained from Claude IA

# Convert epsilon to numeric and calculate Gap

data['Gap'] = 1 - data['Value / M']

# Filter out zero gaps (perfect solutions) for cleaner visualization
data_nonzero = data[data['Gap'] > 0].copy()

# Create figure
fig, ax = plt.subplots(figsize=(10, 7))

# Define colors and markers (matching previous plots)
colors = {
    'G': '#1f77b4',      # Blue for Greedy
    0.5: '#2ca02c',      # Green for ε=0.5
    1.0: '#ff7f0e',      # Orange for ε=1
    2.0: '#d62728'       # Red for ε=2
}

markers = {
    'G': 'o',
    0.5: 's',
    1.0: '^',
    2.0: 'D'
}

# Plot Greedy
greedy_data = data_nonzero[data_nonzero['Algorithm'] == 'G']
if not greedy_data.empty:
    ax.scatter(greedy_data['t'], greedy_data['Gap'],
              color=colors['G'],
              marker=markers['G'],
              s=100,
              alpha=0.7,
              label='Greedy',
              edgecolors='black',
              linewidths=0.5,
              zorder=3)

# Plot SchemeSS for each epsilon
epsilon_values = [0.5, 1, 2]
for eps in epsilon_values:
    eps_data = data_nonzero[(data_nonzero['Algorithm'] == 'S') & 
                            (data_nonzero['epsilon'] == eps)]
    if not eps_data.empty:
        ax.scatter(eps_data['t'], eps_data['Gap'],
                  color=colors[eps],
                  marker=markers[eps],
                  s=100,
                  alpha=0.7,
                  label=f'SchemeSS ε={eps}',
                  edgecolors='black',
                  linewidths=0.5,
                  zorder=3)

# Set logarithmic scale for both axes
ax.set_xscale('log')
ax.set_yscale('log')

# Invert y-axis so better performance (smaller gaps) is at the top
ax.invert_yaxis()

# Add labels and title
ax.set_xlabel('Execution Time (seconds)', fontsize=11, fontweight='bold')
ax.set_ylabel('Approximation Gap (1 - Value/M)', fontsize=11, fontweight='bold')
ax.set_title('Algorithm Performance: Time vs Quality Trade-off', 
             fontsize=12, fontweight='bold', pad=15)

# Add grid
ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
ax.grid(True, which='minor', alpha=0.15, linestyle=':', linewidth=0.3)

# Create legend
ax.legend(loc='upper left', fontsize=9, framealpha=0.9,
         title='Algorithm', title_fontsize=10)

plt.tight_layout()

# Save
plt.savefig('mss_time_vs_gap.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('mss_time_vs_gap.pdf', 
            bbox_inches='tight', facecolor='white')

print("Plot saved successfully!")
print(f"Total data points plotted: {len(data_nonzero)}")
print(f"\nBreakdown by algorithm:")
print(f"  Greedy: {len(greedy_data)}")
for eps in epsilon_values:
    eps_data = data_nonzero[(data_nonzero['Algorithm'] == 'S') & 
                            (data_nonzero['epsilon'] == eps)]
    print(f"  SchemeSS ε={eps}: {len(eps_data)}")

#%% Plot Time-Quality Trade-of but with N represented on marker sizes
# Code obtained from Claude IA


# Calculate Gap
data['Gap'] = 1 - data['Value / M']

# Filter out zero gaps (perfect solutions) for cleaner visualization
data_nonzero = data[data['Gap'] > 0].copy()

# Create figure
fig, ax = plt.subplots(figsize=(10, 7))

# Define colors and markers (matching previous plots)
colors = {
    'G': '#1f77b4',      # Blue for Greedy
    0.5: '#2ca02c',      # Green for ε=0.5
    1.0: '#ff7f0e',      # Orange for ε=1
    2.0: '#d62728'       # Red for ε=2
}

markers = {
    'G': 'o',
    0.5: 's',
    1.0: '^',
    2.0: 'D'
}

# Function to calculate marker size based on problem size
def get_marker_size(size):
    """Convert problem size to marker size using logarithmic scaling"""
    return 30 + 70 * np.log10(size)  # Base size 30, scale with log10

# Plot Greedy
greedy_data = data_nonzero[data_nonzero['Algorithm'] == 'G']
if not greedy_data.empty:
    sizes = [get_marker_size(size) for size in greedy_data['Size']]
    ax.scatter(greedy_data['t'], greedy_data['Gap'],
              color=colors['G'],
              marker=markers['G'],
              s=sizes,
              alpha=0.7,
              label='Greedy',
              edgecolors='black',
              linewidths=0.5,
              zorder=3)

# Plot SchemeSS for each epsilon
epsilon_values = [0.5, 1, 2]
for eps in epsilon_values:
    eps_data = data_nonzero[(data_nonzero['Algorithm'] == 'S') & 
                            (data_nonzero['epsilon'] == eps)]
    if not eps_data.empty:
        sizes = [get_marker_size(size) for size in eps_data['Size']]
        ax.scatter(eps_data['t'], eps_data['Gap'],
                  color=colors[eps],
                  marker=markers[eps],
                  s=sizes,
                  alpha=0.7,
                  label=f'SchemeSS ε={eps}',
                  edgecolors='black',
                  linewidths=0.5,
                  zorder=3)

# Set logarithmic scale for both axes
ax.set_xscale('log')
ax.set_yscale('log')

# Invert y-axis so better performance (smaller gaps) is at the top
ax.invert_yaxis()

# Add labels and title
ax.set_xlabel('Execution Time (seconds)', fontsize=11, fontweight='bold')
ax.set_ylabel('Approximation Gap (1 - Value/M)', fontsize=11, fontweight='bold')
ax.set_title('Algorithm Performance: Time vs Quality Trade-off', 
             fontsize=12, fontweight='bold', pad=15)

# Add grid
ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
ax.grid(True, which='minor', alpha=0.15, linestyle=':', linewidth=0.3)

# Create legend
ax.legend(loc='upper left', fontsize=9, framealpha=0.9,
         title='Algorithm', title_fontsize=10)

# Add size legend
size_legend_elements = []
size_values = [10, 100, 1000, 10000]
for size in size_values:
    size_legend_elements.append(plt.scatter([], [], s=get_marker_size(size), 
                                           c='gray', alpha=0.5, edgecolors='black', linewidths=0.5))
size_legend = ax.legend(size_legend_elements, 
                       [f'n={size:,}' for size in size_values],
                       loc='lower right', 
                       fontsize=8,
                       framealpha=0.9,
                       title='Problem Size',
                       title_fontsize=9,
                       scatterpoints=1)
ax.add_artist(size_legend)

# Re-add the algorithm legend so both appear
algo_legend = ax.legend(loc='upper left', fontsize=9, framealpha=0.9,
                        title='Algorithm', title_fontsize=10)

plt.tight_layout()

# Save
plt.savefig('mss_time_vs_gap-N.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('mss_time_vs_gap-N.pdf', 
            bbox_inches='tight', facecolor='white')

print("Plot saved successfully!")
print(f"Total data points plotted: {len(data_nonzero)}")
print(f"\nBreakdown by algorithm:")
print(f"  Greedy: {len(greedy_data)}")
for eps in epsilon_values:
    eps_data = data_nonzero[(data_nonzero['Algorithm'] == 'S') & 
                            (data_nonzero['epsilon'] == eps)]
    print(f"  SchemeSS ε={eps}: {len(eps_data)}")