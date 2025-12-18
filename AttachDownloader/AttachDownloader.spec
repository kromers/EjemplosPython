# -*- mode: python ; coding: utf-8 -*-

# PyInstaller spec file for AttachDownloader
# Generated to produce one-file executable that bundles all runtime
# dependencies but intentionally DOES NOT bundle external configuration
# files (config/*) ni documentación/ayuda.

block_cipher = None

import sys
from PyInstaller.utils.hooks import collect_submodules

# Some google packages are dynamically imported; ensure they are collected
hidden_imports = [
    'googleapiclient.discovery',
    'google.auth.transport.requests',
    'google.oauth2.credentials',
    'httplib2',
    'oauthlib',
    'requests',
]
# Add any other dynamically imported submodules under google
hidden_imports += collect_submodules('google')

a = Analysis(
    ['src/main.py'],
    pathex=['.', 'src'],  # Añadir 'src' para que se resuelva el paquete local
    binaries=[],
    # Incluir el paquete local 'gmail_downloader' para asegurarnos que se empaqueta
    datas=[('src/gmail_downloader', 'gmail_downloader')],
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
    name='AttachDownloader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AttachDownloader',
)
