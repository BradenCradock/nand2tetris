class Parser:

    def __init__(self, filePath):

        self.currentCommand = ""
        self.currentCommandCounter = 0
        self.programIn = []

        with open(filePath, 'r') as file:
            self.programIn = file.read().splitlines()
            self.programIn = [line.split("//")[0].strip() for line in self.programIn] #Remove all comments
            self.programIn = list(filter(None, self.programIn))   #Remove any empty lines
            file.close()


    #Are there more commands to process?
    def hasMoreCommands(self):
        return (self.currentCommandCounter) < len(self.programIn)

    #Reads the next command. Removes comments
    def advance(self):
        self.currentCommand = self.programIn[self.currentCommandCounter].split("//")[0]
        self.currentCommandCounter += 1

    #Returns the type of the current VM command.
    #C_ARITHMETIC is returned for all the arithmetic commands.
    def commandType(self):
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
        return(commandTypes[self.currentCommand.split(' ')[0]])

    #Returns the first arg. of the current command.
    #In the case of C_ARITHMETIC, the command itself (add, sub, etc.) is returned.
    #Should not be called if the current command is C_RETURN
    def arg1(self):
        if commandType() == "C_ARITHMETIC":
            return self.currentCommand.split(' ')[0]
        else:
            return self.currentCommand.split(' ')[1]

    #Returns the second argument of the current command.
    #Should be called only if the current command is C_PUSH, C_POP, C_FUNCTION, or C_CALL.
    def arg2(self):
        return self.currentCommand.split(' ')[2]
