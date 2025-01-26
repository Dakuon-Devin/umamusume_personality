"""
Prediction script for Spaceship Titanic competition.
"""
import os
import pandas as pd
from data_preprocessing import load_data, preprocess_features
from model import SpaceshipModel

def generate_predictions(
    model: SpaceshipModel,
    data_dir: str = '../data',
    output_dir: str = '../submissions'
) -> None:
    """
    Generate predictions for test data.
    
    Args:
        model: Trained model
        data_dir: Directory containing data files
        output_dir: Directory to save submission file
    """
    # Load and preprocess test data
    _, test_df = load_data(
        os.path.join(data_dir, 'train.csv'),
        os.path.join(data_dir, 'test.csv')
    )
    
    # Save passenger IDs
    passenger_ids = test_df['PassengerId']
    
    # Preprocess features
    processed_test = preprocess_features(test_df, is_training=False)
    
    # Generate predictions
    predictions = model.predict(processed_test)
    
    # Create submission DataFrame
    submission = pd.DataFrame({
        'PassengerId': passenger_ids,
        'Transported': predictions
    })
    
    # Save submission
    os.makedirs(output_dir, exist_ok=True)
    submission_path = os.path.join(output_dir, 'submission.csv')
    submission.to_csv(submission_path, index=False)
    print(f"Submission saved to {submission_path}")

if __name__ == '__main__':
    # TODO: Add argument parsing for model loading
    pass
