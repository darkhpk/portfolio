"""
Machine learning model builder
"""

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC


class ModelBuilder:
    """Class for building ML models"""
    
    def __init__(self):
        """Initialize model builder"""
        self.models = {
            'random_forest': RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            ),
            'logistic_regression': LogisticRegression(
                max_iter=1000,
                random_state=42,
                n_jobs=-1
            ),
            'svm': SVC(
                kernel='rbf',
                probability=True,
                random_state=42
            ),
            'gradient_boosting': GradientBoostingClassifier(
                n_estimators=100,
                max_depth=5,
                random_state=42
            )
        }
    
    def build_model(self, model_name):
        """
        Build a specific model
        
        Args:
            model_name: Name of the model to build
            
        Returns:
            model: Scikit-learn model object
        """
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found. "
                           f"Available models: {list(self.models.keys())}")
        
        return self.models[model_name]
    
    def get_all_models(self):
        """Get all available models"""
        return self.models
