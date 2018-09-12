import sys
import Parser
import os
import CodeWriter
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox



def chooseFiles():
    root = Tk()
    root.withdraw()
    if messagebox.askyesno('Directory or File?', 'Do you want to translate a folder of .vm files?'):
        filePath =  filedialog.askdirectory(initialdir = "/", title = "Select a folder")
        return filePath
    else:
        filePath =  filedialog.askopenfilename(initialdir = "/", title = "Select a .vm file", filetypes = (("vm files","*.vm"),("all files","*.*")))
        return filePath


def main():
    filePath = chooseFiles()
    parse = Parser.Parser(filePath)
    codeWriter = CodeWriter.CodeWriter(filePath)

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

    codeWriter.closeFile()





if __name__ == "__main__":
    main()
