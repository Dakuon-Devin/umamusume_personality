"""
Inspect and summarize the Spaceship Titanic competition data.
"""
import pandas as pd
import json
from pathlib import Path

def create_data_summary():
    """Create a summary of the competition data files."""
    # Read the data files
    data_dir = Path('../data')
    train_df = pd.read_csv(data_dir / 'train.csv')
    test_df = pd.read_csv(data_dir / 'test.csv')
    
    # Create data summary
    data_info = {
        'train': {
            'rows': len(train_df),
            'columns': train_df.columns.tolist(),
            'missing_values': train_df.isnull().sum().to_dict(),
            'dtypes': train_df.dtypes.astype(str).to_dict()
        },
        'test': {
            'rows': len(test_df),
            'columns': test_df.columns.tolist(),
            'missing_values': test_df.isnull().sum().to_dict(),
            'dtypes': test_df.dtypes.astype(str).to_dict()
        }
    }
    
    # Save data summary
    summary_path = data_dir / 'data_summary.json'
    with open(summary_path, 'w') as f:
        json.dump(data_info, f, indent=2)
    
    print('Data Summary:')
    print(json.dumps(data_info, indent=2))

if __name__ == '__main__':
    create_data_summary()
