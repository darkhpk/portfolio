"""
Data loading and preprocessing module
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def load_and_preprocess_data(filepath):
    """
    Load and preprocess sales data
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        DataFrame: Preprocessed sales data
    """
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"File not found. Generating sample data...")
        df = generate_sample_data()
        df.to_csv(filepath, index=False)
        print(f"Sample data saved to {filepath}")
    
    # Convert date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Calculate revenue
    df['Revenue'] = df['Quantity'] * df['Price']
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Handle missing values
    df = df.dropna()
    
    # Sort by date
    df = df.sort_values('Date')
    
    return df


def generate_sample_data(num_records=1000):
    """
    Generate sample sales data for demonstration
    
    Args:
        num_records: Number of records to generate
        
    Returns:
        DataFrame: Sample sales data
    """
    np.random.seed(42)
    
    # Generate dates for the past 2 years
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)
    dates = [start_date + timedelta(days=x) for x in range(730)]
    
    products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones', 
                'Webcam', 'USB Drive', 'External HDD', 'Graphics Card', 'Printer']
    regions = ['North', 'South', 'East', 'West', 'Central']
    customers = [f'Customer_{i:04d}' for i in range(1, 201)]
    
    data = {
        'Date': np.random.choice(dates, num_records),
        'Product': np.random.choice(products, num_records),
        'Region': np.random.choice(regions, num_records),
        'Customer': np.random.choice(customers, num_records),
        'Quantity': np.random.randint(1, 10, num_records),
        'Price': np.random.uniform(10, 2000, num_records).round(2)
    }
    
    df = pd.DataFrame(data)
    return df
