"""
Test Japanese text rendering in matplotlib
"""
import os
import matplotlib.pyplot as plt
import numpy as np

def test_plot():
    """Create a simple plot with Japanese text"""
    # Set up the plot with explicit font configuration
    plt.figure(figsize=(10, 6))
    
    # Generate sample data
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    
    # Create plot with Japanese text
    plt.plot(x, y)
    plt.title('日本語のテスト - テストプロット', fontname='IPAexGothic')
    plt.xlabel('X軸', fontname='IPAexGothic')
    plt.ylabel('Y軸', fontname='IPAexGothic')
    
    # Ensure output directory exists
    output_dir = '../data/analysis'
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the plot
    plt.savefig(os.path.join(output_dir, 'test_japanese.png'))
    plt.close()

if __name__ == '__main__':
    # First run the font cache update
    import update_font_cache
    update_font_cache.main()
    
    print("\nCreating test plot...")
    test_plot()
    print("Test plot saved to ../data/analysis/test_japanese.png")
