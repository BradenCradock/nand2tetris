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

    """
    while parse.hasMoreCommands():
        parse.advance()
        if parse.commandType() in {"C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"}:
            print(parse.arg2())
    """

    codeWriter = CodeWriter.CodeWriter(root.filename)
    codeWriter.setFileName("Hello")
    codeWriter.closeFile()


if __name__ == "__main__":
    main()
