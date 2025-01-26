"""
Training script for Spaceship Titanic competition.
"""
import os
from pathlib import Path
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report

from data_preprocessing import (
    load_data,
    preprocess_features,
    prepare_training_data
)
from model import SpaceshipModel

def train_model(data_dir: str = '../data',
                model_dir: str = '../models',
                model_params: dict = None) -> Tuple[SpaceshipModel, Preprocessor]:
    """
    スペースシップタイタニックのデータでモデルを訓練する。

    Args:
        data_dir: データファイルのディレクトリ
        model_dir: モデルファイルを保存するディレクトリ
        model_params: モデルのパラメータ

    Returns:
        訓練済みモデルと前処理器のタプル
    """
    # データの読み込みと前処理
    train_df, _ = load_data(
        os.path.join(data_dir, 'train.csv'),
        os.path.join(data_dir, 'test.csv')
    )
    
    # 前処理器の初期化と特徴量の前処理
    preprocessor = Preprocessor()
    processed_df = preprocessor.preprocess_features(train_df)
    
    # データの分割
    X_train, X_val, y_train, y_val = prepare_training_data(processed_df)
    
    # モデルの初期化と訓練
    model = SpaceshipModel(model_params)
    model.feature_names = X_train.columns.tolist()
    model.fit(X_train, y_train)
    
    # 評価
    val_preds = model.predict(X_val)
    accuracy = accuracy_score(y_val, val_preds)
    print(f"検証精度: {accuracy:.4f}")
    print("\n分類レポート:")
    print(classification_report(y_val, val_preds))
    
    # 特徴量の重要度を表示
    importances = model.get_feature_importance()
    print("\n特徴量の重要度:")
    for feature, importance in sorted(importances.items(), key=lambda x: x[1], reverse=True):
        print(f"{feature}: {importance:.4f}")
    
    return model, preprocessor

if __name__ == '__main__':
    # TODO: Add argument parsing for model parameters
    model = train_model()
