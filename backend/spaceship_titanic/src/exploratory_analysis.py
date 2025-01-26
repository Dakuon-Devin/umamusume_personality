"""
スペースシップタイタニックのデータ探索的分析
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib

def setup_plotting_style():
    """Set up plotting style with Japanese font support"""
    plt.style.use('seaborn')
    sns.set_palette("viridis")  # 色覚に配慮したパレット
    plt.rcParams['figure.figsize'] = [12, 8]
    plt.rcParams['font.size'] = 12

def load_data():
    """データの読み込み"""
    data_dir = os.path.join('..', 'data')
    train_path = os.path.join(data_dir, 'train.csv')
    test_path = os.path.join(data_dir, 'test.csv')
    
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    return train_df, test_df

def analyze_missing_values(df, title="欠損値の分析"):
    """欠損値の分析とプロット"""
    plt.figure(figsize=(10, 6))
    missing_data = df.isnull().sum().sort_values(ascending=False)
    missing_percent = (missing_data / len(df) * 100).round(2)
    
    sns.barplot(x=missing_percent.values, y=missing_data.index)
    plt.title(f"{title}\n(全{len(df)}レコード中の欠損値の割合)")
    plt.xlabel("欠損値の割合 (%)")
    plt.tight_layout()
    return plt.gcf()

def analyze_categorical_features(df, target_col=None):
    """カテゴリカル特徴量の分析"""
    categorical_cols = ['HomePlanet', 'Destination', 'Cabin']
    
    for col in categorical_cols:
        plt.figure(figsize=(12, 6))
        if target_col:
            sns.countplot(data=df, x=col, hue=target_col)
            plt.title(f"{col}と{target_col}の関係")
        else:
            sns.countplot(data=df, x=col)
            plt.title(f"{col}の分布")
        plt.xticks(rotation=45)
        plt.tight_layout()
        yield plt.gcf()

def analyze_numerical_features(df, target_col=None):
    """数値特徴量の分析"""
    numerical_cols = ['Age', 'RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck']
    
    for col in numerical_cols:
        plt.figure(figsize=(12, 6))
        if target_col:
            sns.boxplot(data=df, x=target_col, y=col)
            plt.title(f"{col}の分布 (by {target_col})")
        else:
            sns.boxplot(data=df, y=col)
            plt.title(f"{col}の分布")
        plt.tight_layout()
        yield plt.gcf()

def analyze_correlations(df):
    """特徴量間の相関分析"""
    numerical_cols = ['Age', 'RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck']
    
    plt.figure(figsize=(10, 8))
    correlation_matrix = df[numerical_cols].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='viridis', center=0)
    plt.title("数値特徴量間の相関")
    plt.tight_layout()
    return plt.gcf()

def save_plots(plots, output_dir='../data/analysis'):
    """プロットの保存"""
    os.makedirs(output_dir, exist_ok=True)
    
    for i, plot in enumerate(plots):
        plot_path = os.path.join(output_dir, f'plot_{i}.png')
        plot.savefig(plot_path)
        plt.close(plot)

def main():
    """メイン分析実行関数"""
    setup_plotting_style()
    train_df, test_df = load_data()
    
    plots = []
    
    # 欠損値分析
    plots.append(analyze_missing_values(train_df, "訓練データの欠損値分析"))
    plots.append(analyze_missing_values(test_df, "テストデータの欠損値分析"))
    
    # カテゴリカル特徴量の分析
    plots.extend(analyze_categorical_features(train_df, 'Transported'))
    
    # 数値特徴量の分析
    plots.extend(analyze_numerical_features(train_df, 'Transported'))
    
    # 相関分析
    plots.append(analyze_correlations(train_df))
    
    # プロットの保存
    save_plots(plots)
    print("分析プロットを保存しました。")

if __name__ == '__main__':
    main()
