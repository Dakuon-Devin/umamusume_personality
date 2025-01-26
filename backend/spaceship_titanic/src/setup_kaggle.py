"""
Set up Kaggle authentication and verify access.
"""
import os
import json
from pathlib import Path
import subprocess

def setup_kaggle_auth():
    """Set up Kaggle authentication and verify it works."""
    try:
        # Create .kaggle directory if it doesn't exist
        kaggle_dir = Path.home() / '.kaggle'
        kaggle_dir.mkdir(exist_ok=True)
        
        # Create kaggle.json with credentials
        kaggle_json = kaggle_dir / 'kaggle.json'
        credentials = {
            'username': os.environ.get('username'),
            'key': os.environ.get('key')
        }
        
        # Verify we have the credentials
        if not credentials['username'] or not credentials['key']:
            raise ValueError("Missing Kaggle credentials in environment variables")
        
        # Write credentials to file
        with open(kaggle_json, 'w') as f:
            json.dump(credentials, f)
        
        # Set correct permissions
        subprocess.run(['chmod', '600', str(kaggle_json)], check=True)
        
        print(f"Created Kaggle configuration at {kaggle_json}")
        print("Testing Kaggle API access...")
        
        # Set Kaggle API environment variables
        os.environ['KAGGLE_USERNAME'] = credentials['username']
        os.environ['KAGGLE_KEY'] = credentials['key']
        
        # Import Kaggle API after setting environment variables
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
