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
                        self.programIn[lineNum].split("/*")[0].strip
                        isComment = True

                elif "*/" in line:
                    self.programIn[lineNum].split("*/")[1].strip
                    isComment = False

                elif isComment == True:
                    self.programIn[lineNum] = ""

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
        return


    def keyWord(self):
        return


    def symbol(self):
        return


    def identifier(self):
        return


    def intVal(self):
        return


    def stringVal(self):
        return
