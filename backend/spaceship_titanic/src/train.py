"""
Training script for Spaceship Titanic competition.
"""
import os
from pathlib import Path
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report

from data_preprocessing import (
    load_data,
    preprocess_features,
    prepare_training_data
)
from model import SpaceshipModel

def train_model(data_dir: str = '../data',
                model_dir: str = '../models',
                model_params: dict = None) -> SpaceshipModel:
    """
    Train model on Spaceship Titanic data.
    
    Args:
        data_dir: Directory containing data files
        model_dir: Directory to save model files
        model_params: Parameters for the model
    
    Returns:
        Trained model
    """
    # Load and preprocess data
    train_df, _ = load_data(
        os.path.join(data_dir, 'train.csv'),
        os.path.join(data_dir, 'test.csv')
    )
    
    # Preprocess features
    processed_df = preprocess_features(train_df)
    
    # Split data
    X_train, X_val, y_train, y_val = prepare_training_data(processed_df)
    
    # Initialize and train model
    model = SpaceshipModel(model_params)
    model.fit(X_train, y_train)
    
    # Evaluate
    val_preds = model.predict(X_val)
    accuracy = accuracy_score(y_val, val_preds)
    print(f"Validation accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_val, val_preds))
    
    return model

if __name__ == '__main__':
    # TODO: Add argument parsing for model parameters
    model = train_model()
