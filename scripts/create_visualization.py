"""
Book Ban Search Trends Visualization
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle
import os

# Set style for professional-looking plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Create output directory
os.makedirs('visualizations', exist_ok=True)

# Load cleaned data
df = pd.read_csv('trends_cleaned.csv')

print("=" * 80)
print("BOOK BAN VISUALIZATION SUITE")
print("=" * 80)
print(f"\nLoaded {len(df)} books from cleaned dataset\n")


# VISUALIZATION 1: Top 20 Books by Percent Change (Bar Chart)

def create_top20_spikes():
    """
    Creates a horizontal bar chart showing the top 20 books by percent change.
    Color-coded to distinguish positive vs. negative changes.
    """
    print("Creating Visualization 1: Top 20 Books by Percent Change...")
    
    # Filter out infinite values and get top 20
    df_finite = df[np.isfinite(df['percent_change'])].copy()
    top20 = df_finite.nlargest(20, 'percent_change')
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Create colors based on positive/negative change
    colors = ['#2ecc71' if x > 0 else '#e74c3c' for x in top20['percent_change']]
    
    # Create horizontal bar chart
    y_pos = np.arange(len(top20))
    bars = ax.barh(y_pos, top20['percent_change'], color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)
    
    # Customize
    ax.set_yticks(y_pos)
    ax.set_yticklabels(top20['book_title'], fontsize=9)
    ax.set_xlabel('Percent Change in Search Interest (%)', fontsize=12, fontweight='bold')
    ax.set_title('Top 20 Books by Search Interest Change After Being Banned', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Add value labels on bars
    for i, (idx, row) in enumerate(top20.iterrows()):
        value = row['percent_change']
        ax.text(value + 20, i, f'+{value:.1f}%', 
                va='center', fontsize=8, fontweight='bold')
    
    # Add grid
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#2ecc71', alpha=0.8, label='Increased Interest'),
        Patch(facecolor='#e74c3c', alpha=0.8, label='Decreased Interest')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('visualizations/top20_spikes.png', dpi=300, bbox_inches='tight')
    print("  ✓ Saved to visualizations/top20_spikes.png")
    plt.close()



# VISUALIZATION 2: Distribution of Engagement Changes (Histogram)


def create_distribution_histogram():
    """
    Creates a histogram showing the distribution of percent changes.
    Includes vertical line at 0% and labels for increase/decrease percentages.
    """
    print("\nCreating Visualization 2: Distribution of Engagement Changes...")
    
    # Filter to finite values for histogram
    df_finite = df[np.isfinite(df['percent_change'])].copy()
    
    # Calculate statistics
    increases = (df_finite['percent_change'] > 0).sum()
    decreases = (df_finite['percent_change'] < 0).sum()
    no_change = (df_finite['percent_change'] == 0).sum()
    total = len(df_finite)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Create histogram
    n, bins, patches = ax.hist(df_finite['percent_change'], bins=50, 
                                edgecolor='black', linewidth=0.5, alpha=0.7)
    
    # Color bars based on positive/negative
    for i, patch in enumerate(patches):
        if bins[i] < 0:
            patch.set_facecolor('#e74c3c')  # Red for decreases
        elif bins[i] > 0:
            patch.set_facecolor('#2ecc71')  # Green for increases
        else:
            patch.set_facecolor('#95a5a6')  # Gray for no change
    
    # Add vertical line at 0%
    ax.axvline(x=0, color='black', linestyle='--', linewidth=2, label='No Change (0%)')
    
    # Customize
    ax.set_xlabel('Percent Change in Search Interest (%)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Books', fontsize=12, fontweight='bold')
    ax.set_title('Distribution of Search Interest Changes After Book Bans', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Add statistics text box
    stats_text = f"""
    Total Books: {total}
    
    Increased: {increases} ({increases/total*100:.1f}%)
    Decreased: {decreases} ({decreases/total*100:.1f}%)
    No Change: {no_change} ({no_change/total*100:.1f}%)
    
    Mean: {df_finite['percent_change'].mean():.1f}%
    Median: {df_finite['percent_change'].median():.1f}%
    """
    
    ax.text(0.98, 0.97, stats_text.strip(), transform=ax.transAxes,
            fontsize=10, verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.legend(fontsize=11)
    
    plt.tight_layout()
    plt.savefig('visualizations/distribution_histogram.png', dpi=300, bbox_inches='tight')
    print("  ✓ Saved to visualizations/distribution_histogram.png")
    plt.close()



# VISUALIZATION 3: Time Series for Top 5 Books (Line Plots)


def create_timeseries_top5():
    """
    Creates time series plots for the top 5 books by percent change.
    Note: This creates a conceptual visualization since we don't have 
    actual time series data - we'll show before/after comparison.
    """
    print("\nCreating Visualization 3: Top 5 Books Comparison...")
    
    # Get top 5 books (finite changes only)
    df_finite = df[np.isfinite(df['percent_change'])].copy()
    top5 = df_finite.nlargest(5, 'percent_change')
    
    # Create subplots
    fig, axes = plt.subplots(5, 1, figsize=(14, 12))
    fig.suptitle('Top 5 Books: Search Interest Before vs. After Ban', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    for idx, (i, row) in enumerate(top5.iterrows()):
        ax = axes[idx]
        
        # Create before/after comparison
        periods = ['Before\nBan', 'After\nBan']
        avg_values = [row['avg_search_before'], row['avg_search_after']]
        max_values = [row['max_search_before'], row['max_search_after']]
        min_values = [row['min_search_before'], row['min_search_after']]
        
        x = [0, 1]
        
        # Plot average line
        ax.plot(x, avg_values, marker='o', linewidth=3, markersize=10, 
                label='Average', color='#3498db')
        
        # Plot max/min range as shaded area
        ax.fill_between(x, min_values, max_values, alpha=0.2, color='#3498db',
                        label='Min-Max Range')
        
        # Add value annotations
        for xi, avg, mx in zip(x, avg_values, max_values):
            ax.text(xi, avg + 2, f'{avg:.1f}', ha='center', fontsize=9, fontweight='bold')
            ax.text(xi, mx + 2, f'max: {mx:.0f}', ha='center', fontsize=7, style='italic')
        
        # Add vertical "ban date" line
        ax.axvline(x=0.5, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Ban Date')
        
        # Customize
        ax.set_xticks(x)
        ax.set_xticklabels(periods, fontsize=11)
        ax.set_ylabel('Search Interest\n(0-100 scale)', fontsize=9)
        ax.set_title(f'{idx+1}. {row["book_title"]} (+{row["percent_change"]:.1f}%)', 
                     fontsize=11, fontweight='bold', loc='left')
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.set_ylim(bottom=0)
        
        if idx == 0:
            ax.legend(loc='upper left', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('visualizations/top5_timeseries.png', dpi=300, bbox_inches='tight')
    print("  ✓ Saved to visualizations/top5_timeseries.png")
    plt.close()



# VISUALIZATION 4: Before vs. After Scatter Plot


def create_before_after_scatter():
    """
    Creates a scatter plot comparing search interest before and after bans.
    Diagonal line represents "no change" - points above = increased interest.
    """
    print("\nCreating Visualization 4: Before vs. After Scatter Plot...")
    
    # Filter to books with non-zero values
    df_scatter = df[
        (df['avg_search_before'] > 0) & 
        (df['avg_search_after'] > 0)
    ].copy()
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Determine point colors based on change
    colors = []
    for _, row in df_scatter.iterrows():
        if row['avg_search_after'] > row['avg_search_before']:
            colors.append('#2ecc71')  # Green for increase
        elif row['avg_search_after'] < row['avg_search_before']:
            colors.append('#e74c3c')  # Red for decrease
        else:
            colors.append('#95a5a6')  # Gray for no change
    
    # Create scatter plot
    scatter = ax.scatter(df_scatter['avg_search_before'], 
                        df_scatter['avg_search_after'],
                        c=colors, s=100, alpha=0.6, edgecolors='black', linewidth=0.5)
    
    # Add diagonal "no change" line
    max_val = max(df_scatter['avg_search_before'].max(), df_scatter['avg_search_after'].max())
    ax.plot([0, max_val], [0, max_val], 'k--', linewidth=2, alpha=0.5, label='No Change Line')
    
    # Add shaded regions
    ax.fill_between([0, max_val], [0, max_val], max_val, alpha=0.1, color='green', 
                     label='Increased Interest')
    ax.fill_between([0, max_val], 0, [0, max_val], alpha=0.1, color='red',
                     label='Decreased Interest')
    
    # Annotate some notable books
    # Top 5 increases
    df_scatter['absolute_diff'] = df_scatter['avg_search_after'] - df_scatter['avg_search_before']
    top_increases = df_scatter.nlargest(5, 'absolute_diff')
    
    for _, row in top_increases.iterrows():
        ax.annotate(row['book_title'], 
                   xy=(row['avg_search_before'], row['avg_search_after']),
                   xytext=(10, 10), textcoords='offset points',
                   fontsize=8, alpha=0.7,
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.3),
                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', alpha=0.5))
    
    # Customize
    ax.set_xlabel('Average Search Interest Before Ban (0-100 scale)', 
                  fontsize=12, fontweight='bold')
    ax.set_ylabel('Average Search Interest After Ban (0-100 scale)', 
                  fontsize=12, fontweight='bold')
    ax.set_title('Search Interest: Before vs. After Book Bans\n(Points above diagonal = increased interest)', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Add statistics
    above_line = (df_scatter['avg_search_after'] > df_scatter['avg_search_before']).sum()
    below_line = (df_scatter['avg_search_after'] < df_scatter['avg_search_before']).sum()
    on_line = (df_scatter['avg_search_after'] == df_scatter['avg_search_before']).sum()
    
    stats_text = f"""
    Total Books: {len(df_scatter)}
    
    Above Line (Increased): {above_line} ({above_line/len(df_scatter)*100:.1f}%)
    Below Line (Decreased): {below_line} ({below_line/len(df_scatter)*100:.1f}%)
    On Line (No Change): {on_line} ({on_line/len(df_scatter)*100:.1f}%)
    """
    
    ax.text(0.02, 0.98, stats_text.strip(), transform=ax.transAxes,
            fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='lower right', fontsize=10)
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    
    plt.tight_layout()
    plt.savefig('visualizations/before_after_scatter.png', dpi=300, bbox_inches='tight')
    print("  ✓ Saved to visualizations/before_after_scatter.png")
    plt.close()


if __name__ == "__main__":
    print("\nGenerating all visualizations...\n")
    
    # Create all visualizations
    create_top20_spikes()
    create_distribution_histogram()
    create_timeseries_top5()
    create_before_after_scatter()
    
    print("\n" + "=" * 80)
    print("ALL VISUALIZATIONS COMPLETE!")
    print("=" * 80)
    print("\nGenerated files:")
    print("  1. visualizations/top20_spikes.png")
    print("  2. visualizations/distribution_histogram.png")
    print("  3. visualizations/top5_timeseries.png")
    print("  4. visualizations/before_after_scatter.png")
    print("\n" + "=" * 80)
    