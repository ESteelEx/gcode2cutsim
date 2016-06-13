import shutil, psutil

for proc in psutil.process_iter():
    try:
        if proc.name() == '3DPrinter.exe':
            try:
                proc.kill()
            except:
                pass
    except:
        pass

# -*- mode: python -*-
a = Analysis(['3DPrinter.py'],
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
    name=os.path.join('dist', '3DPrinter.exe'),
    debug=False, 
    strip=None, 
    upx=True, 
    console=True )
    # icon='dat\\images\\icon.ico' )

if os.path.isfile('3DPrinter.exe'):
    os.remove('3DPrinter.exe')
    shutil.copy('dist\\3DPrinter.exe', '3DPrinter.exe')
else:
    shutil.copy('dist\\3DPrinter.exe', '3DPrinter.exe')