#######################################################################################################################
# String manipulator
########################################################################################################################
__author__ = 'Mathias Rohler'
__version__= 1.0


class StrManipulator:
    def __init__(self):
        pass

    # ----------------------------------------------------------------------------------------------------------------------
    def sepStr(self, line, char):
        """delete a string from a string. Starting with char and ends with white space"""
        posChar = line.find(char)
        if posChar == -1:
            return line

        if posChar != None:
            for i in range(posChar, len(line)):
                if line[i:i+1] == ' ' or i == len(line)-1:
                    line = line[:posChar] + line[i+1:]
                    break

        return line

    # ------------------------------------------------------------------------------------------------------------------
    def insertWS(self, line, char):
        """inserts a white space after user given character"""
        posChar = line.find(char)
        line = line[:posChar+1] + ' ' + line[posChar+1:]

        return line

    # ------------------------------------------------------------------------------------------------------------------
    def insertChar(self, line, char, insertChar):
        """inserts a user given character after user given character"""
        posChar = line.find(char)
        if posChar != -1:
            line = line[:posChar+1] + insertChar + line[posChar+1:]

        return line

    # ------------------------------------------------------------------------------------------------------------------
    def vartype(self, line, char, vartype):
        """inserts a user given character after user given character"""
        posChar = line.find(char)
        if posChar != -1:
            if vartype == 'int':
                line = line[:posChar + 1] + str(int(float(line[posChar + 1:])))

        return line