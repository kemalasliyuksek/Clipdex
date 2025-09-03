"""
Builds the Clipdex application into a single .exe file.
Usage:  python build_exe.py
"""

import PyInstaller.__main__

PyInstaller.__main__.run([
    '--onefile',
    '--clean',
    '--noconfirm',
    '--name=Clipdex',
    '--windowed',
    '--icon=clipdex_gui/assets/icon_package/app_icon.ico',
    '--add-data=clipdex_gui/assets;clipdex_gui/assets',
    '--add-data=config.json;.',
    '--add-data=snippets.json;.',
    'main.py'
])