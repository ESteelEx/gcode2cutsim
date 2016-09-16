import sys, os, threading, zipfile, shutil


def package_flist():
    package = {}
    package['calc_core'] = 'mwAdditive3DPrinter.exe'
    package['simulation_core'] = 'gcode2cutsimFDM.exe'
    package['workpiece'] = 'Mesh.stl'
    package['simulation_file'] = 'Mesh.cl'
    package['gcode'] = 'Mesh.gcode'
    package['build_space'] = 'Default.3dm'
    package['config_file'] = 'Mesh.ini'

    return package


class MWPackager(threading.Thread):
    def __init__(self, corePath, pluginPath):
        self.pluginPath = pluginPath
        self.corePath = corePath
        threading.Thread.__init__(self)

    # ------------------------------------------------------------------------------------------------------------------
    def copy_core(self):
        sys.path.append(self.pluginPath)
        package = package_flist()
        print 'creating archive'
        zf = zipfile.ZipFile(self.corePath + r'\MW_Package.mw3D', mode='w')
        for key, file in package.iteritems():
            try:
                print 'Adding ' + key + ' - ' + file
                zf.write(self.corePath + r'\\' + file)
            except:
                print 'something went wrong'
                zf.close()

        print 'closing file.'
        zf.close()
        print 'MW Package stored.'
        print 'FINISHED'
