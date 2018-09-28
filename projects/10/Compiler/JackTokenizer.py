import re


class JackTokenizer:

    def __init__(self, filePath):

        with open(filePath, 'r') as file:
            self.programIn = file.read().splitlines()
            self.programIn = [line.split("//")[0].strip() for line in self.programIn]

            isComment = False
            for lineNum, line in enumerate(self.programIn): #Removes all comments using the /* identifier
                if "/*" in line:
                    if "*/" in line:
                        self.programIn[lineNum] = re.sub('/*(.*)*/', '', line)
                    else:
                        self.programIn[lineNum] = self.programIn[lineNum].split("/*", 1)[0]
                        isComment = True

                elif "*/" in line:
                    self.programIn[lineNum] = self.programIn[lineNum].split("*/")[1].strip()
                    isComment = False

                elif isComment:
                    self.programIn[lineNum] = ""


            self.programIn = re.split('([(;) ])', " ".join(self.programIn))
            self.programIn = " ".join(self.programIn).split()
            self.programIn = list(filter(None, self.programIn))

            file.close()
            self.currentToken = ""
            self.tokenCounter = 0

    def hasMoreTokens(self):
        return (self.tokenCounter) < len(self.programIn)

    def advance(self):
        self.currentToken = self.programIn[self.tokenCounter].split("//")[0]
        self.tokenCounter += 1


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
        return self.currentToken.upper()


    def symbol(self):
        return self.currentToken


    def identifier(self):
        return  self.currentToken


    def intVal(self):
        return int(self.currentToken)


    def stringVal(self):
        return self.currentToken.strip("\"")
