class VMWriter:

    def __init__(self, outputFilepath):
        self.VMFile = open(outputFilepath, "w+")

    #Writes a VM push command
    def writePush(self, segment, index):
        print("push " + segment.lower() + " " + str(index), file = self.VMFile)

    #Writes a VM pop command
    def writePop(self, segment, index):
        print("pop " + segment.lower() + " " + str(index), file = self.VMFile)

    #Writes a VM arithmetic command
    def writeArithmetic(self, command):
        print(command.lower(), file = self.VMFile)

    #Writes a VM label command
    def writeLabel(self, label):
        print("label " + label, file = self.VMFile)

    #Writes a VM goto command
    def writeGoto(self, label):
        print("goto " + label, file = self.VMFile)

    #Writes a VM If-goto command
    def writeIf(self, label):
        print("if-goto " + label, file = self.VMFile)

    #Writes a VM call command
    def writeCall(self, name, nArgs):
        print("call " + name + " " + str(nArgs), file = self.VMFile)

    #Writes a VM function command
    def writeFunction(self, name, nLocals):
        print("function " + name + " " + str(nLocals), file = self.VMFile)

    #Writes a VM return command
    def writeReturn(self):
        print("return", file = self.VMFile)

    #Closes the output file
    def close(self):
        self.VMFile.close()
        return
