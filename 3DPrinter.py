#!/usr/bin/env python
# sysTrayIcon.py
# main script

import sys, os
import win32com.shell.shell as shell
import win32con, win32event

__author__ = 'mathiasr'


# ----------------------------------------------------------------------------------------------------------------------
def start_3DPrintJob():
    print 'starting printer job'
    command = '3DPrintModule/mw3DPrinter.exe'
    params = ''
    abscommand = os.path.abspath(command)
    dict = shell.ShellExecuteEx(nShow=win32con.SW_SHOWNORMAL, lpFile=abscommand, lpParameters=params)

    hh = dict['hProcess']
    print hh
    ret = win32event.WaitForSingleObject(hh, -1)
    print ret

# ----------------------------------------------------------------------------------------------------------------------
def main():

    if len(sys.argv) == 1:
        print 'no input. EXIT. Starting with config.ini'
        start_3DPrintJob()
    else:
        if not os.path.isfile(sys.argv[1]):
            print 'no such STL file -> ' + str(sys.argv[1])
            return

    print 'DONE'

# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()