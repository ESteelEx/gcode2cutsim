import time
import threading
from RhinoInterface import runSimulation
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
        self.no_action_list = ['collapse']

    def on_modified(self, event):
        src_path = event.src_path
        etype = event.event_type

        try:
            print 'Changed ' + str(self.PG_UI.GOC.param_changed) + ' ...'

            if self.PG_UI.GOC.param_changed not in self.no_action_list:
                if etype == 'modified' and src_path.split('\\')[-1] == 'Mesh.ini':
                    try:
                        self.PG_UI.GOC.inject_param_changed(None) # reset to no changes
                        self.PG_UI.refresh_UI()
                        SLICE = slice.slicer(None, self.pluginPath, self.corePath)
                        print 'Started slicer'
                        self.PG_UI.param_dict['SLICER']['firstLayerHeight'][1]['headline'].SetForegroundColour(UI.TWARNING['FG'])
                        self.PG_UI.param_dict['SLICER']['firstLayerHeight'][1]['headline'].Hide()
                        self.PG_UI.param_dict['SLICER']['firstLayerHeight'][1]['headline'].Show()
                        result = SLICE.slicing()
                        if result:
                            self.PG_UI.param_dict['SLICER']['firstLayerHeight'][1]['headline'].SetForegroundColour(UI.TOK['FG'])

                            print 'Finished slicing'
                            # When slicing finished slicer created a new g-code file.
                            # We parse the cl file in background so we are able to start simulation
                            # without starting the parser in the beginning
                            print 'Precalculating simulation file'
                            self.PG_UI.param_dict['SIMULATION']['precision'][1]['headline'].SetForegroundColour(
                                UI.TWARNING['FG'])
                            self.PG_UI.param_dict['SIMULATION']['precision'][1]['headline'].Hide()
                            self.PG_UI.param_dict['SIMULATION']['precision'][1]['headline'].Show()
                            RS = runSimulation.runSimulation(self.corePath, self.pluginPath, silent=True)
                            RS.execute()
                            self.PG_UI.param_dict['SIMULATION']['precision'][1]['headline'].SetForegroundColour(
                                UI.TOK['FG'])
                            self.PG_UI.param_dict['SIMULATION']['precision'][1]['headline'].Hide()
                            self.PG_UI.param_dict['SIMULATION']['precision'][1]['headline'].Show()
                            print 'DONE'

                        else:
                            self.PG_UI.param_dict['SLICER']['firstLayerHeight'][1]['headline'].SetForegroundColour(UI.TERROR['FG'])

                        self.PG_UI.param_dict['SLICER']['firstLayerHeight'][1]['headline'].Hide()
                        self.PG_UI.param_dict['SLICER']['firstLayerHeight'][1]['headline'].Show()


                    except:
                        pass

            self.PG_UI.GOC.inject_param_changed(None)
        except:
            pass


# ----------------------------------------------------------------------------------------------------------------------
class guard_of_changes(threading.Thread):
    def __init__(self, PG_UI):
        self.pluginPath = PG_UI.pluginPath
        self.corePath = PG_UI.corePath
        self.runstat = True
        self.PG_UI = PG_UI
        self.param_changed = None
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

        print '--|X|-- MAIN GUARD unplugged'

    # ------------------------------------------------------------------------------------------------------------------
    def inject_runstat(self, runstat):
        self.runstat = runstat

    # ------------------------------------------------------------------------------------------------------------------
    def inject_param_changed(self, param_changed):
        self.param_changed = param_changed