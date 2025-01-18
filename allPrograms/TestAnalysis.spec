# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['TestAnalysis.py'],
    pathex=[],
    binaries=[],
    datas=[('thelab.kv', '.'), ('images (1).jpg', '.'), ('csv_format.jpeg', '.'), ('files_name.png', '.'), ('KivyAppData.db', '.'), ('AppIcon.ico', '.')],
    hiddenimports=['plyer.platforms.win.filechooser'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='TestAnalysis',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['AppIcon.ico'],
)
