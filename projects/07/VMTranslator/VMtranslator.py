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
        if parse.commandType() is "C_ARITHMETIC":
            print(parse.currentCommand)
            codeWriter.writeArithmetic(parse.currentCommand)
    codeWriter.closeFile()

if __name__ == "__main__":
    main()
