import psutil


# ----------------------------------------------------------------------------------------------------------------------
def terminate(prog='mwAdditive3DPrinter.exe'):
    # proof if an instance of slicer is already running.
    # slicer will be terminated to avoid a second instance running and writing to the same file.
    for proc in psutil.process_iter():
        print proc
        try:
            if proc.name() == prog:
                print 'SLICER RUNNING. LETS END THIS PROCESS FIRST'
                proc.kill()
                print 'DONE'
            else:
                print 'PROG DID NOT MATCH'
        except:
            print 'THIS DID NOT WORK'

if __name__ == '__main__':
    terminate()