import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ----------------------------------------------------------------------------------------------------------------------
class ParamEventHandler(FileSystemEventHandler):
    def __init__(self, pluginPath, corePath, PG_UI):
        self.PG_UI = PG_UI

    def on_modified(self, event):
        src_path = event.src_path
        etype = event.event_type

        if etype == 'modified' and src_path.split('\\')[-1] == 'Mesh.ini':
            print 'Config file was modified. Updating UI.'
            self.PG_UI.refresh_UI()


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
