import sys
import CompilationEngine
import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

def main():
    root = Tk()
    root.withdraw()
    inputFilepath =  filePath =  filedialog.askdirectory(initialdir = "/", title = "Select a folder")

    for fileName in os.listdir(inputFilepath):
        if fileName.lower().endswith(".jack"):
            compilationEngine = CompilationEngine.CompilationEngine(inputFilepath, (inputFilepath + "\\" + os.path.basename(inputFilepath) + ".xml"))

if __name__ == "__main__":
    main()
