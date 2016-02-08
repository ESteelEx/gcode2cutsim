import traceback, sys

source = raw_input(">>> ")
try:
    exec source in envdir
except:
    print "Exception in user code:"
    print '-'*60
    message = traceback.print_exc(file=sys.stdout)
    message = str(message)
    print message
    print '-'*60