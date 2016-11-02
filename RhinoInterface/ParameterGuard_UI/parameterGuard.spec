import os
import sys
import shutil, psutil
from PyInstaller.building.api import PYZ, EXE, COLLECT
from PyInstaller.building.build_main import Analysis
from PyInstaller.building.datastruct import TOC
from multiprocessing import Queue

# append current directory
sys.path.append(os.getcwd())
# from config import options

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
# , 'watchdog'
a = Analysis(['parameterGuard.py'],
              pathex=['.'], 
              hiddenimports=['guard', 'watchdog', 'multiprocessing'],
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

shutil.copy('dist\\paramGuard.exe', 'C:\\MWAdditive\\paramGuard.exe')
