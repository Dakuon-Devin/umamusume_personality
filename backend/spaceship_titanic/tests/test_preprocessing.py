"""
Tests for data preprocessing pipeline.
"""
import pytest
import pandas as pd
import numpy as np
from src.data_preprocessing import (
    extract_cabin_features,
    extract_passenger_group,
    preprocess_features
)

def test_extract_cabin_features():
    """Test cabin feature extraction."""
    # Test valid cabin string
    assert extract_cabin_features("B/123/P") == ("B", 123, "P")
    
    # Test missing cabin
    assert extract_cabin_features(np.nan) == (np.nan, np.nan, np.nan)
    
    # Test invalid format
    assert extract_cabin_features("invalid") == (np.nan, np.nan, np.nan)

def test_extract_passenger_group():
    """Test passenger group extraction."""
    # Test valid passenger ID
    assert extract_passenger_group("1234_56") == (1234, 56)
    
    # Test invalid format
    assert extract_passenger_group("invalid") == (np.nan, np.nan)

def test_preprocess_features():
    """Test feature preprocessing pipeline."""
    # Create sample data
    sample_data = pd.DataFrame({
        'PassengerId': ['1234_56', '7890_12'],
        'HomePlanet': ['Earth', 'Mars'],
        'CryoSleep': [True, False],
        'Cabin': ['B/123/P', 'G/789/S'],
        'Destination': ['TRAPPIST-1e', 'PSO J318.5-22'],
        'Age': [20.0, 30.0],
        'VIP': [False, True],
        'RoomService': [100.0, 200.0],
        'FoodCourt': [50.0, 150.0],
        'ShoppingMall': [0.0, 300.0],
        'Spa': [200.0, 100.0],
        'VRDeck': [30.0, 400.0]
    })
    
    # Process features
    processed_df = preprocess_features(sample_data)
    
    # Verify expected columns exist
    expected_columns = {
        'GroupNumber', 'GroupPosition', 'Deck', 'CabinNumber', 'Side',
        'CryoSleep', 'VIP', 'TotalExpenses', 'AgeGroup'
    }
    assert all(col in processed_df.columns for col in expected_columns)
    
    # Verify numerical features are scaled
    assert processed_df['Age'].mean() == pytest.approx(0, abs=1e-10)
    assert processed_df['TotalExpenses'].mean() == pytest.approx(0, abs=1e-10)
    
    # Verify categorical features are encoded
    assert processed_df['HomePlanet'].dtype != 'object'
    assert processed_df['Destination'].dtype != 'object'
    
    # Verify boolean features are converted to float
    assert processed_df['CryoSleep'].dtype == 'float64'
    assert processed_df['VIP'].dtype == 'float64'

def test_preprocess_features_with_missing_values():
    """Test preprocessing with missing values."""
    # Create sample data with missing values
    sample_data = pd.DataFrame({
        'PassengerId': ['1234_56', '7890_12'],
        'HomePlanet': ['Earth', np.nan],
        'CryoSleep': [True, np.nan],
        'Cabin': [np.nan, 'G/789/S'],
        'Destination': ['TRAPPIST-1e', np.nan],
        'Age': [20.0, np.nan],
        'VIP': [False, np.nan],
        'RoomService': [np.nan, 200.0],
        'FoodCourt': [50.0, np.nan],
        'ShoppingMall': [0.0, np.nan],
        'Spa': [np.nan, 100.0],
        'VRDeck': [30.0, np.nan]
    })
    
    # Process features
    processed_df = preprocess_features(sample_data)
    
    # Verify no missing values in processed data
    assert not processed_df.isnull().any().any()

if __name__ == '__main__':
    pytest.main([__file__])
