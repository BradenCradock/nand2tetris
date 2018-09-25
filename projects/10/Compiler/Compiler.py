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
        print(tokenizer.currentToken)

if __name__ == "__main__":
    main()
