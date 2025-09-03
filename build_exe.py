"""
Builds the Clipdex application into a single executable file.
Usage:  python build_exe.py
"""

import PyInstaller.__main__
import sys
from pathlib import Path

def build_app():
    """Build the application with platform-specific settings."""
    
    # Base arguments
    args = [
        '--onefile',
        '--clean',
        '--noconfirm',
        '--name=Clipdex',
        '--windowed',
        '--add-data=clipdex_gui/assets;clipdex_gui/assets',
        '--add-data=config.json;.',
        '--add-data=snippets.json;.',
        'main.py'
    ]
    
    # Platform-specific icon
    assets_dir = Path('clipdex_gui/assets/icon_package')
    if sys.platform.startswith('win'):
        icon_path = assets_dir / 'app_icon.ico'
        if icon_path.exists():
            args.insert(-1, f'--icon={icon_path}')
    elif sys.platform == 'darwin':
        icon_path = assets_dir / 'app_icon.icns'
        if icon_path.exists():
            args.insert(-1, f'--icon={icon_path}')
    else:  # Linux
        icon_path = assets_dir / 'icon_512x512.png'
        if icon_path.exists():
            args.insert(-1, f'--icon={icon_path}')
    
    print(f"Building for platform: {sys.platform}")
    print(f"Arguments: {args}")
    
    PyInstaller.__main__.run(args)

if __name__ == '__main__':
    build_app()