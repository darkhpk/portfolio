"""
Model evaluation module
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                            f1_score, confusion_matrix, classification_report)


class ModelEvaluator:
    """Class for evaluating ML models"""
    
    def __init__(self, models, X_test, y_test):
        """
        Initialize evaluator
        
        Args:
            models: Dictionary of trained models
            X_test: Test features
            y_test: Test labels
        """
        self.models = models
        self.X_test = X_test
        self.y_test = y_test
    
    def evaluate_model(self, model_name, model):
        """
        Evaluate a single model
        
        Args:
            model_name: Name of the model
            model: Trained model object
            
        Returns:
            dict: Evaluation metrics
        """
        y_pred = model.predict(self.X_test)
        
        metrics = {
            'accuracy': accuracy_score(self.y_test, y_pred),
            'precision': precision_score(self.y_test, y_pred, average='weighted'),
            'recall': recall_score(self.y_test, y_pred, average='weighted'),
            'f1_score': f1_score(self.y_test, y_pred, average='weighted'),
            'confusion_matrix': confusion_matrix(self.y_test, y_pred),
            'predictions': y_pred
        }
        
        return metrics
    
    def evaluate_all(self):
        """
        Evaluate all models
        
        Returns:
            dict: Results for all models
        """
        results = {}
        
        for model_name, model in self.models.items():
            results[model_name] = self.evaluate_model(model_name, model)
        
        return results
    
    def plot_confusion_matrices(self):
        """Plot confusion matrices for all models"""
        results = self.evaluate_all()
        n_models = len(results)
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 14))
        axes = axes.ravel()
        
        for idx, (model_name, metrics) in enumerate(results.items()):
            cm = metrics['confusion_matrix']
            
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                       ax=axes[idx], cbar_kws={'shrink': 0.8})
            
            axes[idx].set_title(f'{model_name.replace("_", " ").title()}\n'
                              f'Accuracy: {metrics["accuracy"]:.3f}',
                              fontsize=12, fontweight='bold')
            axes[idx].set_ylabel('True Label', fontsize=10)
            axes[idx].set_xlabel('Predicted Label', fontsize=10)
            
            # Set tick labels
            labels = sorted(self.y_test.unique())
            axes[idx].set_xticklabels(labels, rotation=45)
            axes[idx].set_yticklabels(labels, rotation=0)
        
        plt.tight_layout()
        plt.savefig('results/confusion_matrices.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_model_comparison(self):
        """Plot comparison of all models"""
        results = self.evaluate_all()
        
        model_names = [name.replace('_', ' ').title() for name in results.keys()]
        accuracies = [metrics['accuracy'] for metrics in results.values()]
        f1_scores = [metrics['f1_score'] for metrics in results.values()]
        
        x = np.arange(len(model_names))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        bars1 = ax.bar(x - width/2, accuracies, width, label='Accuracy', color='#3498db', alpha=0.8)
        bars2 = ax.bar(x + width/2, f1_scores, width, label='F1-Score', color='#e74c3c', alpha=0.8)
        
        ax.set_xlabel('Model', fontsize=12, fontweight='bold')
        ax.set_ylabel('Score', fontsize=12, fontweight='bold')
        ax.set_title('Model Performance Comparison', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(model_names, rotation=15, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_ylim([0, 1.1])
        
        # Add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.3f}',
                       ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        plt.savefig('results/model_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_feature_importance(self, model, feature_names):
        """
        Plot feature importance for tree-based models
        
        Args:
            model: Trained model with feature_importances_ attribute
            feature_names: List of feature names
        """
        if not hasattr(model, 'feature_importances_'):
            print("Model does not support feature importance")
            return
        
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        bars = ax.barh(range(len(importances)), importances[indices], color='#2ecc71', alpha=0.7)
        ax.set_yticks(range(len(importances)))
        ax.set_yticklabels([feature_names[i] for i in indices])
        ax.set_xlabel('Importance', fontsize=12, fontweight='bold')
        ax.set_title('Feature Importance', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add value labels
        for idx, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2,
                   f'{width:.3f}',
                   ha='left', va='center', fontsize=9)
        
        plt.tight_layout()
        plt.savefig('results/feature_importance.png', dpi=300, bbox_inches='tight')
        plt.close()
