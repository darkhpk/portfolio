"""
Sales analysis functions
"""

import pandas as pd
import numpy as np


class SalesAnalyzer:
    """Class for performing sales data analysis"""
    
    def __init__(self, df):
        """
        Initialize analyzer with sales data
        
        Args:
            df: DataFrame containing sales data
        """
        self.df = df
    
    def get_summary_statistics(self):
        """Get summary statistics of sales data"""
        summary = {
            'Total Revenue': f"${self.df['Revenue'].sum():,.2f}",
            'Total Orders': len(self.df),
            'Average Order Value': f"${self.df['Revenue'].mean():,.2f}",
            'Unique Products': self.df['Product'].nunique(),
            'Unique Customers': self.df['Customer'].nunique(),
        }
        return summary
    
    def get_top_products(self, n=10):
        """
        Get top N products by revenue
        
        Args:
            n: Number of top products to return
            
        Returns:
            DataFrame: Top products with revenue
        """
        top_products = (self.df.groupby('Product')['Revenue']
                       .sum()
                       .sort_values(ascending=False)
                       .head(n)
                       .reset_index())
        return top_products
    
    def get_regional_performance(self):
        """Get sales performance by region"""
        regional = (self.df.groupby('Region')
                   .agg({
                       'Revenue': 'sum',
                       'Date': 'count'
                   })
                   .rename(columns={'Date': 'Orders'})
                   .sort_values('Revenue', ascending=False)
                   .reset_index())
        return regional
    
    def get_monthly_trends(self):
        """Get monthly sales trends"""
        monthly = (self.df.groupby(self.df['Date'].dt.to_period('M'))
                  .agg({
                      'Revenue': 'sum',
                      'Date': 'count'
                  })
                  .rename(columns={'Date': 'Orders'}))
        monthly.index = monthly.index.to_timestamp()
        return monthly
    
    def get_customer_segments(self):
        """Segment customers based on purchase value"""
        customer_value = (self.df.groupby('Customer')['Revenue']
                         .sum()
                         .reset_index())
        
        # Define segments based on quartiles
        q75 = customer_value['Revenue'].quantile(0.75)
        q50 = customer_value['Revenue'].quantile(0.50)
        q25 = customer_value['Revenue'].quantile(0.25)
        
        def categorize(revenue):
            if revenue >= q75:
                return 'Premium'
            elif revenue >= q50:
                return 'High Value'
            elif revenue >= q25:
                return 'Medium Value'
            else:
                return 'Low Value'
        
        customer_value['Segment'] = customer_value['Revenue'].apply(categorize)
        segment_counts = customer_value['Segment'].value_counts()
        return segment_counts
    
    def get_product_correlation(self):
        """Analyze product purchase correlations"""
        # Create a matrix of customers vs products
        product_matrix = self.df.pivot_table(
            index='Customer',
            columns='Product',
            values='Quantity',
            aggfunc='sum',
            fill_value=0
        )
        
        # Calculate correlation
        correlation = product_matrix.corr()
        return correlation
