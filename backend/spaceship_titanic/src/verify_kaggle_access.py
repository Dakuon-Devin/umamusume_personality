"""
Verify Kaggle API authentication and competition access.
"""
from kaggle.api.kaggle_api_extended import KaggleApi

def verify_competition_access():
    """Verify that we can access the Spaceship Titanic competition."""
    try:
        # Initialize and authenticate
        api = KaggleApi()
        api.authenticate()
        print('Authentication successful')
        
        # Test competition access
        competitions = api.competition_list(search='spaceship-titanic')
        if any(comp.ref == 'spaceship-titanic' for comp in competitions):
            print('Successfully accessed Spaceship Titanic competition')
            return True
        else:
            print('Competition not found')
            return False
    except Exception as e:
        print(f'Error accessing Kaggle API: {e}')
        return False

if __name__ == '__main__':
    verify_competition_access()
