"""
Spaceship Titanicデータセットの探索的データ分析

このスクリプトでは以下の分析を行います：
1. データの基本統計量
2. 特徴量の分布
3. 欠損値の分析
4. カテゴリカル変数の分析
5. 特徴量間の相関分析
"""
import os
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json

# プロットのスタイル設定
plt.style.use('seaborn-v0_8')  # 新しいバージョンのseabornスタイル
sns.set_theme(style="whitegrid")  # seabornのテーマを設定
sns.set_palette('husl')

# 日本語フォントの設定（利用可能なフォントがない場合はデフォルトを使用）
try:
    plt.rcParams['font.family'] = 'IPAexGothic'
except:
    print('Warning: IPAexGothic font not found. Using default font.')

def load_data():
    """データの読み込み"""
    data_dir = Path('../data/raw')
    train_df = pd.read_csv(data_dir / 'train.csv')
    test_df = pd.read_csv(data_dir / 'test.csv')
    return train_df, test_df

def analyze_numerical_features(train_df, output_dir):
    """数値特徴量の分布分析"""
    numerical_features = ['Age', 'RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck']
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.ravel()
    
    for idx, feature in enumerate(numerical_features):
        sns.histplot(data=train_df, x=feature, ax=axes[idx])
        axes[idx].set_title(f'{feature}の分布')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'numerical_distributions.png')
    plt.close()
    
    # 基本統計量を保存
    stats = train_df[numerical_features].describe()
    stats.to_csv(output_dir / 'numerical_statistics.csv')

def analyze_missing_values(train_df, test_df, output_dir):
    """欠損値の分析"""
    missing_train = (train_df.isnull().sum() / len(train_df) * 100).sort_values(ascending=False)
    missing_test = (test_df.isnull().sum() / len(test_df) * 100).sort_values(ascending=False)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    sns.barplot(x=missing_train.values, y=missing_train.index, ax=ax1)
    ax1.set_title('訓練データの欠損値割合')
    ax1.set_xlabel('欠損値の割合 (%)')
    
    sns.barplot(x=missing_test.values, y=missing_test.index, ax=ax2)
    ax2.set_title('テストデータの欠損値割合')
    ax2.set_xlabel('欠損値の割合 (%)')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'missing_values.png')
    plt.close()
    
    # 欠損値の詳細を保存
    missing_stats = {
        'train': missing_train.to_dict(),
        'test': missing_test.to_dict()
    }
    with open(output_dir / 'missing_values.json', 'w') as f:
        json.dump(missing_stats, f, indent=2)

def analyze_categorical_features(train_df, output_dir):
    """カテゴリカル変数の分析"""
    categorical_features = ['HomePlanet', 'CryoSleep', 'Destination', 'VIP']
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    axes = axes.ravel()
    
    categorical_stats = {}
    
    for idx, feature in enumerate(categorical_features):
        # 各カテゴリの転送率を計算
        transport_rate = train_df.groupby(feature)['Transported'].mean().sort_values(ascending=False)
        categorical_stats[feature] = transport_rate.to_dict()
        
        sns.barplot(x=transport_rate.index, y=transport_rate.values, ax=axes[idx])
        axes[idx].set_title(f'{feature}別の転送率')
        axes[idx].set_ylabel('転送率')
        axes[idx].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'categorical_analysis.png')
    plt.close()
    
    # カテゴリカル変数の統計を保存
    with open(output_dir / 'categorical_statistics.json', 'w') as f:
        json.dump(categorical_stats, f, indent=2)

def analyze_correlations(train_df, output_dir):
    """特徴量間の相関分析"""
    numerical_features = ['Age', 'RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck']
    correlation_matrix = train_df[numerical_features].corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('数値特徴量間の相関')
    plt.savefig(output_dir / 'correlation_matrix.png')
    plt.close()
    
    # 相関行列を保存
    correlation_matrix.to_csv(output_dir / 'correlation_matrix.csv')

def main():
    """メイン関数"""
    # 出力ディレクトリの作成
    output_dir = Path('../data/analysis')
    output_dir.mkdir(exist_ok=True)
    
    # データの読み込み
    train_df, test_df = load_data()
    
    # 各分析の実行
    analyze_numerical_features(train_df, output_dir)
    analyze_missing_values(train_df, test_df, output_dir)
    analyze_categorical_features(train_df, output_dir)
    analyze_correlations(train_df, output_dir)
    
    print('分析が完了しました。結果は以下のディレクトリに保存されています：')
    print(output_dir.absolute())

if __name__ == '__main__':
    main()
