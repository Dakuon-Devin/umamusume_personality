"""
Download Spaceship Titanic competition data using Kaggle API
"""
import os
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi

def download_competition_data():
    """Download data from Kaggle competition"""
    print("Kaggle APIで認証中...")
    api = KaggleApi()
    api.authenticate()
    
    # Create data directory if it doesn't exist
    data_dir = Path('../data')
    data_dir.mkdir(exist_ok=True)
    
    print("データをダウンロード中...")
    competition = "spaceship-titanic"
    api.competition_download_files(
        competition,
        path=str(data_dir),
        quiet=False
    )
    
    # Unzip the downloaded file
    import zipfile
    zip_path = data_dir / f"{competition}.zip"
    if zip_path.exists():
        print("ZIPファイルを展開中...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(data_dir)
        # Remove zip file after extraction
        zip_path.unlink()
        print("データのダウンロードと展開が完了しました")
    else:
        print("エラー: ZIPファイルが見つかりません")

if __name__ == '__main__':
    download_competition_data()
