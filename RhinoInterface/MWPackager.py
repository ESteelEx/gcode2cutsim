try:
    import rhinoscriptsyntax as rs
except:
    print 'You have to execute this script inside Rhino environment'

import sys, os, threading, zipfile, shutil
import adjustINI
reload(adjustINI)


# ----------------------------------------------------------------------------------------------------------------------
def package_flist():
    package = {}
    #package['calc_core'] = 'mwAdditive3DPrinter.exe'
    #package['simulation_core'] = 'gcode2cutsimFDM.exe'
    package['workpiece'] = 'Mesh.stl'
    package['simulation_file_AddSim'] = 'Mesh.cl'
    package['simulation_file_MachSim'] = 'Mesh.sim'
    package['gcode'] = 'Mesh.gcode'
    package['build_space'] = 'buildspace.3dm'
    package['config_file'] = 'Mesh.ini'

    return package



class MWPackager(threading.Thread):
    def __init__(self, pluginPath, corePath, command='save'):
        self.pluginPath = pluginPath
        self.corePath = corePath
        self.cachePath = 'Cache'
        self.command = command
        threading.Thread.__init__(self)

    # ------------------------------------------------------------------------------------------------------------------
    def run(self):
        if self.command == 'save':
            self.copy_core()
        else:
            self.load_package()

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

            rs.Command('_-SaveAs ' + self.corePath + '\\' + package['build_space'])

            zf = zipfile.ZipFile(fileName, mode='w')
            for key, file in package.iteritems():
                file_abs = self.corePath + '\\' + file
                if os.path.isfile(file_abs):
                    try:
                        print 'Adding ' + key + ' - ' + file
                        zf.write(file_abs, arcname=file, compress_type=zipfile.ZIP_DEFLATED)
                    except:
                        print 'Something went wrong while zipping'
                        zf.close()
                else:
                    print 'File not found: ' + str(file)

            print 'Closing package'
            zf.close()
            # if os.path.isfile(package['build_space']):
            #     print 'Removing TMP data ...'
            #     os.remove(package['build_space'])

            print 'MW Package stored.'
            print 'FINISHED'

    # ------------------------------------------------------------------------------------------------------------------
    def load_package(self):
        sys.path.append(self.pluginPath)
        fileName = rs.OpenFileName(title='Enter or select MW 3D package', filter='MW3D|*.mw3D', extension='mw3D')

        if fileName is not None:
            packageFileNames = []

            try:
                fh = open(fileName, 'rb')
                z = zipfile.ZipFile(fh)
                for name in z.namelist():
                    packageFileNames.append(name.split('/')[-1])
                    outputPath = name.split('/')[:-1]
                    if len(outputPath) == 0:
                        outputPath = ['']
                    packageFolder = fileName.split('\\')[-1].split('.')[0]
                    extractionPath = self.corePath + '\\' + self.cachePath + '\\' + packageFolder + '\\' + outputPath[0]

                    print 'Extracting : ' + packageFolder + '\\' + name

                    if not os.path.isdir(extractionPath):
                        os.mkdir(extractionPath)

                    outfile = open(self.corePath + '\\' + self.cachePath + '\\' + packageFolder + '\\' + name, 'wb')
                    outfile.write(z.read(name))
                    outfile.close()

                fh.close()

                # load buildspace with workpiece and tool path etc.
                for file in packageFileNames:
                    if file.split('.')[-1] == '3dm':
                        rs.Command(r'_-Open ' + extractionPath + r'/' + file +
                                   r' N ' +
                                   extractionPath + r'/' + file + r' _Enter')

                # copy settings to core
                for file in packageFileNames:
                    if file.split('.')[-1] == 'stl' or file.split('.')[-1] == 'ini' or  \
                                    file.split('.')[-1] == 'cl' or file.split('.')[-1] == 'gcode':

                        shutil.copy(extractionPath + '\\' + file,
                                    self.corePath + '\\' + file)

                print 'Adjusting INI File ...'
                AI = adjustINI.adjustINI(self.pluginPath, self.corePath)
                AI.adjust_abs_folder()

                print 'FINISHED'

            except:
                print 'ERROR. Could not open MW3D package.'



