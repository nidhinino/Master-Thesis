import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_extraction_performance(performance_csv='./performance_metrics/table_extraction_performance.csv'):
    """
    Comprehensive analysis of PDF extraction performance metrics
    
    Args:
        performance_csv (str): Path to performance metrics CSV file
    
    Returns:
        dict: Summary statistics and visualization details
    """
    # Read performance data
    df = pd.read_csv(performance_csv)
    
    # Basic summary statistics
    summary_stats = df.groupby('Extraction Method').agg({
        'tables_extracted': ['mean', 'min', 'max', 'std'],
        'extraction_time': ['mean', 'min', 'max', 'std'],
        'memory_usage': ['mean', 'min', 'max', 'std'],
        'cpu_usage': ['mean', 'min', 'max', 'std']
    }).round(4)
    
    # Create visualization directory
    import os
    os.makedirs('performance_metrics', exist_ok=True)
    
    # 1. Boxplot for Extraction Time
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Extraction Method', y='extraction_time', data=df)
    plt.title('Extraction Time Comparison')
    plt.ylabel('Time (seconds)')
    plt.tight_layout()
    plt.savefig('performance_metrics/extraction_time_boxplot.png')
    plt.close()
    
    # 2. Boxplot for Memory Usage
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Extraction Method', y='memory_usage', data=df)
    plt.title('Memory Usage Comparison')
    plt.ylabel('Memory (MB)')
    plt.tight_layout()
    plt.savefig('performance_metrics/memory_usage_boxplot.png')
    plt.close()
    
    # 3. Scatter Plot: Extraction Time vs Tables Extracted
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='tables_extracted', y='extraction_time', 
                    hue='Extraction Method', data=df)
    plt.title('Extraction Time vs Tables Extracted')
    plt.xlabel('Tables Extracted')
    plt.ylabel('Extraction Time (seconds)')
    plt.tight_layout()
    plt.savefig('performance_metrics/time_vs_length_scatter.png')
    plt.close()
    
    
    # 4. Bar Graph: Average Tables Extracted by Method
    plt.figure(figsize=(10, 6))
    avg_tables_extracted = df.groupby('Extraction Method')['tables_extracted'].mean().reset_index()
    sns.barplot(x='Extraction Method', y='tables_extracted', data=avg_tables_extracted)
    plt.title('Average Tables Extracted by Method')
    plt.ylabel('Average Tables Extracted')
    plt.tight_layout()
    plt.savefig('performance_metrics/avg_tables_extracted_bar.png')
    plt.close()
    
    # 5. Heatmap: Compare Performance Metrics Across All Methods and PDFs
    heatmap_data = df.pivot_table(
        index='Filename',
        columns='Extraction Method',
        values=['tables_extracted', 'extraction_time', 'memory_usage', 'cpu_usage']
    )
    plt.figure(figsize=(12, 10))
    sns.heatmap(heatmap_data, annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.5)
    plt.title('Performance Metrics Heatmap by PDF and Method')
    plt.tight_layout()
    heatmap_path = 'performance_metrics/comparison_heatmap.png'
    plt.savefig(heatmap_path)
    plt.close()
    
    # 6. Bar Graph: Compare Each Method Against Every PDF
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Filename', y='tables_extracted', hue='Extraction Method', data=df)
    plt.title('Comparison of Tables Extracted by Method for Each PDF')
    plt.ylabel('Tables Extracted')
    plt.xlabel('PDF Files')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Extraction Method')
    plt.tight_layout()
    bar_graph_path = 'performance_metrics/comparison_bar_graph.png'
    plt.savefig(bar_graph_path)
    plt.close()

    # 7. Boxplot for CPU Usage
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Extraction Method', y='cpu_usage', data=df)
    plt.title('CPU Usage Comparison')
    plt.ylabel('CPU Usage (%)')
    plt.tight_layout()
    plt.savefig('performance_metrics/cpu_usage_boxplot.png')
    plt.close()

    # Save summary to text file
    with open('performance_metrics/performance_summary.txt', 'w') as f:
        f.write("PDF Extraction Performance Summary\n")
        f.write("==================================\n\n")
        f.write(str(summary_stats))
    
    return {
        'summary_statistics': summary_stats,
        'visualizations': [
            'performance_metrics/extraction_time_boxplot.png',
            'performance_metrics/memory_usage_boxplot.png',
            'performance_metrics/cpu_usage_boxplot.png',
            'performance_metrics/time_vs_length_scatter.png',
            'performance_metrics/avg_tables_extracted_bar.png',
            'performance_metrics/comparison_bar_graph.png',
            'performance_metrics/comparison_heatmap.png'
        ],
        'summary_file': 'performance_metrics/performance_summary.txt'
    }

# Run the analysis
performance_analysis = analyze_extraction_performance()

# Print summary statistics
print(performance_analysis['summary_statistics'])
print("\nVisualizations and summary have been saved in the 'performance_metrics' directory.")
