# -*- mode: python -*-
a = Analysis(['3DPrinter.py'],
             pathex=['C:\\Users\\ModuleWoks\\Documents\\Development\\GitRep\\gcode2cutsim'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='3DPTestStage.exe',
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
               name='3DPrinterTeststage')
