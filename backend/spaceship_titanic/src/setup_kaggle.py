"""
Set up Kaggle API authentication.
"""
import os
import json
from pathlib import Path

def setup_kaggle_auth():
    """Set up Kaggle API authentication using environment variables."""
    try:
        # Get Kaggle credentials from environment variables
        username = os.environ.get('username')
        key = os.environ.get('key')
        
        if not username or not key:
            raise ValueError("Missing Kaggle credentials in environment variables")
        
        # Create Kaggle directory if it doesn't exist
        kaggle_dir = Path.home() / '.kaggle'
        kaggle_dir.mkdir(exist_ok=True)
        
        # Create kaggle.json with credentials
        kaggle_json = kaggle_dir / 'kaggle.json'
        credentials = {
            'username': username,
            'key': key
        }
        
        # Write credentials to file
        with open(kaggle_json, 'w') as f:
            json.dump(credentials, f)
        
        # Set correct permissions
        os.chmod(kaggle_json, 0o600)
        
        print(f"Created Kaggle configuration at {kaggle_json}")
        print("Testing Kaggle API access...")
        
        # Test authentication
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi()
        api.authenticate()
        print('Kaggle authentication successful')
        return True
        
    except Exception as e:
        print(f"Error setting up Kaggle authentication: {e}")
        return False

if __name__ == '__main__':
    setup_kaggle_auth()
