"""
Builds the Clipdex application into a single .exe file.
Usage:  python build_exe.py
"""

import PyInstaller.__main__

PyInstaller.__main__.run([
    '--clean',                 # Delete old build files
    '--noconfirm',             # Don't ask for user confirmation
    '--name=Clipdex',          # Output exe name
    '--windowed',              # Hide console window (GUI application)
    '--icon=clipdex_gui/assets/icon_package/app_icon.ico',
    # The application needs the following data files ↓
    '--add-data=snippets.json;.',          # ; = Windows separator
    '--add-data=config.json;.',
    '--add-data=clipdex_gui/assets;clipdex_gui/assets',
    'main.py'                  # Entry point
])