import sys, threading, time


# ----------------------------------------------------------------------------------------------------------------------
class ParamEventHandler(FileSystemEventHandler):
    def __init__(self, pluginPath, corePath, PG_UI):
        self.pluginPath = pluginPath
        self.corePath = corePath
        self.PG_UI = PG_UI

    # ------------------------------------------------------------------------------------------------------------------
    def on_modified(self, event):
        src_path = event.src_path
        etype = event.event_type

        if etype == 'modified' and src_path.split('\\')[-1] == 'Mesh.gcode':
            print 'gcode changed'
            AP = addPoints.addPoints(self.pluginPath, self.corePath)
            AP.start()


class gcodeGuard(threading.Thread):
    def __init__(self, pluginPath, corePath):
        self.pluginPath = pluginPath
        self.corePath = corePath
        self.runstat = True
        threading.Thread.__init__(self)

    # ------------------------------------------------------------------------------------------------------------------
    def run(self):
        sys.path.append(self.pluginPath)
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler

        event_handler = ParamEventHandler(self.pluginPath, self.corePath, self.PG_UI) # start class that handles the event
        observer = Observer()
        observer.schedule(event_handler, self.corePath, recursive=True)
        observer.start()

        while self.runstat:
            time.sleep(1)

        observer.stop()
        observer.join()

        print '--|X|-- GCODE GUARD unplugged'

    # ------------------------------------------------------------------------------------------------------------------
    def inject_runstat(self, runstat):
        self.runstat = runstat