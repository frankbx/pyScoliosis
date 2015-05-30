# -*- mode: python -*-
a = Analysis(['pyScoliosis.py'],
             pathex=['C:\\PycharmProjects\\pyScoliosis'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='pyScoliosis.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False )
