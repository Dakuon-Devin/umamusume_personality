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
import matplotlib

# バックエンドを設定（メモリ使用量を抑制）
matplotlib.use('Agg')

# プロットのスタイル設定
plt.style.use('seaborn-v0_8')  # 新しいバージョンのseabornスタイル
sns.set_theme(style="whitegrid")  # seabornのテーマを設定
sns.set_palette('husl')

# フォントの設定
import matplotlib
import matplotlib.font_manager as fm

# IPAexGothicフォントのパスを設定
font_path = '/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf'
font_prop = fm.FontProperties(fname=font_path)

# フォントの登録
fm.fontManager.addfont(font_path)

# プロットの設定
plt.rcParams['font.family'] = ['IPAexGothic']
plt.rcParams['font.sans-serif'] = ['IPAexGothic']
plt.rcParams['font.size'] = 12  # フォントサイズを大きくして読みやすく
plt.rcParams['axes.unicode_minus'] = False  # マイナス記号を正しく表示
plt.rcParams['figure.figsize'] = [12, 8]  # 図のサイズを大きくして見やすく
plt.rcParams['figure.dpi'] = 300  # 解像度を高く設定

# タイトルなどのテキストにフォントを設定する関数
def set_plot_font(ax):
    """Set font for plot title and labels"""
    if ax.get_title():
        ax.set_title(ax.get_title(), fontproperties=font_prop)
    ax.set_xlabel(ax.get_xlabel(), fontproperties=font_prop)
    ax.set_ylabel(ax.get_ylabel(), fontproperties=font_prop)

def load_data():
    """データの読み込み"""
    data_dir = Path('../data')
    train_df = pd.read_csv(data_dir / 'train.csv')
    test_df = pd.read_csv(data_dir / 'test.csv')
    return train_df, test_df

def analyze_numerical_features(train_df, output_dir):
    """数値特徴量の分布分析"""
    numerical_features = ['Age', 'RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck']
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.ravel()
    
    for idx, feature in enumerate(numerical_features):
        sns.histplot(data=train_df, x=feature, ax=axes[idx], hue='Transported')
        axes[idx].set_title(f'{feature}の分布', fontproperties=font_prop)
        axes[idx].set_xlabel(feature, fontproperties=font_prop)
        axes[idx].set_ylabel('頻度', fontproperties=font_prop)
        
    plt.suptitle('数値特徴量の分布（転送状態別）', fontsize=14, fontproperties=font_prop)
    plt.tight_layout()
    plt.savefig(output_dir / 'numerical_distributions.png', bbox_inches='tight', dpi=300)
    plt.close()
    
    # 基本統計量を保存
    stats = train_df[numerical_features].describe()
    stats.to_csv(output_dir / 'numerical_statistics.csv')

def analyze_missing_values(train_df, test_df, output_dir):
    """欠損値の分析"""
    missing_train = (train_df.isnull().sum() / len(train_df) * 100).sort_values(ascending=False)
    missing_test = (test_df.isnull().sum() / len(test_df) * 100).sort_values(ascending=False)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))
    
    sns.barplot(x=missing_train.values, y=missing_train.index, ax=ax1, palette='husl')
    ax1.set_title('訓練データの欠損値割合', fontproperties=font_prop, fontsize=12)
    ax1.set_xlabel('欠損値の割合 (%)', fontproperties=font_prop)
    ax1.set_ylabel('特徴量', fontproperties=font_prop)
    
    sns.barplot(x=missing_test.values, y=missing_test.index, ax=ax2, palette='husl')
    ax2.set_title('テストデータの欠損値割合', fontproperties=font_prop, fontsize=12)
    ax2.set_xlabel('欠損値の割合 (%)', fontproperties=font_prop)
    ax2.set_ylabel('特徴量', fontproperties=font_prop)
    
    plt.suptitle('データセットの欠損値分析', fontsize=14, fontproperties=font_prop)
    plt.tight_layout()
    plt.savefig(output_dir / 'missing_values.png', bbox_inches='tight', dpi=300)
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
        
        sns.barplot(x=transport_rate.index, y=transport_rate.values, ax=axes[idx], palette='husl')
        axes[idx].set_title(f'{feature}別の転送率', fontproperties=font_prop, fontsize=12)
        axes[idx].set_ylabel('転送率', fontproperties=font_prop)
        axes[idx].set_xlabel(feature, fontproperties=font_prop)
        axes[idx].tick_params(axis='x', rotation=45)
        
        # パーセント表示に変換
        axes[idx].set_yticklabels([f'{x:.1%}' for x in axes[idx].get_yticks()])
    
    plt.suptitle('カテゴリ別の転送率分析', fontsize=14, fontproperties=font_prop)
    plt.tight_layout()
    plt.savefig(output_dir / 'categorical_analysis.png', bbox_inches='tight', dpi=300)
    plt.close()
    
    # カテゴリカル変数の統計を保存
    with open(output_dir / 'categorical_statistics.json', 'w') as f:
        json.dump(categorical_stats, f, indent=2)

