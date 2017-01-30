import sys, shutil

# append current directory
sys.path.append(os.getcwd())
# from config import options


# -*- mode: python -*-
# , 'watchdog'
a = Analysis(['terminate.py'],
              pathex=['.'],
              hiddenimports=['Queue', 'multiprocessing.Queue', 'queuelib', 'queuelib.queue', 'queue', 'queue.Queue', 'guard', 'watchdog', 'multiprocessing', 'appdirs', 'six', 'packaging', 'packaging.version', 'packaging.specifiers', 'packaging.requirements'],
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
    name=os.path.join('dist', 'terminator.exe'),
    debug=False,
    strip=None,
    upx=True,
    console=False)

terminator_loc_file = 'terminator.exe'
terminator_loc_path = 'C:\\MW3D_07\\'

if os.path.isfile(terminator_loc_path + terminator_loc_file):
    try:
        os.remove(terminator_loc_path + terminator_loc_file)
        shutil.copy('dist\\terminator.exe', terminator_loc_path + terminator_loc_file)
    except:
        print 'Could not find exe. Investigate the source'