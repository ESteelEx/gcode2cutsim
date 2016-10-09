import shutil, psutil

for proc in psutil.process_iter():
    try:
        if proc.name() == 'paramGuard.exe':
            try:
                proc.kill()
            except:
                pass
    except:
        pass

# -*- mode: python -*-
a = Analysis(['parameterGuard.py'],
              pathex=['.'], 
              hiddenimports=[],
              hookspath=None, 
              runtime_hooks=None)

# a.datas.append(('cacert.pem', 'cacert.pem', 'DATA'))

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
    name=os.path.join('dist', 'paramGuard.exe'),
    debug=False,
    strip=None,
    upx=True, 
    console=True,
    icon='..\\..\\bin\\images\\paramGuard.ico')

#if os.path.isfile('gcode2cutsim.exe'):
#    os.remove('gcode2cutsim.exe')

shutil.copy('dist\\paramGuard.exe', 'D:\\MWAdditive\\paramGuard.exe')
