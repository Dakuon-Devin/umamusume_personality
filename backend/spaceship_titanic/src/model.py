"""
Model definition for Spaceship Titanic competition.
"""
from typing import Dict, Any
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.ensemble import RandomForestClassifier

class SpaceshipModel:
    """
    Model wrapper for Spaceship Titanic competition.
    """
    
    def __init__(self, model_params: Dict[str, Any] = None):
        """
        Initialize model with given parameters.
        
        Args:
            model_params: Dictionary of model parameters
        """
        self.model_params = model_params or {
            'n_estimators': 100,
            'max_depth': None,
            'random_state': 42
        }
        self.model = RandomForestClassifier(**self.model_params)
    
    def fit(self, X, y):
        """
        Train the model.
        
        Args:
            X: Feature matrix
            y: Target vector
        """
        self.model.fit(X, y)
        return self
    
    def predict(self, X) -> np.ndarray:
        """
        Make predictions on new data.
        
        Args:
            X: Feature matrix
        
        Returns:
            Array of predictions
        """
        return self.model.predict(X)
    
    def predict_proba(self, X) -> np.ndarray:
        """
        Get probability predictions.
        
        Args:
            X: Feature matrix
        
        Returns:
            Array of prediction probabilities
        """
        return self.model.predict_proba(X)
    
    def get_feature_importance(self) -> Dict[str, float]:
        """
        Get feature importance scores.
        
        Returns:
            Dictionary mapping feature names to importance scores
        """
        if not hasattr(self.model, 'feature_importances_'):
            raise ValueError("Model doesn't have feature importances available")
            
        return dict(zip(self.feature_names_, self.model.feature_importances_))
