"""
Data preprocessing module for Spaceship Titanic competition.
"""
from typing import Tuple
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_data(train_path: str, test_path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load training and test data from CSV files.
    
    Args:
        train_path: Path to training data CSV
        test_path: Path to test data CSV
    
    Returns:
        Tuple of (training DataFrame, test DataFrame)
    """
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    return train_df, test_df

def preprocess_features(df: pd.DataFrame, is_training: bool = True) -> pd.DataFrame:
    """
    Preprocess features including handling missing values, encoding categorical variables,
    and scaling numerical features.
    
    Args:
        df: Input DataFrame
        is_training: Whether this is training data (affects how we handle certain operations)
    
    Returns:
        Preprocessed DataFrame
    """
    # TODO: Implement once we have access to data and can analyze its structure
    # Expected steps:
    # 1. Handle missing values
    # 2. Encode categorical variables
    # 3. Scale numerical features
    # 4. Create new features if helpful
    return df

def prepare_training_data(df: pd.DataFrame, 
                         target_col: str = 'Transported',
                         test_size: float = 0.2,
                         random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Prepare training data by splitting into train/validation sets.
    
    Args:
        df: Input DataFrame
        target_col: Name of target column
        test_size: Proportion of data to use for validation
        random_state: Random seed for reproducibility
    
    Returns:
        Tuple of (X_train, X_val, y_train, y_val)
    """
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

def prepare_test_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare test data for predictions.
    
    Args:
        df: Input DataFrame
    
    Returns:
        Preprocessed test DataFrame
    """
    return df
