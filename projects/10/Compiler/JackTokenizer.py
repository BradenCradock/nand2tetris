import re

class JackTokenizer:

    def __init__(self, filePath):

        with open(filePath, 'r') as file:
            self.programIn = file.read().splitlines()
            #self.programIn = [line.split("//")[0].strip() for line in self.programIn] #Remove all comments that use the "//" identifier

            isComment = False
            for lineNum, line in enumerate(self.programIn): #Removes all comments
                lineNoQuotes = re.sub('"[^>]+"', '', line)
                if ("/*" in lineNoQuotes) & ("//" in lineNoQuotes):
                    if lineNoQuotes.find("/*") < lineNoQuotes.find("//"):
                        if "*/" in lineNoQuotes:
                            self.programIn[lineNum] = re.sub('/*(.*)*/', '', line)
                        else:
                            self.programIn[lineNum] = self.programIn[lineNum].split("/*", 1)[0]
                            isComment = True
                    else:
                        self.programIn[lineNum] = line.split("//")[0]
                if ("/*" in lineNoQuotes):
                    if "*/" in lineNoQuotes:
                        self.programIn[lineNum] = re.sub('/*(.*)*/', '', line)
                    else:
                        self.programIn[lineNum] = self.programIn[lineNum].split("/*", 1)[0]
                        isComment = True

                elif ("*/" in lineNoQuotes) & (isComment == True):
                    self.programIn[lineNum] = self.programIn[lineNum].split("*/")[1]
                    isComment = False

                elif "//" in lineNoQuotes:
                    self.programIn[lineNum] = line.split("//")[0]

                elif isComment:
                    self.programIn[lineNum] = ""

            self.programIn = re.split('([(;)., ])', " ".join(self.programIn)) #Creates a new element in the list for every instance of "(", ")" and ";"
            self.programIn = " ".join(self.programIn).split() #Seperates every token into a new element
            self.programIn = list(filter(None, self.programIn)) #Removes any null elements in the list

            file.close()
            self.currentToken = ""
            self.currentTokenType = ""
            self.tokenCounter = 0

    def hasMoreTokens(self):
        return (self.tokenCounter) < len(self.programIn)

    def advance(self):
        self.currentToken = self.programIn[self.tokenCounter]
        self.tokenCounter += 1
        self.currentTokenType = self.tokenType()
        if self.currentTokenType == "KEYWORD":
            self.currentToken = self.keyWord()
        elif self.currentTokenType == "SYMBOL":
            self.currentToken = self.symbol()
        elif self.currentTokenType == "IDENTIFIER":
            self.currentToken = self.identifier()
        elif self.currentTokenType == "INT_CONST":
            self.currentToken = self.intVal()
        elif self.currentTokenType == "STRING_CONST":
            self.currentToken = self.stringVal()

    def tokenType(self):
        if self.currentToken[0].isalpha() or self.currentToken[0] == "_":

            keywords = {"class", "constructor", "function", "method", "field","static",
                        "var","int", "char", "boolean", "void", "true", "false",
                        "null", "this","let", "do", "if", "else", "while", "return"}

            if self.currentToken in keywords:
                return "KEYWORD"
            else:
                return "IDENTIFIER"
        elif self.currentToken[0].isnumeric():
            return "INT_CONST"

        elif self.currentToken[0] == "\"":
            return  "STRING_CONST"

        else:
            return "SYMBOL"

    def keyWord(self):
        return self.currentToken


    def symbol(self):
        return self.currentToken


    def identifier(self):
        return  self.currentToken


    def intVal(self):
        return self.currentToken


    def stringVal(self):
        return self.currentToken.strip("\"")
