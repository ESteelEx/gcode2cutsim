# -*- mode: python -*-
a = Analysis(['gcode2cutsim.py'],
             pathex=['C:\\Users\\ModuleWoks\\Documents\\Development\\GitRep\\gcode2cutsim'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='gcode2cutsim.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='gcode2cutsim')
