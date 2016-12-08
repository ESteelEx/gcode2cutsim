import threading, time
import shutil
from CLUtilities import threadedWriter


MAX_THREADS = 15
TW = []

start = time.time()

fh = open(r'C:\MW3D\Mesh.gcode')
content = fh.readlines()

print 'lines: ' + str(len(content))

end = time.time()

print str(end - start) + ' sec'

time.sleep(1)


# ----------------------------------------------------------------------------------------------------------------------
start = time.time()
j = 0
jj = 0
SLfh = open(r'C:\MW3D\singleLoop.txt', 'w')
for i in content:
    SLfh.write(i)

SLfh.close()

end = time.time()

deltaSingle = end - start

print str(end - start) + ' sec'

time.sleep(1)


# ----------------------------------------------------------------------------------------------------------------------
start = time.time()
TWList = []
while 1:
    if threading.active_count() <= MAX_THREADS:
         if len(TW) == 0:
            TW.append(threadedWriter.threadedWriter(content))
         else:
            if TW[-1].nextStartPoint <= len(content):
                if not TW[-1].EOF:
                    TW.append(threadedWriter.threadedWriter(content,
                                                            startPoint=TW[-1].nextStartPoint,
                                                            threadCount=len(TW),
                                                            THList=TW[-1].THList))
                else:
                    break
            try:
                TW[-1].start()
                print TW[-1].THList
            except:
                TWList = TW[-1].THList
                break

# concartenate

print TW[-1].THList

concfh = open(r'C:\MW3D\TC\Mesh.test', 'w')
while 1:
    active_threads = threading.active_count()
    if active_threads <= len(TW[-1].THList):
        TW[-1].THList = TW[-1].THList.pop(-1)
        print len(TW[-1].THList)
        for f in TW[-1].THList:
            with open(f, 'rb') as fd:
                shutil.copyfileobj(fd, concfh, 1024*1024*10)

    if len(TW[-1].THList) == 0:
        break

end = time.time()

deltaThread = end - start

if deltaSingle > deltaThread:
    print str(deltaSingle / deltaThread) + ' times faster'
else:
    print str(deltaThread / deltaSingle) + ' times slower'

print str(end - start) + ' sec - in ' + str(len(TW)) + ' threads'


