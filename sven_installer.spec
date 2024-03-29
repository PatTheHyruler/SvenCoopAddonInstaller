# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['sven_installer.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'patoolib.programs',
        'patoolib.programs.ar',
        'patoolib.programs.arc',
        'patoolib.programs.archmage',
        'patoolib.programs.bsdcpio',
        'patoolib.programs.bsdtar',
        'patoolib.programs.bzip2',
        'patoolib.programs.cabextract',
        'patoolib.programs.chmlib',
        'patoolib.programs.clzip',
        'patoolib.programs.compress',
        'patoolib.programs.cpio',
        'patoolib.programs.dpkg',
        'patoolib.programs.flac',
        'patoolib.programs.genisoimage',
        'patoolib.programs.gzip',
        'patoolib.programs.isoinfo',
        'patoolib.programs.lbzip2',
        'patoolib.programs.lcab',
        'patoolib.programs.lha',
        'patoolib.programs.lhasa',
        'patoolib.programs.lrzip',
        'patoolib.programs.lzip',
        'patoolib.programs.lzma',
        'patoolib.programs.lzop',
        'patoolib.programs.mac',
        'patoolib.programs.nomarch',
        'patoolib.programs.p7azip',
        'patoolib.programs.p7rzip',
        'patoolib.programs.p7zip',
        'patoolib.programs.pbzip2',
        'patoolib.programs.pdlzip',
        'patoolib.programs.pigz',
        'patoolib.programs.plzip',
        'patoolib.programs.py_bz2',
        'patoolib.programs.py_echo',
        'patoolib.programs.py_gzip',
        'patoolib.programs.py_lzma',
        'patoolib.programs.py_tarfile',
        'patoolib.programs.py_zipfile',
        'patoolib.programs.rar',
        'patoolib.programs.rpm',
        'patoolib.programs.rpm2cpio',
        'patoolib.programs.rzip',
        'patoolib.programs.shar',
        'patoolib.programs.shorten',
        'patoolib.programs.star',
        'patoolib.programs.tar',
        'patoolib.programs.unace',
        'patoolib.programs.unadf',
        'patoolib.programs.unalz',
        'patoolib.programs.uncompress',
        'patoolib.programs.unrar',
        'patoolib.programs.unshar',
        'patoolib.programs.unzip',
        'patoolib.programs.xdms',
        'patoolib.programs.xz',
        'patoolib.programs.zip',
        'patoolib.programs.zoo',
        'patoolib.programs.zopfli',
        'patoolib.programs.zpaq',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='sven_installer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)