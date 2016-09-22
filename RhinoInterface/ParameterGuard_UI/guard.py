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
            self.PG_UI.editbox[0].SetValue('Hey')


# ----------------------------------------------------------------------------------------------------------------------
class guard_of_changes(threading.Thread):
    def __init__(self, pluginPath, corePath, PG_UI):
        self.pluginPath = pluginPath
        self.corePath = corePath
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
            try:
                self.PG_UI.editbox[0]
            except:
                self.runstat = False

        observer.stop()
        observer.join()

        print 'CHIAO'

    # ------------------------------------------------------------------------------------------------------------------
    def inject_runstat(self, runstat):
        self.runstat = runstat
