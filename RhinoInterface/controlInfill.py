import sys

sys.path.append(r'C:\Users\ModuleWoks\Documents\Development\GitRep\gcode2cutsim')

import rhinoscriptsyntax as rs
from Utilities import ini_worker

reload(ini_worker)

INI_CONFIG = r'D:\StoreDaily\Mesh.ini'

section_params = ini_worker.get_section_from_ini(INI_CONFIG, 'INFILL')

for key, value in section_params.iteritems():
    if key == 'cross':
        if int(value) == 0:
            print 'INFILL PATTERN SWITCHHED TO CROSS'
            ini_worker.write_to_section(INI_CONFIG, 'INFILL', 'cross', 1)
        else:
            print 'INFILL PATTERN SWITCHHED TO PARALLEL'
            ini_worker.write_to_section(INI_CONFIG, 'INFILL', 'cross', 0)