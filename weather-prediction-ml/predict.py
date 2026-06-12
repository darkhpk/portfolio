"""
Weather Prediction Script
"""

import argparse
import joblib
import numpy as np
import os


def load_model(model_name='random_forest'):
    """Load a trained model"""
    model_path = f'models/{model_name}_model.pkl'
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found: {model_path}. Please train the model first.")
    return joblib.load(model_path)


def predict_weather(temperature, humidity, pressure, wind_speed, 
                   wind_direction=180, cloud_cover=50, visibility=10):
    """
    Predict weather condition based on input parameters
    
    Args:
        temperature: Temperature in Celsius
        humidity: Humidity percentage
        pressure: Atmospheric pressure in hPa
        wind_speed: Wind speed in km/h
        wind_direction: Wind direction in degrees (default: 180)
        cloud_cover: Cloud cover percentage (default: 50)
        visibility: Visibility in km (default: 10)
        
    Returns:
        str: Predicted weather condition
    """
    
    # Load the best model (Random Forest)
    model = load_model('random_forest')
    
    # Prepare input features
    features = np.array([[temperature, humidity, pressure, wind_speed, 
                         wind_direction, cloud_cover, visibility]])
    
    # Make prediction
    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    
    # Get class names
    classes = model.classes_
    
    return prediction, dict(zip(classes, probabilities))


def main():
    """Command-line interface for weather prediction"""
    
    parser = argparse.ArgumentParser(description='Predict weather conditions')
    parser.add_argument('--temperature', type=float, required=True,
                       help='Temperature in Celsius')
    parser.add_argument('--humidity', type=float, required=True,
                       help='Humidity percentage (0-100)')
    parser.add_argument('--pressure', type=float, required=True,
                       help='Atmospheric pressure in hPa')
    parser.add_argument('--wind-speed', type=float, required=True,
                       help='Wind speed in km/h')
    parser.add_argument('--wind-direction', type=float, default=180,
                       help='Wind direction in degrees (default: 180)')
    parser.add_argument('--cloud-cover', type=float, default=50,
                       help='Cloud cover percentage (default: 50)')
    parser.add_argument('--visibility', type=float, default=10,
                       help='Visibility in km (default: 10)')
    
    args = parser.parse_args()
    
    print("\n" + "=" * 60)
    print("Weather Prediction")
    print("=" * 60)
    
    print("\nInput Parameters:")
    print(f"  Temperature: {args.temperature}°C")
    print(f"  Humidity: {args.humidity}%")
    print(f"  Pressure: {args.pressure} hPa")
    print(f"  Wind Speed: {args.wind_speed} km/h")
    print(f"  Wind Direction: {args.wind_direction}°")
    print(f"  Cloud Cover: {args.cloud_cover}%")
    print(f"  Visibility: {args.visibility} km")
    
    try:
        prediction, probabilities = predict_weather(
            args.temperature, args.humidity, args.pressure, 
            args.wind_speed, args.wind_direction, 
            args.cloud_cover, args.visibility
        )
        
        print("\n" + "-" * 60)
        print(f"Predicted Weather: {prediction}")
        print("-" * 60)
        
        print("\nConfidence Levels:")
        for weather, prob in sorted(probabilities.items(), 
                                   key=lambda x: x[1], reverse=True):
            bar = '█' * int(prob * 50)
            print(f"  {weather:<10} {prob*100:>5.1f}% {bar}")
        
        print("\n" + "=" * 60)
        
    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("Please run 'python train.py' first to train the models.")


if __name__ == "__main__":
    main()
