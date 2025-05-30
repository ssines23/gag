# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

a = Analysis(
    ['gag.py'],  # Your new entry point
    pathex=[],
    binaries=[],
    datas=[
        ('obs-portable', 'obs-portable'),  # OBS folder
        ('f8_sound.wav', '.'),             # Sound file in root
        ('README.txt', '.'),               # Optional: Usage notes
    ],
    hiddenimports=collect_submodules('obswebsocket'),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='gag',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    icon='gag.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='gag',
)
