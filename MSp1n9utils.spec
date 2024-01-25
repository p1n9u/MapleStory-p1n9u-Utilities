# -*- mode: python ; coding: utf-8 -*-

added_files=[
    ('./resources/snd/*', './resources/snd'),
    ('./resources/ui/*', './resources/ui'),
    ('./resources/icon/*', './resources/icon'),
    ('./resources/img/*', './resources/img'),
    ('./log/*', './log'),
    ('./nexon_api_key/*', './nexon_api_key')
]

a = Analysis(
    ['App.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[],
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
    name='MSp1n9utils',
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
    icon=['resources\\icon\\favicon.ico'],
)
