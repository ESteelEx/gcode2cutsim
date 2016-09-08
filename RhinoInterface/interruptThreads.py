
class interruptThreads:
    def __init__(self, tr):
        self.threads = tr

    def kill(self):
        print self.threads
        for thread in self.threads:
            try:
                print 'Trying to interrupt Thread: ' + str(thread)
                thread.inject_runstat(False)
                print 'Killed ' + str(thread)
            except:
                print 'Cannot kill ' + str(thread)
