"""
Visualization functions for sales data
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from src.analyzer import SalesAnalyzer


class SalesVisualizer:
    """Class for creating sales data visualizations"""
    
    def __init__(self, df):
        """
        Initialize visualizer with sales data
        
        Args:
            df: DataFrame containing sales data
        """
        self.df = df
        self.analyzer = SalesAnalyzer(df)
        
        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)
    
    def plot_sales_trend(self):
        """Plot sales trend over time"""
        monthly = self.analyzer.get_monthly_trends()
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        # Revenue trend
        ax1.plot(monthly.index, monthly['Revenue'], marker='o', linewidth=2, color='#2ecc71')
        ax1.fill_between(monthly.index, monthly['Revenue'], alpha=0.3, color='#2ecc71')
        ax1.set_title('Monthly Revenue Trend', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Revenue ($)', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        # Orders trend
        ax2.bar(monthly.index, monthly['Orders'], color='#3498db', alpha=0.7)
        ax2.set_title('Monthly Order Count', fontsize=16, fontweight='bold')
        ax2.set_xlabel('Month', fontsize=12)
        ax2.set_ylabel('Number of Orders', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('reports/sales_trend.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_product_performance(self):
        """Plot top products performance"""
        top_products = self.analyzer.get_top_products(10)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        bars = ax.barh(top_products['Product'], top_products['Revenue'], color='#e74c3c')
        
        # Add value labels
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2, 
                   f'${width:,.0f}', 
                   ha='left', va='center', fontsize=10, fontweight='bold')
        
        ax.set_title('Top 10 Products by Revenue', fontsize=16, fontweight='bold')
        ax.set_xlabel('Revenue ($)', fontsize=12)
        ax.set_ylabel('Product', fontsize=12)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        plt.tight_layout()
        plt.savefig('reports/product_performance.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_regional_distribution(self):
        """Plot regional sales distribution"""
        regional = self.analyzer.get_regional_performance()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Pie chart for revenue distribution
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
        wedges, texts, autotexts = ax1.pie(regional['Revenue'], 
                                            labels=regional['Region'],
                                            autopct='%1.1f%%',
                                            colors=colors,
                                            startangle=90)
        ax1.set_title('Revenue Distribution by Region', fontsize=14, fontweight='bold')
        
        # Bar chart for order count
        ax2.bar(regional['Region'], regional['Orders'], color=colors, alpha=0.7)
        ax2.set_title('Order Count by Region', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Region', fontsize=12)
        ax2.set_ylabel('Number of Orders', fontsize=12)
        ax2.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('reports/regional_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_customer_segments(self):
        """Plot customer segmentation"""
        segments = self.analyzer.get_customer_segments()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        colors = ['#e74c3c', '#f39c12', '#3498db', '#95a5a6']
        wedges, texts, autotexts = ax.pie(segments.values, 
                                           labels=segments.index,
                                           autopct='%1.1f%%',
                                           colors=colors,
                                           startangle=45)
        
        # Enhance text
        for text in texts:
            text.set_fontsize(12)
            text.set_fontweight('bold')
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')
        
        ax.set_title('Customer Segmentation by Purchase Value', 
                    fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig('reports/customer_segments.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_dashboard(self):
        """Create a comprehensive dashboard"""
        fig = plt.figure(figsize=(20, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # Title
        fig.suptitle('Sales Analytics Dashboard', fontsize=24, fontweight='bold', y=0.98)
        
        # 1. Monthly revenue trend
        ax1 = fig.add_subplot(gs[0, :])
        monthly = self.analyzer.get_monthly_trends()
        ax1.plot(monthly.index, monthly['Revenue'], marker='o', linewidth=2, color='#2ecc71')
        ax1.fill_between(monthly.index, monthly['Revenue'], alpha=0.3, color='#2ecc71')
        ax1.set_title('Monthly Revenue Trend', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Revenue ($)', fontsize=10)
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        ax1.grid(True, alpha=0.3)
        
        # 2. Top products
        ax2 = fig.add_subplot(gs[1, :2])
        top_products = self.analyzer.get_top_products(5)
        ax2.barh(top_products['Product'], top_products['Revenue'], color='#e74c3c', alpha=0.7)
        ax2.set_title('Top 5 Products', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Revenue ($)', fontsize=10)
        ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        # 3. Regional distribution
        ax3 = fig.add_subplot(gs[1, 2])
        regional = self.analyzer.get_regional_performance()
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
        ax3.pie(regional['Revenue'], labels=regional['Region'], 
               autopct='%1.1f%%', colors=colors, startangle=90)
        ax3.set_title('Regional Distribution', fontsize=14, fontweight='bold')
        
        # 4. Customer segments
        ax4 = fig.add_subplot(gs[2, 0])
        segments = self.analyzer.get_customer_segments()
        ax4.bar(segments.index, segments.values, color=['#e74c3c', '#f39c12', '#3498db', '#95a5a6'])
        ax4.set_title('Customer Segments', fontsize=14, fontweight='bold')
        ax4.set_ylabel('Count', fontsize=10)
        ax4.tick_params(axis='x', rotation=45)
        
        # 5. Summary statistics box
        ax5 = fig.add_subplot(gs[2, 1:])
        ax5.axis('off')
        summary = self.analyzer.get_summary_statistics()
        summary_text = '\n'.join([f'{k}: {v}' for k, v in summary.items()])
        ax5.text(0.1, 0.5, summary_text, fontsize=14, verticalalignment='center',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        ax5.set_title('Summary Statistics', fontsize=14, fontweight='bold')
        
        plt.savefig('reports/dashboard.png', dpi=300, bbox_inches='tight')
        plt.close()
