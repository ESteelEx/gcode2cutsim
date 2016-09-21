try:
    import rhinoscriptsyntax as rs
except:
    pass

import sys, os, threading, zipfile, shutil

# ------------------------------------------------------------------------------------------------------------------
def package_flist():
    package = {}
    package['calc_core'] = 'mwAdditive3DPrinter.exe'
    package['simulation_core'] = 'gcode2cutsimFDM.exe'
    package['workpiece'] = 'Mesh.stl'
    package['simulation_file'] = 'Mesh.cl'
    package['gcode'] = 'Mesh.gcode'
    package['build_space'] = 'buildspace.3dm'
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

        print 'Creating archive ...'
        fileName = rs.SaveFileName(title='Enter or select MW 3D package', filter='MW3D|*.mw3D', extension='mw3D')

        if fileName is not None:

            print 'Packing archive to -> ' + fileName

            print 'Preparing buildspace ...'
            if os.path.isfile(package['build_space']):
                os.remove(package['build_space'])

            rs.Command('_-SaveAs ' + package['build_space'])

            zf = zipfile.ZipFile(fileName, mode='w')
            for key, file in package.iteritems():
                try:
                    print 'Adding ' + key + ' - ' + file
                    zf.write(self.corePath + r'\\' + file)
                except:
                    print 'Something went wrong'
                    zf.close()

            print 'closing file.'
            zf.close()
            # if os.path.isfile(package['build_space']):
            #     print 'Removing TMP data ...'
            #     os.remove(package['build_space'])

            print 'MW Package stored.'
            print 'FINISHED'

    # ------------------------------------------------------------------------------------------------------------------
    def load_package(self):

        fileName = rs.OpenFileName(title='Enter or select MW 3D package', filter='MW3D|*.mw3D', extension='mw3D')

        if fileName is not None:

            packageFileNames = []

            try:
                fh = open(fileName, 'rb')
                z = zipfile.ZipFile(fh)
                for name in z.namelist():
                    packageFileNames.append(name.split('/')[-1])
                    outputPath = name.split('/')[:-1]
                    packageFolder = fileName.split('\\')[-1].split('.')[0]
                    extractionPath = self.corePath + '\\' + packageFolder + '\\' + outputPath[0]

                    print 'Extracting to : ' + packageFolder + '\\' + name

                    if not os.path.isdir(extractionPath):
                        os.mkdir(extractionPath)

                    print packageFolder + '\\' + name

                    outfile = open(self.corePath + '\\' + packageFolder + '\\' + name, 'wb')
                    outfile.write(self.corePath + '\\' + packageFolder + '\\' + z.read(name))
                    outfile.close()
                fh.close()

                for file in packageFileNames:
                    if file.split('.')[-1] == '3dm':
                        rs.Command(r'_-Open ' + extractionPath + r'/' + file +
                                   r' N ' +
                                   extractionPath + r'/' + file + r' _Enter')

                print 'FINISHED'

            except:
                print 'ERROR. Could not open MW3D package.'
                raise



