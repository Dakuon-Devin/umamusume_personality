"""
Verify Kaggle API authentication and competition access.
"""
from kaggle.api.kaggle_api_extended import KaggleApi
import os

def verify_competition_access():
    """Verify that we can access the Spaceship Titanic competition."""
    try:
        # Initialize and authenticate
        api = KaggleApi()
        api.authenticate()
        print('Authentication successful')
        
        # Test competition access by trying to download competition files
        # This will raise an error if we can't access the competition
        competition_name = 'spaceship-titanic'
        api.competition_download_files(
            competition_name,
            path='../data',
            quiet=False
        )
        print('Successfully accessed Spaceship Titanic competition')
        return True
        
    except Exception as e:
        print(f'Error accessing Kaggle API: {e}')
        return False

if __name__ == '__main__':
    # Create data directory if it doesn't exist
    os.makedirs('../data', exist_ok=True)
    verify_competition_access()
