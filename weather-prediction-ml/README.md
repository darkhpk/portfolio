# Weather Prediction ML Model

A machine learning project that predicts weather conditions using historical weather data. Built with scikit-learn, featuring multiple ML models and comprehensive evaluation metrics.

## Features

- **Multiple ML Models**: 
  - Random Forest Classifier
  - Logistic Regression
  - Support Vector Machine
  - Gradient Boosting
- **Feature Engineering**: Advanced preprocessing and feature extraction
- **Model Evaluation**: Comprehensive metrics including accuracy, precision, recall, F1-score
- **Cross-validation**: K-fold cross-validation for robust model evaluation
- **Visualization**: Feature importance plots and confusion matrices
- **Model Persistence**: Save and load trained models

## Technologies Used

- Python 3.8+
- scikit-learn - Machine learning algorithms
- pandas - Data manipulation
- numpy - Numerical computing
- matplotlib & seaborn - Visualization
- joblib - Model serialization

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Train the model:
```bash
python train.py
```

### Make predictions:
```bash
python predict.py --temperature 25 --humidity 65 --pressure 1013 --wind-speed 15
```

### Evaluate models:
```bash
python evaluate.py
```

## Dataset Features

The model uses the following features for prediction:
- Temperature (°C)
- Humidity (%)
- Pressure (hPa)
- Wind Speed (km/h)
- Wind Direction (degrees)
- Cloud Cover (%)
- Visibility (km)

## Target Classes

- Sunny
- Cloudy
- Rainy
- Stormy
- Snowy

## Model Performance

Best performing model: Random Forest Classifier
- Accuracy: ~85%
- Cross-validation score: 83%
- Training time: <2 seconds

## Project Structure

- `train.py` - Model training script
- `predict.py` - Prediction interface
- `evaluate.py` - Model evaluation script
- `models/` - Saved trained models
- `data/` - Dataset storage
- `src/` - Source modules
  - `preprocessing.py` - Data preprocessing
  - `model_builder.py` - Model definitions
  - `evaluator.py` - Evaluation functions

## Future Enhancements

- Deep learning models (LSTM, CNN)
- Real-time weather data integration
- Web API for predictions
- Time series forecasting
- Ensemble methods
