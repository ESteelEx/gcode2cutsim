
class interruptThreads:
    def __init__(self, tr):
        self.threads = tr

    def kill(self):
        print self.threads
        try:
            for thread in self.threads:
                print 'Trying to interrupt Thread: ' + str(thread)
                thread.inject_runstat(False)
        except:
            pass