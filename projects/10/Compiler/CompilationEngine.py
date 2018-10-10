import JackTokenizer
import re
import sys

class CompilationEngine:

    def __init__(self, inputFilepath, outputFilepath):
        self.tokenizer = JackTokenizer.JackTokenizer(inputFilepath)
        self.file = open(outputFilepath, "w+")
        self.xmlIndentation = 0
        self.types = ["int", "boolean", "char"]

        self.compileClass()

    def writeXml(self):
        rep = {"<"  : "&lt;",
               ">"  : "$gt;",
               "\"" : "&quot;",
               "&"  : "&amp;"}
        rep = dict((re.escape(k), v) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        token = pattern.sub(lambda m: rep[re.escape(m.group(0))], self.tokenizer.currentToken)

        print("\t" * self.xmlIndentation + "<" + self.tokenizer.currentTokenType + "> " + token + " </" + self.tokenizer.currentTokenType + "> ", file = self.file)


    def syntaxError(self, expected, recieved):
        print("</class>", file = self.file)
        sys.exit("Invalid Syntax: Expected " + expected + "but recieved " + recieved)

    def checkToken(self, string):
        if self.tokenizer.currentToken in string:
            self.writeXml()
            self.tokenizer.advance()
        else:
            self.syntaxError(string, self.tokenizer.currentToken)

    def checkTokenType(self, string):
        if self.tokenizer.currentTokenType in string:
            self.writeXml()
            self.tokenizer.advance()
        else:
            self.syntaxError(string, self.tokenizer.currentTokenType)

    def checkVarType(self):
        if self.tokenizer.currentToken in self.types:
            self.writeXml()
            self.tokenizer.advance()
        else:
            print("</class>", file = self.file)
            sys.exit("Invalid Syntax: " + self.tokenizer.currentToken + "is not a valid type.")

    #Compiles a complete class.
    def compileClass(self):
        self.tokenizer.advance()
        print("<class>", file = self.file)
        self.xmlIndentation += 1

        self.checkToken("class")
        self.checkTokenType("IDENTIFIER")
        self.checkToken("{")

        while self.tokenizer.currentToken not in {"}", "constructor", "function", "method", "void"} :
            self.compileClassVarDec()
        while self.tokenizer.currentToken != "}":
            self.compileSubroutine()

        print("</class>", file = self.file)
        self.xmlIndentation -= 1


    #Compiles a static or field declaration.
    def compileClassVarDec(self):
        print("\t" * self.xmlIndentation + "<classVarDec>", file = self.file)
        self.xmlIndentation += 1

        self.checkToken({"field", "static"})
        self.checkVarType()
        self.checkTokenType("IDENTIFIER")
        while self.tokenizer.currentToken != ";":
            self.checkToken(",")
            self.checkTokenType("IDENTIFIER")
        self.checkToken(";")

        self.xmlIndentation -= 1
        print("\t" * self.xmlIndentation + "</classVarDec>", file = self.file)

    #Compiles a complete method, function or constructor.
    def compileSubroutine(self):
        print("\t" * self.xmlIndentation + "<subroutineDec>", file = self.file)
        self.xmlIndentation += 1

        self.checkToken({"constructor", "function", "method", "void"})
        self.checkToken(self.types.append("void"))
        self.checkTokenType("IDENTIFIER")
        self.checkToken("(")
        self.compileParameterList()
        self.checkToken(")")
        self.compileSubroutineBody()

        self.xmlIndentation -= 1
        print("\t" * self.xmlIndentation + "</subroutineDec>", file = self.file)
        return


    #Compiles the boday of a method, function or constructor.
    def compileSubroutineBody(self):
        print("\t" * self.xmlIndentation + "<subroutineBody>", file = self.file)
        self.xmlIndentation += 1

        self.checkToken("{")
        while self.tokenizer.currentToken != "return":
            if self.tokenizer.currentToken == "var":
                    self.compileVarDec()
            if self.tokenizer.currentToken == "}":
                self.writeXml()
                self.tokenizer.advance()

            else:
                print("</class>", file = self.file)
                sys.exit("Invalid Syntax: Expected \"}\" after return.")
        else:
            print("</class>", file = self.file)
            sys.exit("Invalid Syntax: Expected \"{\" after declaration of function.")
        return
    #Compiles a (possibly empty) parameter list, not including the enclosing"()".
    def compileParameterList(self):
        print("\t" * self.xmlIndentation + "<parameterList>", file = self.file)
        self.xmlIndentation += 1

        #while self.tokenizer.currentToken != ")":

        return

    #Compiles a var declaration.
    def compileVarDec(self):
        return

    #Compiles a sequence of statements, not including the enclosing "{}".
    def compileStatements(self):
        return

    #Compiles a do statement.
    def compileDo(self):
        return

    #Compiles a let statement.
    def compileLet(self):
        return

    #Compiles a while statement.
    def compileWhile(self):
        return

    #Compiles a return statement.
    def compileReturn(self):
        return

    #Compiles an if statement, possibly with a trailing else clause.
    def compileIf(self):
        return

    #Compiles and expression.
    def compileExpression(self):
        return

    #Compiles a term.
    #This rotuine is faced with a slight difficulty when trying to decide between some of the alternate parsing rules.
    #Specifically, if the current token is an identifier, the subrotuine must distinguish between a varible, an array entry and a subrotune call.
    #A single look ahead token, which may be one of "[", "(" or "." suffices to distinguish between the three possibilities.
    #Any other token is not part of this term and should not be advanced over.
    def compileTerm(self):
        return

    #Compiles a (possibily empty) comma-seperated list of expressions.
    def compileExpressionList(self):
        return
