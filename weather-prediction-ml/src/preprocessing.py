"""
Data preprocessing module
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def generate_sample_data(n_samples=5000):
    """
    Generate sample weather data for training
    
    Args:
        n_samples: Number of samples to generate
        
    Returns:
        DataFrame: Sample weather data
    """
    np.random.seed(42)
    
    weather_conditions = ['Sunny', 'Cloudy', 'Rainy', 'Stormy', 'Snowy']
    
    data = []
    
    for _ in range(n_samples):
        # Generate random weather condition
        condition = np.random.choice(weather_conditions)
        
        # Generate features based on condition
        if condition == 'Sunny':
            temp = np.random.uniform(20, 35)
            humidity = np.random.uniform(20, 60)
            pressure = np.random.uniform(1015, 1025)
            wind_speed = np.random.uniform(0, 15)
            cloud_cover = np.random.uniform(0, 30)
            visibility = np.random.uniform(8, 10)
        elif condition == 'Cloudy':
            temp = np.random.uniform(15, 25)
            humidity = np.random.uniform(50, 75)
            pressure = np.random.uniform(1010, 1020)
            wind_speed = np.random.uniform(5, 20)
            cloud_cover = np.random.uniform(50, 90)
            visibility = np.random.uniform(5, 10)
        elif condition == 'Rainy':
            temp = np.random.uniform(10, 20)
            humidity = np.random.uniform(70, 95)
            pressure = np.random.uniform(1005, 1015)
            wind_speed = np.random.uniform(10, 30)
            cloud_cover = np.random.uniform(80, 100)
            visibility = np.random.uniform(2, 6)
        elif condition == 'Stormy':
            temp = np.random.uniform(15, 25)
            humidity = np.random.uniform(75, 100)
            pressure = np.random.uniform(990, 1010)
            wind_speed = np.random.uniform(30, 70)
            cloud_cover = np.random.uniform(90, 100)
            visibility = np.random.uniform(0.5, 3)
        else:  # Snowy
            temp = np.random.uniform(-10, 5)
            humidity = np.random.uniform(60, 90)
            pressure = np.random.uniform(1005, 1020)
            wind_speed = np.random.uniform(5, 25)
            cloud_cover = np.random.uniform(70, 100)
            visibility = np.random.uniform(1, 5)
        
        wind_direction = np.random.uniform(0, 360)
        
        data.append({
            'Temperature': temp,
            'Humidity': humidity,
            'Pressure': pressure,
            'Wind_Speed': wind_speed,
            'Wind_Direction': wind_direction,
            'Cloud_Cover': cloud_cover,
            'Visibility': visibility,
            'Weather': condition
        })
    
    return pd.DataFrame(data)


def load_and_preprocess_data(filepath):
    """
    Load and preprocess weather data
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        DataFrame: Preprocessed data
    """
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"File not found. Generating sample data...")
        df = generate_sample_data()
        df.to_csv(filepath, index=False)
        print(f"Sample data saved to {filepath}")
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Handle missing values
    df = df.dropna()
    
    return df


def split_data(df, test_size=0.2, random_state=42):
    """
    Split data into training and testing sets
    
    Args:
        df: DataFrame with features and target
        test_size: Proportion of test data
        random_state: Random seed
        
    Returns:
        tuple: X_train, X_test, y_train, y_test
    """
    X = df.drop('Weather', axis=1)
    y = df['Weather']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # Standardize features
    scaler = StandardScaler()
    X_train = pd.DataFrame(
        scaler.fit_transform(X_train),
        columns=X_train.columns,
        index=X_train.index
    )
    X_test = pd.DataFrame(
        scaler.transform(X_test),
        columns=X_test.columns,
        index=X_test.index
    )
    
    return X_train, X_test, y_train, y_test