def analyze_correlations(train_df, output_dir):
    """特徴量間の相関分析"""
    numerical_features = ['Age', 'RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck']
    correlation_matrix = train_df[numerical_features].corr()
    
    plt.figure(figsize=(12, 10))
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
    sns.heatmap(correlation_matrix, 
                mask=mask,
                annot=True, 
                cmap='coolwarm', 
                center=0,
                fmt='.2f',
                square=True,
                linewidths=0.5)
    
    plt.title('数値特徴量間の相関係数', fontproperties=font_prop, fontsize=14, pad=20)
    plt.xticks(fontproperties=font_prop)
    plt.yticks(fontproperties=font_prop, rotation=0)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'correlation_matrix.png', bbox_inches='tight', dpi=300)
    plt.close()
    
    # 相関行列を保存
    correlation_matrix.to_csv(output_dir / 'correlation_matrix.csv')

def main():
    """メイン関数"""
    try:
        print("探索的データ分析を開始します...")
        
        # 出力ディレクトリの作成
        output_dir = Path('../data/analysis')
        output_dir.mkdir(exist_ok=True)
        print(f"出力ディレクトリを作成しました: {output_dir.absolute()}")
        
        # データの読み込み
        print("データを読み込んでいます...")
        train_df, test_df = load_data()
        print(f"データ読み込み完了 - 訓練データ: {train_df.shape}, テストデータ: {test_df.shape}")
        
        # メモリ使用量を最適化
        print("大きなデータセットをサンプリングします...")
        sample_size = min(5000, len(train_df))
        train_sample = train_df.sample(n=sample_size, random_state=42) if len(train_df) > sample_size else train_df
        
        # 各分析の実行
        print("\n数値特徴量の分布を分析中...")
        analyze_numerical_features(train_sample, output_dir)
        print("✓ 数値特徴量の分析が完了しました")
        
        print("\n欠損値を分析中...")
        analyze_missing_values(train_df, test_df, output_dir)
        print("✓ 欠損値の分析が完了しました")
        
        print("\nカテゴリカル変数を分析中...")
        analyze_categorical_features(train_sample, output_dir)
        print("✓ カテゴリカル変数の分析が完了しました")
        
        print("\n特徴量間の相関を分析中...")
        analyze_correlations(train_sample, output_dir)
        print("✓ 相関分析が完了しました")
        
        print("\n分析が完了しました。結果は以下のディレクトリに保存されています：")
        print(output_dir.absolute())
        
        # 生成されたファイルの一覧を表示
        print("\n生成されたファイル：")
        for file in output_dir.glob('*'):
            print(f"- {file.name}")
            
    except Exception as e:
        print(f"\nエラーが発生しました: {str(e)}")
        raise

if __name__ == '__main__':
    main()
