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
    def __init__(self, pluginPath, corePath, UIs):
        self.pluginPath = pluginPath
        self.corePath = corePath
        self.UIs = UIs
        self.no_action_list = ['collapse']
        print UIs.TS
        self.TS = UIs.TS

    def on_modified(self, event):
        src_path = event.src_path
        etype = event.event_type

        try:
            print 'Changed ' + str(self.UIs.GOC.param_changed) + ' ...'

            if self.UIs.GOC.param_changed not in self.no_action_list:
                if etype == 'modified' and src_path.split('\\')[-1] == 'Mesh.ini':
                    try:
                        self.UIs.GOC.inject_param_changed(None) # reset to no changes
                        self.UIs.refresh_UI()
                        SLICE = slice.slicer(None, self.pluginPath, self.corePath)
                        self.UIs.param_dict['SLICER']['firstLayerHeight'][1]['headline'].SetForegroundColour(UI.TWARNING['FG'])
                        self.UIs.param_dict['SLICER']['firstLayerHeight'][1]['headline'].Hide()
                        self.UIs.param_dict['SLICER']['firstLayerHeight'][1]['headline'].Show()
                        self.TS.slicer_working(True)
                        result = SLICE.slicing()
                        self.TS.slicer_working(False)
                        if result:
                            self.UIs.param_dict['SLICER']['firstLayerHeight'][1]['headline'].SetForegroundColour(UI.TOK['FG'])

                            print 'Finished slicing'
                            # When slicing finished slicer created a new g-code file.
                            # We parse the cl file in background so we are able to start simulation
                            # without starting the parser in the beginning
                            print 'Precalculating simulation file'
                            self.UIs.param_dict['SIMULATION']['precision'][1]['headline'].SetForegroundColour(
                                UI.TWARNING['FG'])
                            self.UIs.param_dict['SIMULATION']['precision'][1]['headline'].Hide()
                            self.UIs.param_dict['SIMULATION']['precision'][1]['headline'].Show()
                            RS = runSimulation.runSimulation(self.corePath, self.pluginPath, silent=True)
                            RS.execute()
                            self.UIs.param_dict['SIMULATION']['precision'][1]['headline'].SetForegroundColour(
                                UI.TOK['FG'])
                            self.UIs.param_dict['SIMULATION']['precision'][1]['headline'].Hide()
                            self.UIs.param_dict['SIMULATION']['precision'][1]['headline'].Show()
                            print 'DONE'

                        else:
                            self.UIs.param_dict['SLICER']['firstLayerHeight'][1]['headline'].SetForegroundColour(UI.TERROR['FG'])

                        self.UIs.param_dict['SLICER']['firstLayerHeight'][1]['headline'].Hide()
                        self.UIs.param_dict['SLICER']['firstLayerHeight'][1]['headline'].Show()


                    except:
                        pass

            self.UIs.GOC.inject_param_changed(None)
        except:
            pass


# ----------------------------------------------------------------------------------------------------------------------
class guard_of_changes(threading.Thread):
    def __init__(self, UIs):
        self.pluginPath = UIs.pluginPath
        self.corePath = UIs.corePath
        self.runstat = True
        self.UIs = UIs
        self.param_changed = None
        threading.Thread.__init__(self)

    # ------------------------------------------------------------------------------------------------------------------
    def run(self):
        event_handler = ParamEventHandler(self.pluginPath, self.corePath, self.UIs) # start class that handles the event
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