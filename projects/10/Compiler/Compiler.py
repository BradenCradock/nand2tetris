import sys
import JackTokenizer
import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

def main():
    root = Tk()
    root.withdraw()
    filePath =  filedialog.askopenfilename(initialdir = "/", title = "Select a file", filetypes = (("jack files","*.jack"), ("all files","*.*")))

    tokenizer = JackTokenizer.JackTokenizer(filePath)

    while tokenizer.hasMoreTokens():
        tokenizer.advance()
        tokenType = tokenizer.tokenType()
        if tokenType == "KEYWORD":
            print(tokenizer.keyWord())
        elif tokenType == "SYMBOL":
            print(tokenizer.symbol())
        elif tokenType == "IDENTIFIER":
            print(tokenizer.identifier())
        elif tokenType == "INT_CONST":
            print(tokenizer.intVal())
        elif tokenType == "STRING_CONST":
            print(tokenizer.stringVal())

if __name__ == "__main__":
    main()
