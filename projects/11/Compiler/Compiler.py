import sys
import VMWriter
import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

def main():
    root = Tk()
    root.withdraw()
    inputFilepath = filedialog.askdirectory(initialdir = "/", title = "Select a folder")
    for fileName in os.listdir(inputFilepath):
        if fileName.lower().endswith(".jack"):
            Writer = VMWriter.VMWriter(os.path.basename(inputFilepath) + "\\" + fileName, os.path.basename(inputFilepath) + "\\" + fileName[:-5] + ".xml")

if __name__ == "__main__":
    main()
