import sys
import Parser
import os
import CodeWriter
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox



def translateVM(file, codeWriter):
    parse = Parser.Parser(file)
    codeWriter.writeInit()
    while parse.hasMoreCommands():
        parse.advance()
        if parse.commandType() == "C_ARITHMETIC":
            codeWriter.writeArithmetic(parse.currentCommand)

        elif parse.commandType() in {"C_POP", "C_PUSH"}:
            codeWriter.writePushPop(parse.commandType(), parse.arg1(), int(parse.arg2()))

        elif parse.commandType() == "C_LABEL":
            codeWriter.writeLabel(parse.arg1())

        elif parse.commandType() == "C_GOTO":
            codeWriter.writeGoto(parse.arg1())

        elif parse.commandType() == "C_IF":
            codeWriter.writeIf(parse.arg1())

        elif parse.commandType() == "C_CALL":
            codeWriter.writeCall(parse.arg1(), int(parse.arg2()))

        elif parse.commandType() == "C_FUNCTION":
            codeWriter.writeFunction(parse.arg1(), int(parse.arg2()))

        elif parse.commandType() == "C_RETURN":
            codeWriter.writeReturn()

def main():
    root = Tk()
    root.withdraw()
    filePath =  filedialog.askdirectory(initialdir = "/", title = "Select a folder")

    codeWriter = CodeWriter.CodeWriter(filePath + "\\" + os.path.basename(filePath) + ".asm")

    for fileName in os.listdir(filePath):
        if fileName.lower().endswith(".vm"):
            codeWriter.setFileName(fileName)
            translateVM(filePath + "\\" + fileName, codeWriter)

    codeWriter.closeFile()

if __name__ == "__main__":
    main()
