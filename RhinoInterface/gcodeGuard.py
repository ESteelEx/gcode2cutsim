import os, sys, threading, time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ----------------------------------------------------------------------------------------------------------------------
class ParamEventHandler(FileSystemEventHandler):
    def __init__(self, pluginPath, corePath):
        self.pluginPath = pluginPath
        self.corePath = corePath

    # ------------------------------------------------------------------------------------------------------------------
    def on_modified(self, event):
        import addPoints
        src_path = event.src_path
        etype = event.event_type

        if etype == 'modified' and src_path.split('\\')[-1] == 'Mesh.gcode':
            print 'gcode changed'
            AP = addPoints.addPoints(self.pluginPath, self.corePath)
            AP.flush_data()

# ----------------------------------------------------------------------------------------------------------------------
class gcodeGuard(threading.Thread):
    def __init__(self, pluginPath, corePath):
        self.pluginPath = pluginPath
        self.corePath = corePath
        self.runstat = True
        self.FileSystemEventHandler = None
        threading.Thread.__init__(self)

    # ------------------------------------------------------------------------------------------------------------------
    def run(self):
        sys.path.append(self.pluginPath)

        event_handler = ParamEventHandler(self.pluginPath, self.corePath)  # start class that handles the event
        observer = Observer()
        observer.schedule(event_handler, self.corePath, recursive=True)
        observer.start()

        #while self.runstat:
        #    pass
            # time.sleep(5)

        #observer.stop()
        #observer.join()

        print '--|X|-- GCODE GUARD unplugged'

    # ------------------------------------------------------------------------------------------------------------------
    def inject_runstat(self, runstat):
        self.runstat = runstat

