import sys
import re

currentCommand = ""
currentCommandCounter = 0
programIn = []



#Are there more commands to process?
def hasMoreCommands():
    if (currentCommandCounter) != len(programIn):
        return True
    else:
        return False

#Reads the next command. Removes comments
def advance():
    global currentCommandCounter
    global currentCommand
    currentCommand = programIn[currentCommandCounter].split("//")[0]
    currentCommandCounter += 1

#Returns the type of the current VM command.
#C_ARITHMETIC is returned for all the arithmetic commands.
def commandType():
    global currentCommand
    commandTypes = {
            "add"       : "C_ARITHMETIC",
            "sub"       : "C_ARITHMETIC",
            "neg"       : "C_ARITHMETIC",
            "eq"        : "C_ARITHMETIC",
            "gt"        : "C_ARITHMETIC",
            "lt"        : "C_ARITHMETIC",
            "and"       : "C_ARITHMETIC",
            "or"        : "C_ARITHMETIC",
            "not"       : "C_ARITHMETIC",
            "pop"       : "C_POP",
            "push"      : "C_PUSH",
            "label"     : "C_LABEL",
            "goto"      : "C_GOTO",
            "if-goto"   : "C_IF",
            "function"  : "C_FUNCTION",
            "call"      : "C_RETURN",
            "return"    : "C_CALL"
    }
    return(commandTypes[currentCommand.split(' ')[0]])

#Returns the first arg. of the current command.
#In the case of C_ARITHMETIC, the command itself (add, sub, etc.) is returned.
#Should not be called if the current command is C_RETURN
def arg1():
    if commandType() == "C_ARITHMETIC":
        return currentCommand.split(' ')[0]
    else:
        return currentCommand.split(' ')[1]

#Returns the second argument of the current command.
#Should be called only if the current command is C_PUSH, C_POP, C_FUNCTION, or C_CALL.
def arg2():
    return currentCommand.split(' ')[2]

#Reads Prog.asm in current directory
with open("Prog.vm", 'r') as file:
    programIn = file.read().splitlines()
    programIn = [line for line in programIn if not line.startswith("//")]
    programIn = list(filter(None, programIn))
    file.close()
