import re

class JackTokenizer:

    def __init__(self, filePath):

        with open(filePath, 'r') as file:

            self.programIn = file.read()
            self.tokens = []
            self.formatProgramAsRead()

            file.close()
            #print(*self.tokens, sep = "\n")
            self.currentToken = ""
            self.currentTokenType = ""
            self.tokenCounter = 0

    def removeComments(self):
        pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
        # first group captures quoted strings (double or single)
        # second group captures comments (//single-line or /* multi-line */)
        regex = re.compile(pattern, re.MULTILINE|re.DOTALL)

        def _replacer(match):
            # if the 2nd group (capturing comments) is not None,
            # it means we have captured a non-quoted (real) comment string.
            if match.group(2) is not None:
                return "" # so we will return empty to remove the comment
            else: # otherwise, we will return the 1st group
                return match.group(1) # captured quoted-string

        return regex.sub(_replacer, self.programIn)

    def fixStrings(self):
        string = False
        appendedString = ""
        newlist = []
        for line in self.tokens:
            if "\"" in line and string == False:
                string = True
                appendedString = line
            elif string == True and "\"" in line:
                string = False
                appendedString += " " + line
                newlist.append(appendedString)
            elif string == True:
                appendedString += " " + line

            elif line.startswith("-") and len(line) > 1:
                newlist.append("-")
                newlist.append(line[1:])
            else:
                newlist.append(line)
        return newlist

    def removeWhitespace(self):
        newlist = (item.strip() if hasattr(item, 'strip') else item for item in self.tokens)
        return [item for item in newlist if item != '']

    def formatProgramAsRead(self):
        self.programIn = self.removeComments()
        self.tokens = re.split('([(;})~{.,-])| ', self.programIn)
        self.tokens = self.removeWhitespace()
        self.tokens = list(filter(None, self.tokens)) #Removes any null elements in the list
        self.tokens = self.fixStrings()

    def hasMoreTokens(self):
        return (self.tokenCounter) < len(self.tokens)

    def advance(self):
        self.currentToken = self.tokens[self.tokenCounter]
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

        if re.match("[a-zA-Z_]", self.currentToken):

            keywords = {"class", "constructor", "function", "method", "field","static",
                        "var","int", "char", "boolean", "void", "true", "false",
                        "null", "this", "let", "do", "if", "else", "while", "return"}

            if self.currentToken in keywords:
                return "KEYWORD"
            else:
                return "IDENTIFIER"
        elif self.currentToken.isnumeric():
            return "INT_CONST"

        elif self.currentToken.startswith("\"") and  self.currentToken.endswith("\""):
            return  "STRING_CONST"

        elif re.match("\W", self.currentToken):
            return "SYMBOL"
        else:
            print("Invalid token: " + self.currentToken)

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
