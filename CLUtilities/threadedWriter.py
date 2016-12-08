import threading


class threadedWriter(threading.Thread):
    def __init__(self, content, startPoint=0, linePos=0, threadCount=1, THList=[]):
        self.MAX_LINES_THREAD = 40000
        self.THList = THList
        self.linePos = linePos
        self.nextStartPoint = threadCount * self.MAX_LINES_THREAD
        self.content = content
        self.threadCount = threadCount
        self.EOF = False
        threading.Thread.__init__(self)

    # ------------------------------------------------------------------------------------------------------------------
    def run(self):
        if self.nextStartPoint <= len(self.content):
            self.openTHBlock()
            self.readBlock()
            self.closTHBlock()

    # ------------------------------------------------------------------------------------------------------------------
    def readBlock(self):
        for i in range(self.MAX_LINES_THREAD):
            try:
                line = self.content[self.threadCount * self.MAX_LINES_THREAD + i]
                self.writeBlock(line)
                self.linePos = self.threadCount * self.MAX_LINES_THREAD + i
            except:
                self.EOF = True

    # ------------------------------------------------------------------------------------------------------------------
    def openTHBlock(self):
        self.TCfname = r'C:\MW3D\TC\threadCache' + str(self.threadCount) + '.mwtc'
        self.TCfh = open(self.TCfname, 'w')
        self.THList.append(self.TCfname)

    # ------------------------------------------------------------------------------------------------------------------
    def closTHBlock(self):
        self.TCfh.close()

    # ------------------------------------------------------------------------------------------------------------------
    def writeBlock(self, line):
        self.TCfh.write(line)
