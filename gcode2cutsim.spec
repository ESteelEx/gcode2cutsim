import shutil, psutil, os

for proc in psutil.process_iter():
    try:
        if proc.name() == 'gcode2cutsim.exe':
            try:
                proc.kill()
            except:
                pass
    except:
        pass

# -*- mode: python -*-
a = Analysis(['gcode2cutsim.py'],
                pathex=['.'],
                hiddenimports=['appdirs', 'six', 'packaging', 'packaging.version', 'packaging.specifiers', 'packaging.requirements'],
                hookspath=None,
                runtime_hooks=None)

if os.path.isfile('cacert.pem'):
    a.datas.append(('cacert.pem', 'cacert.pem', 'DATA'))

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
    name=os.path.join('dist', 'gcode2cutsim.exe'),
    debug=False,
    strip=None,
    upx=True,
    console=True,
    icon='bin\\images\\3dPrintVer.ico')

if os.path.isfile('gcode2cutsimFDM.exe'):
    os.remove('gcode2cutsimFDM.exe')

shutil.copy('dist\\gcode2cutsim.exe', 'gcode2cutsimFDM.exe')
shutil.copy('gcode2cutsimFDM.exe', 'D:\\MW3DPrinting_MachSim\\gcode2cutsimFDM.exe')