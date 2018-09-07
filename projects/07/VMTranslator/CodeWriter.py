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

    #Writes the arithmetic assembly code that requires only one stack entry
    def unaryOp(self, operation):
        asmInstr =  "@SP\n" +\
                    "AM = M - 1\n" +\
                    "M ="  + operation + "M\n" +\
                    "@SP\n" +\
                    "M = M + 1\n"
        return asmInstr

    #Writes the arithmetic assembly code that requires only two stack entries
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
    #Writes the arithmetic assembly code that requires a comparison between two stack entries.
    #Note that this code requires labels in assembly hence the self.compareCounter
    def compareOp(self, command):

        asmInstr =  "@SP\n" +\
                    "AM = M - 1\n" +\
                    "D = M\n" +\
                    "@SP\n" +\
                    "AM = M - 1\n" +\
                    "D = M - D\n" +\
                    "@PASS" + str(self.compareCounter) + "\n" +\
                    "D;J" + command.upper() + "\n" +\
                    "D = 0\n" +\
                    "@END" + str(self.compareCounter) + "\n" +\
                    "0;JMP\n" +\
                    "(PASS" + str(self.compareCounter) + ")\n" +\
                    "@SP\n" +\
                    "D = -1\n" +\
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
        asmInstr = ""
        if command == "add":
            asmInstr = self.binaryOp("+")

        elif command == "sub":
            asmInstr = self.binaryOp("-")

        elif command == "neg":
            asmInstr = self.unaryOp("-")

        elif command == "eq":
            asmInstr = self.compareOp(command)

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

    def writePush(self):
        asmInstr =  "@SP\n" +\
                    "A = M\n" +\
                    "M = D\n" +\
                    "@SP\n" +\
                    "M = M + 1\n"
        return asmInstr

    def writePop(self):
            asmInstr = ""
            return asmInstr

    #Writes the assembly code that is the translation of the given command, where command is either C_PUSH or C_POP.
    def writePushPop(self, command, segment, index):
        asmInstr = ""
        asmHeapSegments = {
                    "local"     : "LCL",
                    "argument"  : "ARG",
                    "this"      : "THIS",
                    "that"      : "THAT"
        }

        if command == "C_PUSH":
            if segment == "static":
                asmInstr =  "@" + self.fileName.split(".")[0] + "." + str(index) +"\n" +\
                            "D = A\n" +\
                            self.writePush()

            elif segment in {"local", "argument", "this", "that"}:

                asmInstr =  "@" + asmHeapSegments[segment] + "\n" +\
                            "D = M\n" +\
                            "@" + str(index) + "\n" +\
                            "A = D + A\n" +\
                            "D = M\n" +\
                            self.writePush()

            elif segment == "constant":
                asmInstr =  "@" + str(index) + "\n" +\
                            "D = A\n" +\
                            self.writePush()

        elif command == "C_POP":
            if segment == "static":
                asmInstr =  "@SP\n" +\
                            "AM = M - 1\n" +\
                            "D = M\n" +\
                            "@" + self.fileName.split(".")[0] + "." + str(index) +"\n" +\
                            "M = D\n"

            elif segment in {"local", "argument", "this", "that"}:
                asmInstr =  "@" + asmHeapSegments[segment] + "\n" +\
                            "D = M\n" +\
                            "@" + str(index) + "\n" +\
                            "D = D + A\n" +\
                            "@R13\n" +\
                            "M = D\n" +\
                            "@SP\n" +\
                            "AM = M - 1\n" +\
                            "D = M\n" +\
                            "@R13\n" +\
                            "A = M\n" +\
                            "M = D\n"
        self.file.write(asmInstr)

    #Closes and renames the file to the designated name, if the file already exists then it is replaced by the new version
    def closeFile(self):
        self.file.close()
        try:
            os.rename(self.filePath, self.filePath[:self.filePath.rindex("/")] + "/" + self.fileName)
        except WindowsError:
            os.remove(self.filePath[:self.filePath.rindex("/")] + "/" + self.fileName)
            os.rename(self.filePath, self.filePath[:self.filePath.rindex("/")] + "/" + self.fileName)
