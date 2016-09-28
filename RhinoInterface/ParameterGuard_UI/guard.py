import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from RhinoInterface import slice
from RhinoInterface.ParameterGuard_UI import UI_settings as UI
from RhinoInterface import addPoints

# ----------------------------------------------------------------------------------------------------------------------
class ParamEventHandler(FileSystemEventHandler):
    def __init__(self, pluginPath, corePath, PG_UI):
        self.pluginPath = pluginPath
        self.corePath = corePath
        self.PG_UI = PG_UI

    def on_modified(self, event):
        src_path = event.src_path
        etype = event.event_type

        if etype == 'modified' and src_path.split('\\')[-1] == 'Mesh.ini':
            try:
                self.PG_UI.refresh_UI()
                SLICE = slice.slicer(None, self.pluginPath, self.corePath)
                print 'Started slicer'
                self.PG_UI.param_dict['SLICER']['firstLayerHeight'][1]['headline'].SetForegroundColour(UI.TERROR['FG'])
                self.PG_UI.param_dict['SLICER']['firstLayerHeight'][1]['headline'].Hide()
                self.PG_UI.param_dict['SLICER']['firstLayerHeight'][1]['headline'].Show()
                SLICE.slicing()
                self.PG_UI.param_dict['SLICER']['firstLayerHeight'][1]['headline'].SetForegroundColour(UI.TCOLOR['FG'])
                self.PG_UI.param_dict['SLICER']['firstLayerHeight'][1]['headline'].Hide()
                self.PG_UI.param_dict['SLICER']['firstLayerHeight'][1]['headline'].Show()
                print 'finished slicing'
            except:
                pass

# ----------------------------------------------------------------------------------------------------------------------
class guard_of_changes(threading.Thread):
    def __init__(self, PG_UI):
        self.pluginPath = PG_UI.pluginPath
        self.corePath = PG_UI.corePath
        self.runstat = True
        self.PG_UI = PG_UI
        threading.Thread.__init__(self)

    # ------------------------------------------------------------------------------------------------------------------
    def run(self):
        event_handler = ParamEventHandler(self.pluginPath, self.corePath, self.PG_UI) # start class that handles the event
        observer = Observer()
        observer.schedule(event_handler, self.corePath, recursive=True)
        observer.start()

        while self.runstat:
            time.sleep(1)

        observer.stop()
        observer.join()

        print '--|X|-- GUARD unplugged'

    # ------------------------------------------------------------------------------------------------------------------
    def inject_runstat(self, runstat):
        self.runstat = runstat
