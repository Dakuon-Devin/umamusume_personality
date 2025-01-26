"""
Data preprocessing module for Spaceship Titanic competition.
"""
from typing import Tuple, Dict, Any
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer

def extract_cabin_features(cabin: str) -> Tuple[str, int, str]:
    """
    Extract deck, num, and side from cabin string.
    Format: deck/num/side where side is P (Port) or S (Starboard)
    
    Args:
        cabin: Cabin string in format 'deck/num/side'
    
    Returns:
        Tuple of (deck, num, side)
    """
    if pd.isna(cabin):
        return np.nan, np.nan, np.nan
    try:
        deck, num, side = cabin.split('/')
        return deck, int(num), side
    except:
        return np.nan, np.nan, np.nan

def extract_passenger_group(passenger_id: str) -> Tuple[int, int]:
    """
    Extract group number and position from PassengerId.
    Format: gggg_pp where gggg is group and pp is position
    
    Args:
        passenger_id: PassengerId string
    
    Returns:
        Tuple of (group_number, position)
    """
    try:
        group, position = passenger_id.split('_')
        return int(group), int(position)
    except:
        return np.nan, np.nan

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
    # Create a copy to avoid modifying original data
    df = df.copy()
    
    # Extract features from PassengerId
    df['GroupNumber'], df['GroupPosition'] = zip(*df['PassengerId'].map(extract_passenger_group))
    
    # Extract features from Cabin
    df[['Deck', 'CabinNumber', 'Side']] = pd.DataFrame(
        df['Cabin'].map(extract_cabin_features).tolist(),
        columns=['Deck', 'CabinNumber', 'Side']
    )
    
    # Handle boolean features
    df['CryoSleep'] = df['CryoSleep'].astype('float')
    df['VIP'] = df['VIP'].astype('float')
    
    # Split RoomService, FoodCourt, ShoppingMall, Spa, VRDeck into bins
    expense_columns = ['RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck']
    for col in expense_columns:
        df[f'{col}_binned'] = pd.qcut(df[col].fillna(-1), q=10, labels=False, duplicates='drop')
    
    # Calculate total expenses
    df['TotalExpenses'] = df[expense_columns].sum(axis=1)
    
    # Create age groups
    df['AgeGroup'] = pd.qcut(df['Age'].fillna(-1), q=10, labels=False, duplicates='drop')
    
    # Handle categorical variables
    categorical_columns = ['HomePlanet', 'Destination', 'Deck', 'Side']
    for col in categorical_columns:
        df[col] = df[col].astype('category')
        if is_training:
            df[col] = LabelEncoder().fit_transform(df[col].astype(str))
    
    # Handle numerical features
    numerical_columns = ['Age', 'GroupNumber', 'CabinNumber'] + expense_columns
    for col in numerical_columns:
        if is_training:
            imputer = SimpleImputer(strategy='median')
            df[col] = imputer.fit_transform(df[[col]])
        scaler = StandardScaler()
        df[col] = scaler.fit_transform(df[[col]])
    
    # Drop original columns that have been transformed
    columns_to_drop = ['PassengerId', 'Cabin'] + expense_columns
    df = df.drop(columns=columns_to_drop)
    
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
