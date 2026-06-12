"""
Weather Prediction Model Training Script
"""

import os
import joblib
from src.preprocessing import load_and_preprocess_data, split_data
from src.model_builder import ModelBuilder
from src.evaluator import ModelEvaluator


def main():
    """Train weather prediction models"""
    
    print("=" * 60)
    print("Weather Prediction Model Training")
    print("=" * 60)
    
    # Create necessary directories
    os.makedirs('models', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    os.makedirs('results', exist_ok=True)
    
    # Load and preprocess data
    print("\n1. Loading and preprocessing data...")
    df = load_and_preprocess_data('data/weather_data.csv')
    print(f"   Dataset shape: {df.shape}")
    print(f"   Features: {list(df.columns[:-1])}")
    
    # Split data
    X_train, X_test, y_train, y_test = split_data(df)
    print(f"\n   Training samples: {len(X_train)}")
    print(f"   Testing samples: {len(X_test)}")
    
    # Initialize model builder
    builder = ModelBuilder()
    
    # Train models
    print("\n2. Training models...")
    models = {}
    
    model_names = ['random_forest', 'logistic_regression', 'svm', 'gradient_boosting']
    
    for model_name in model_names:
        print(f"\n   Training {model_name.replace('_', ' ').title()}...")
        model = builder.build_model(model_name)
        model.fit(X_train, y_train)
        models[model_name] = model
        
        # Save model
        joblib.dump(model, f'models/{model_name}_model.pkl')
        print(f"   ✓ Model saved to models/{model_name}_model.pkl")
    
    # Evaluate models
    print("\n3. Evaluating models...")
    evaluator = ModelEvaluator(models, X_test, y_test)
    
    results = evaluator.evaluate_all()
    
    print("\n   Model Performance:")
    print("   " + "-" * 56)
    print(f"   {'Model':<25} {'Accuracy':<15} {'F1-Score':<15}")
    print("   " + "-" * 56)
    
    for model_name, metrics in results.items():
        print(f"   {model_name.replace('_', ' ').title():<25} "
              f"{metrics['accuracy']:<15.4f} {metrics['f1_score']:<15.4f}")
    
    # Find best model
    best_model_name = max(results, key=lambda x: results[x]['accuracy'])
    best_accuracy = results[best_model_name]['accuracy']
    
    print("\n   " + "=" * 56)
    print(f"   Best Model: {best_model_name.replace('_', ' ').title()}")
    print(f"   Accuracy: {best_accuracy:.4f}")
    print("   " + "=" * 56)
    
    # Generate visualizations
    print("\n4. Generating visualizations...")
    evaluator.plot_confusion_matrices()
    print("   ✓ Confusion matrices saved")
    
    evaluator.plot_model_comparison()
    print("   ✓ Model comparison chart saved")
    
    evaluator.plot_feature_importance(models['random_forest'], 
                                     X_train.columns)
    print("   ✓ Feature importance chart saved")
    
    print("\n" + "=" * 60)
    print("Training complete! Models saved to 'models' folder.")
    print("=" * 60)


if __name__ == "__main__":
    main()
