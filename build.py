import PyInstaller.__main__

PyInstaller.__main__.run([
    'run.py',
    '--onefile',
    '--windowed',
    '--name=Skintils',
    '--hidden-import=PIL._tkinter_finder',
    '--hidden-import=skintils.ui',
    '--hidden-import=skintils.processor',
])