# -*- mode: python -*-
a = Analysis(['3DPrinter.py'],
             pathex=['.'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
#a.datas.append(('DATA'))

for d in a.datas:
    if 'pyconfig' in d[0]:
        a.datas.remove(d)
        break

pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name=os.path.join('dist', '3DPrinter.exe'),
    debug=False,
    strip=None,
    upx=True,
    console=True )
