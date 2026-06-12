"""
Sales Analytics Dashboard - Main Script
Analyzes sales data and generates visualizations and reports
"""

import os
from src.data_loader import load_and_preprocess_data
from src.analyzer import SalesAnalyzer
from src.visualizer import SalesVisualizer


def main():
    """Main function to run the sales analytics dashboard"""
    
    print("=" * 60)
    print("Sales Analytics Dashboard")
    print("=" * 60)
    
    # Create reports directory if it doesn't exist
    os.makedirs('reports', exist_ok=True)
    
    # Load and preprocess data
    print("\n1. Loading sales data...")
    df = load_and_preprocess_data('data/sales_data.csv')
    print(f"   Loaded {len(df)} records")
    print(f"   Date range: {df['Date'].min()} to {df['Date'].max()}")
    
    # Initialize analyzer and visualizer
    analyzer = SalesAnalyzer(df)
    visualizer = SalesVisualizer(df)
    
    # Perform analysis
    print("\n2. Analyzing sales data...")
    
    # Basic statistics
    print("\n   Sales Summary:")
    summary = analyzer.get_summary_statistics()
    for key, value in summary.items():
        print(f"   - {key}: {value}")
    
    # Top products
    print("\n   Top 5 Products by Revenue:")
    top_products = analyzer.get_top_products(5)
    for idx, row in top_products.iterrows():
        print(f"   {idx + 1}. {row['Product']}: ${row['Revenue']:,.2f}")
    
    # Regional performance
    print("\n   Regional Performance:")
    regional = analyzer.get_regional_performance()
    for idx, row in regional.iterrows():
        print(f"   - {row['Region']}: ${row['Revenue']:,.2f} ({row['Orders']} orders)")
    
    # Generate visualizations
    print("\n3. Generating visualizations...")
    
    visualizer.plot_sales_trend()
    print("   ✓ Sales trend chart saved")
    
    visualizer.plot_product_performance()
    print("   ✓ Product performance chart saved")
    
    visualizer.plot_regional_distribution()
    print("   ✓ Regional distribution chart saved")
    
    visualizer.plot_customer_segments()
    print("   ✓ Customer segmentation chart saved")
    
    visualizer.create_dashboard()
    print("   ✓ Complete dashboard saved")
    
    print("\n" + "=" * 60)
    print("Analysis complete! Check the 'reports' folder for outputs.")
    print("=" * 60)


if __name__ == "__main__":
    main()
