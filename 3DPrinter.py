#!/usr/bin/env python
# sysTrayIcon.py
# main script

import sys, os
import win32com.shell.shell as shell
import win32con

__author__ = 'mathiasr'


# ----------------------------------------------------------------------------------------------------------------------
def start_3DPrintJob():
    print 'starting printer job'
    command = '3DPrintModule/mw3DPrinter.exe'
    params = ''
    abscommand = os.path.abspath(command)
    shell.ShellExecuteEx(nShow=win32con.SW_SHOWNORMAL, lpFile=abscommand, lpParameters=params)

# ----------------------------------------------------------------------------------------------------------------------
def main():

    if len(sys.argv) == 1:
        print 'no input. EXIT. Starting with config.ini'
        start_3DPrintJob()
    else:
        if not os.path.isfile(sys.argv[1]):
            print 'no such STL file -> ' + str(sys.argv[1])
            return

# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()