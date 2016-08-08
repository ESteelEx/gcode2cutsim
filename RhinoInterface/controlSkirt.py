import sys

sys.path.append(r'C:\Users\ModuleWoks\Documents\Development\GitRep\gcode2cutsim')

import rhinoscriptsyntax as rs
from Utilities import ini_worker

reload(ini_worker)

INI_CONFIG = r'C:\StoreDaily\Mesh.ini'

section_params = ini_worker.get_section_from_ini(INI_CONFIG, 'SKIRT')

for key, value in section_params.iteritems():
    if key == 'create':
        if int(value) == 0:
            print 'SKIRT SWITCHED TO ON'
            ini_worker.write_to_section(INI_CONFIG, 'SKIRT', 'create', 1)
        else:
            print 'SKIRT SWITCHED TO OFF'
            ini_worker.write_to_section(INI_CONFIG, 'SKIRT', 'create', 0)


