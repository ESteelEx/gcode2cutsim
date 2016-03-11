# -*- mode: python -*-
a = Analysis(['gcode2cutsim.py'],
             pathex=['D:\\Development\\GitRep\\gcode2cutsim'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='gcode2cutsim.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True,
          icon='bin\\images\\3dPrintVer.ico' )
