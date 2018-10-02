import sys
import CompilationEngine
import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

def main():
    root = Tk()
    root.withdraw()
    inputFilepath =  filedialog.askopenfilename(initialdir = "/", title = "Select a file", filetypes = (("jack files","*.jack"), ("all files","*.*")))
    outputFilepath = inputFilepath[:-5] + "T.xml"
    compilationEngine = CompilationEngine.CompilationEngine(inputFilepath, outputFilepath)

if __name__ == "__main__":
    main()
