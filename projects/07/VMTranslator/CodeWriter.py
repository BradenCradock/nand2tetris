import os
import re
class CodeWriter:

    def __init__(self, filePath):

        self.file = open(filePath.split(".")[0] + ".asm","w+")
        self.fileName = os.path.basename(filePath).split(".")[0]
        self.filePath = filePath.split(".")[0] + ".asm"


    #Informs the code writer that the translation of a new VM file is started.
    def setFileName(self, fileName):

        self.fileName = fileName + ".asm"

    def closeFile(self):
        self.file.close()
        os.rename(self.filePath, self.filePath[:self.filePath.rindex("/")] + "/" + self.fileName)
