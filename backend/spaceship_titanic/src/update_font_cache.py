"""
Update matplotlib font cache and verify IPAexGothic font availability
"""
import os
import matplotlib
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

def setup_font():
    """Configure matplotlib to use IPAexGothic font"""
    font_path = '/usr/share/fonts/truetype/ipaex/ipaexg.ttf'
    if not os.path.exists(font_path):
        print(f"Error: Font file not found at {font_path}")
        return False
        
    # Add custom font
    fm.fontManager.addfont(font_path)
    
    # Configure matplotlib
    matplotlib.rc('font', family='IPAexGothic')
    
    return True

def main():
    """Update font cache and check IPAexGothic availability"""
    print("Setting up IPAexGothic font...")
    if not setup_font():
        return
    
    # List available fonts containing 'IPA'
    print("\nScanning for IPA fonts...")
    ipa_fonts = [f.name for f in fm.fontManager.ttflist if 'IPA' in f.name]
    print('Available IPA fonts:', ipa_fonts)
    
    if any('IPAexGothic' in font for font in ipa_fonts):
        print("✓ IPAexGothic font is available")
    else:
        print("✗ IPAexGothic font not found")

if __name__ == '__main__':
    main()
