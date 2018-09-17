import os
import re
import Parser
class CodeWriter:

    def __init__(self, filePath):

        self.file = open(filePath, "w+")
        self.filePath = filePath
        self.fileName = ""
        self.compareCounter = 0
        self.returnAddress = 0

    #Informs the code writer that the translation of a new VM file is started.
    def setFileName(self, fileName):
        self.fileName = fileName
        print("Begun translating file: " + fileName)

    #Writes the assembly code that effects the VM initialization, called bootstrap code.
    #This code is placed at the beginning of the output file.
    def writeInit(self):
        asmCode =   "@256\n" +\
                    "D = A\n" +\
                    "@SP\n" +\
                    "M = D\n"

        self.file.write(asmCode)
        self.writeCall("Sys.init", 0)

    #Writes the arithmetic assembly code that requires only one stack entry.
    def unaryOp(self, operation):
        asmCode =   "@SP\n" +\
                    "AM = M - 1\n" +\
                    "M ="  + operation + "M\n" +\
                    "@SP\n" +\
                    "M = M + 1\n"
        return asmCode

    #Writes the arithmetic assembly code that requires only two stack entries
    def binaryOp(self, operation):
        asmCode =  "@SP\n" +\
                    "AM = M - 1\n" +\
                    "D = M\n" +\
                    "@SP\n" +\
                    "AM = M - 1\n" +\
                    "M = M " + operation + " D\n" +\
                    "@SP\n" +\
                    "M = M + 1\n"
        return asmCode

    #Writes the arithmetic assembly code that requires a comparison between two stack entries.
    #Note that this code requires labels in assembly hence the self.compareCounter
    def compareOp(self, command):
        asmCode =  "@SP\n" +\
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
        return asmCode

    #Writes the assembly code that is the translation of the given arithmetic command.
    def writeArithmetic(self, command):
        asmCode = ""
        if command == "add":
            asmCode = self.binaryOp("+")

        elif command == "sub":
            asmCode = self.binaryOp("-")

        elif command == "neg":
            asmCode = self.unaryOp("-")

        elif command == "eq":
            asmCode = self.compareOp(command)

        elif command == "gt":
            asmCode = self.compareOp(command)

        elif command == "lt":
            asmCode = self.compareOp(command)

        elif command == "or":
            asmCode = self.binaryOp("|")

        elif command == "and":
            asmCode = self.binaryOp("&")

        elif command == "not":
            asmCode = self.unaryOp("!")

        self.file.write(asmCode)

    #This block of code is appended onto any push command.
    #It writes whatever is stored in D to the stack then increments SP
    def writePush(self):
        asmCode =   "@SP\n" +\
                    "A = M\n" +\
                    "M = D\n" +\
                    "@SP\n" +\
                    "M = M + 1\n"
        return asmCode

    #Writes the assembly code that is the translation of the given command, where command is either C_PUSH or C_POP.
    def writePushPop(self, command, segment, index):
        asmCode = ""
        segmentTranslator = {
                    "local"     : "LCL",
                    "argument"  : "ARG",
                    "this"      : "THIS",
                    "that"      : "THAT",
                    "pointer"   : 3,
                    "temp"      : 5
        }

        if command == "C_PUSH":
            #Mapped on RAM[16 ... 255]; each segment reference static i appearing in a VM file named f is compiled to the assembly language symbol f.i
            #Pushing a static i  is as simple as getting the value at its associated address f.i and pushing it onto the stack
            if segment == "static":
                asmCode =   "@" + self.fileName.split(".")[0] + "." + str(index) +"\n" +\
                            "D = M\n" +\
                            self.writePush()

            #These method-level segments are mapped somewhere from address 2048 onward, in an area called “heap”.
            #The base addresses of these segments are kept in RAM addresses LCL, ARG, THIS, and THAT.
            #Access to the i-th entry of any of these segments is implemented by accessing RAM[segmentBase + i].
            elif segment in {"local", "argument", "this", "that"}:
                asmCode =   "@" + segmentTranslator[segment] + "\n" +\
                            "D = M\n" +\
                            "@" + str(index) + "\n" +\
                            "A = D + A\n" +\
                            "D = M\n" +\
                            self.writePush()

            #A truly a virtual segment:
            #Access to constant i is implemented by supplying the constant i.
            elif segment == "constant":
                asmCode =   "@" + str(index) + "\n" +\
                            "D = A\n" +\
                            self.writePush()

            #These segments are each mapped directly onto a fixed area in the RAM.
            #The pointer segment is mapped on RAM locations 3-4 (also called THIS and THAT)
            #The temp segment on locations 5-12 (also called R5, R6,..., R12).
            #Thus access to pointer i is translated to assembly code that accesses RAM location 3 + iself.
            #Access to temp i is translated to assembly code that accesses RAM location 5 + i.
            elif segment in {"pointer", "temp"}:
                asmCode =   "@R" + str(index + segmentTranslator[segment]) + "\n" +\
                            "D = M\n" +\
                            self.writePush()

        elif command == "C_POP":
            #Mapped on RAM[16 ... 255]; each segment reference static i appearing in a VM file named f is compiled to the assembly language symbol f.i
            #To pop static i the stack pointer SP is decremented and the value contained at the new stack location is stored in f.i
            if segment == "static":
                asmCode =   "@SP\n" +\
                            "AM = M - 1\n" +\
                            "D = M\n" +\
                            "@" + self.fileName.split(".")[0] + "." + str(index) +"\n" +\
                            "M = D\n"

            #These method-level segments are mapped somewhere from address 2048 onward, in an area called “heap”.
            #The base addresses of these segments are kept in RAM addresses LCL, ARG, THIS, and THAT.
            #Access to the i-th entry of any of these segments is implemented by accessing RAM[segmentBase + i].
            elif segment in {"local", "argument", "this", "that"}:
                asmCode =   "@" + segmentTranslator[segment] + "\n" +\
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

            #These segments are each mapped directly onto a fixed area in the RAM.
            #The pointer segment is mapped on RAM locations 3-4 (also called THIS and THAT)
            #The temp segment on locations 5-12 (also called R5, R6,..., R12).
            #Thus access to pointer i is translated to assembly code that accesses RAM location 3 + iself.
            #Access to temp i is translated to assembly code that accesses RAM location 5 + i.
            elif segment in {"pointer", "temp"}:
                asmCode =   "@SP\n" +\
                            "AM = M - 1\n" +\
                            "D = M\n" +\
                            "@R" + str(index + segmentTranslator[segment]) + "\n" +\
                            "M = D\n"

        self.file.write(asmCode)

    #Writes assembly code that is the translation of the label command.
    def writeLabel(self, label):
        asmCode = "(" + label + ")\n"

        self.file.write(asmCode)

    #Writes the assembly code that is the translation of the goto command.
    def writeGoto(self, label):
        asmCode =   "@" + label + "\n" +\
                    "0;JMP\n"

        self.file.write(asmCode)

    #Writes the assembly code that is the translation of the if-goto command.
    def writeIf(self, label):
        asmCode =   "@SP\n" +\
                    "AM = M - 1\n" +\
                    "D = M\n" +\
                    "@" + label + "\n" +\
                    "D;JNE\n"

        self.file.write(asmCode)

    #Writes the assembly code that is the translation of the call command.
    def writeCall(self, functionName, numArgs):
        asmCode =   "@" + str(self.returnAddress) + "\n" +\
                    "D = A\n" +\
                    self.writePush() +\
                    "@LCL\n" +\
                    "D = M\n" +\
                    self.writePush() +\
                    "@ARG\n" +\
                    "D = M\n" +\
                    self.writePush() +\
                    "@THIS\n" +\
                    "D = M\n" +\
                    self.writePush() +\
                    "@THAT\n" +\
                    "D = M\n" +\
                    self.writePush() +\
                    "@" + str(numArgs + 5) + "\n" +\
                    "D = A\n" +\
                    "@SP\n" +\
                    "D = M - D\n" +\
                    "@ARG\n" +\
                    "M = D\n" +\
                    "@SP\n" +\
                    "D = M\n" +\
                    "@LCL\n" +\
                    "M = D\n"

        self.file.write(asmCode)
        self.writeGoto(functionName)
        self.writeLabel(str(self.returnAddress))
        self.returnAddress += 1

    def restoreSegment(self, segment):
        asmCode =   "@R14\n" +\
                    "M = M - 1\n" +\
                    "A = M\n" +\
                    "D = M\n" +\
                    "@" + segment + "\n" +\
                    "M = D\n"

        return asmCode


    #Writes the assembly code that is the translation of the return command.
    def writeReturn(self):
        asmCode =   "@LCL\n" +\
                    "D = M\n" +\
                    "@R14\n" +\
                    "M = D\n" +\
                    "@5\n" +\
                    "AD = D - A\n" +\
                    "@R15\n" +\
                    "M = D\n" +\
                    "@SP\n" +\
                    "AM = M - 1\n" +\
                    "D = M\n" +\
                    "@ARG\n" +\
                    "A = M\n" +\
                    "M = D\n" +\
                    "D = A\n" +\
                    "@SP\n" +\
                    "M = D + 1\n" +\
                    self.restoreSegment("THAT") +\
                    self.restoreSegment("THIS") +\
                    self.restoreSegment("ARG") +\
                    self.restoreSegment("LCL") +\
                    "@R15\n" +\
                    "A = M\n" +\
                    "A = M\n" +\
                    "0;JMP\n"

        self.file.write(asmCode)

    #Writes the assembly code that is the translation of the function command.
    def writeFunction(self, functionName, numLocals):
        asmCode =   "(" + functionName + ")\n"

        for _ in range(numLocals):
            asmCode +=  "@0\n" +\
                        "D = A\n" +\
                        self.writePush()

        self.file.write(asmCode)

    #Closes and renames the file to the designated name, if the file already exists then it is replaced by the new version
    def closeFile(self):
        self.file.close()
