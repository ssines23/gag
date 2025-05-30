# clip_trigger.spec
from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

# Path to your Python entry point
script_path = 'clip_trigger.py'

# OBS portable directory to bundle
obs_data = ('obs-portable', 'obs-portable')

# Collect any dynamic modules (for packages like obswebsocket)
hidden_imports = collect_submodules('obswebsocket')

a = Analysis(
    [script_path],
    pathex=[],
    binaries=[],
    datas=[obs_data],
    hiddenimports=hidden_imports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='RocketClipper',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Set to False to hide the terminal window
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='RocketClipper'
)
