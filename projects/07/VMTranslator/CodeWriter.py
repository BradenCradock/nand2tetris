import os
import re
import Parser
class CodeWriter:

    def __init__(self, filePath):

        self.file = open(filePath.split(".")[0] + ".asm","w+")
        self.filePath = filePath.split(".")[0] + ".asm"
        self.fileName = os.path.basename(self.filePath)
        self.compareCounter = 0

    #Informs the code writer that the translation of a new VM file is started.
    def setFileName(self, fileName):
        self.fileName = fileName + ".asm"

    def unaryOp(self, operation):
        asmInstr =  "@SP\n" +\
                    "AM = M - 1\n" +\
                    "M ="  + operation + "M\n" +\
                    "@SP\n" +\
                    "M = M + 1\n"
        return asmInstr

    def binaryOp(self, operation):
        asmInstr =  "@SP\n" +\
                    "AM = M - 1\n" +\
                    "D = M\n" +\
                    "@SP\n" +\
                    "AM = M - 1\n" +\
                    "M = M " + operation + " D\n" +\
                    "@SP\n" +\
                    "M = M + 1\n"
        return asmInstr

    def compareOp(self, command):

        asmInstr =  "@SP\n" +\
                    "AM = M - 1\n" +\
                    "D = M\n" +\
                    "@SP\n" +\
                    "AM = M - 1\n" +\
                    "D = D - M\n" +\
                    "@PASS" + str(self.compareCounter) + "\n" +\
                    "D;J" + command.upper() + "\n" +\
                    "D = -1\n" +\
                    "@END" + str(self.compareCounter) + "\n" +\
                    "0;JMP\n" +\
                    "(PASS" + str(self.compareCounter) + ")\n" +\
                    "@SP\n" +\
                    "D = 0\n" +\
                    "(END" + str(self.compareCounter) + ")\n" +\
                    "@SP\n" +\
                    "A = M\n" +\
                    "M = D\n" +\
                    "@SP\n" +\
                    "M = M + 1\n"

        self.compareCounter += 1
        return asmInstr

    #Writes the assembly code that is the translation of the given arithmetic command.
    def writeArithmetic(self, command):
        asmInstr = {}
        if command == "add":
            asmInstr = self.binaryOp("+")

        elif command == "sub":
            asmInstr = self.binaryOp("-")

        elif command == "neg":
            asmInstr = self.unaryOp("-")

        elif command == "eq":
            asmInstr = self.binaryOp("+")

        elif command == "gt":
            asmInstr = self.compareOp(command)

        elif command == "lt":
            asmInstr = self.compareOp(command)

        elif command == "or":
            asmInstr = self.binaryOp("|")

        elif command == "and":
            asmInstr = self.binaryOp("&")

        elif command == "not":
            asmInstr = self.unaryOp("!")

        self.file.write(asmInstr)

    def closeFile(self):
        self.file.close()
        try:
            os.rename(self.filePath, self.filePath[:self.filePath.rindex("/")] + "/" + self.fileName)
        except WindowsError:
            os.remove(self.filePath[:self.filePath.rindex("/")] + "/" + self.fileName)
            os.rename(self.filePath, self.filePath[:self.filePath.rindex("/")] + "/" + self.fileName)
