import sys
import re
from tkinter import *
from tkinter import filedialog

currentCommand = ""
currentCommandCounter = 0
programIn = []

root = Tk()
root.filename =  filedialog.askopenfilename(initialdir = "/", title = "Select .asm file", filetypes = (("asm files","*.asm"),("all files","*.*")))

with open(root.filename, 'r') as file:
    programIn = file.read().splitlines()
    file.close()

#Are there more commands to process?
def hasMoreCommands():
    if (currentCommandCounter) != len(programIn):
        return True
    else:
        return False

#Reads the next command. Removes whitespace and comments
def advance():
    global currentCommandCounter
    global currentCommand
    currentCommand = programIn[currentCommandCounter].replace(" ", "").split("//")[0]
    currentCommandCounter += 1

#Returns the command type, A, L or C
def commandType():
    global currentCommand
    if currentCommand.startswith("@"):
        return "A_COMMAND"
    elif currentCommand.startswith("("):
        return "L_COMMAND"
    elif not currentCommand:
        return ""
    else:
        return "C_COMMAND"

#Returns Xxx from @Xxx or (Xxx)
def symbol():
    global currentCommand
    if currentCommand.startswith("@"):
        return currentCommand.strip("@")
    else:
        return re.search(r'\((.*?)\)', currentCommand).group(1)

#Returns the destination registers of a C command
def dest():
    global currentCommand
    if "=" in currentCommand:
        return currentCommand.split("=")[0]

#Returns the computation insctructions of a C command
def comp():
    global currentCommand
    if "=" in currentCommand:
        if ";" in currentCommand:
            return currentCommand.split("=")[1].split(";")[0]
        else:
            return currentCommand.split("=")[1]
    elif ";" in currentCommand:
        return currentCommand.split(";")[0]

#Returns the jump conditions of a C command
def jump():
    global currentCommand
    if ";" in currentCommand:
        return currentCommand.split(";")[1]
