import sys
import Parser
import os
import CodeWriter
from tkinter import *
from tkinter import filedialog

def main():
    root = Tk()
    root.withdraw()
    root.filename =  filedialog.askopenfilename(initialdir = "/", title = "Select .vm file", filetypes = (("vm files","*.vm"),("all files","*.*")))

    parse = Parser.Parser(root.filename)
    codeWriter = CodeWriter.CodeWriter(root.filename)


    while parse.hasMoreCommands():
        parse.advance()
        if parse.commandType() == "C_ARITHMETIC":
            codeWriter.writeArithmetic(parse.currentCommand)

        elif parse.commandType() in {"C_POP", "C_PUSH"}:
            codeWriter.writePushPop(parse.commandType(), parse.arg1(), parse.arg2())

    codeWriter.closeFile()

if __name__ == "__main__":
    main()
