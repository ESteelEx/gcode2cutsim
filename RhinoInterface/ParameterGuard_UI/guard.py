import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ----------------------------------------------------------------------------------------------------------------------
class ParamEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        #keys = event.key
        # isdir = event.is_directory
        src_path = event.src_path
        etype = event.event_type

        if etype == 'modified' and src_path.split('\\')[-1] == 'Mesh.ini':
            print 'Config file was modified. Updating UI.'


# ----------------------------------------------------------------------------------------------------------------------
class guard_of_changes(threading.Thread):
    def __init__(self, pluginPath, corePath):
        self.pluginPath = pluginPath
        self.corePath = corePath
        self.runstat = True
        threading.Thread.__init__(self)

    # ------------------------------------------------------------------------------------------------------------------
    def run(self):
        event_handler = ParamEventHandler() # start class that handles the event
        observer = Observer()
        observer.schedule(event_handler, self.corePath, recursive=True)
        observer.start()

        while self.runstat:
            time.sleep(1)

        observer.stop()
        observer.join()

        print 'CHIAO'

    # ------------------------------------------------------------------------------------------------------------------
    def inject_runstat(self, runstat):
        self.runstat = runstat
