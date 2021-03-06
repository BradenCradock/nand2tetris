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
        self.xmlIndentation = 0
        self.xmlCloseTag("class")
        sys.exit("Invalid Syntax: Expected " + str(expected) + " but recieved " + recieved)

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
            self.xmlIndentation = 0
            self.xmlCloseTag("class")
            sys.exit("Invalid Syntax: " + self.tokenizer.currentToken + " is not a valid type.")

    def xmlOpenTag(self, tag):
        print("\t" * self.xmlIndentation + "<" + tag + ">", file = self.file)
        self.xmlIndentation += 1

    def xmlCloseTag(self, tag):
        self.xmlIndentation -= 1
        print("\t" * self.xmlIndentation + "</" + tag + ">", file = self.file)

    #Compiles a complete class.
    def compileClass(self):
        self.tokenizer.advance()
        self.xmlOpenTag("class")

        self.checkToken("class")
        self.checkTokenType("IDENTIFIER")
        self.checkToken("{")
        while self.tokenizer.currentToken not in {"}", "constructor", "function", "method", "void"} :
            self.compileClassVarDec()
        while self.tokenizer.currentToken != "}":
            self.compileSubroutine()

        self.xmlCloseTag("class")

    #Compiles a static or field declaration.
    def compileClassVarDec(self):
        self.xmlOpenTag("classVarDec")

        self.checkToken({"field", "static"})
        if self.tokenizer.currentTokenType == "IDENTIFIER":
            self.checkTokenType("IDENTIFIER") #Should be var type check
        else:
            self.checkToken(self.types)
        self.checkTokenType("IDENTIFIER")
        while self.tokenizer.currentToken != ";":
            self.checkToken(",")
            self.checkTokenType("IDENTIFIER")
        self.checkToken(";")

        self.xmlCloseTag("classVarDec")

    #Compiles a complete method, function or constructor.
    def compileSubroutine(self):
        self.xmlOpenTag("subroutineDec")

        self.checkToken({"constructor", "function", "method", "void"})
        if self.tokenizer.currentTokenType == "IDENTIFIER":
            self.checkTokenType("IDENTIFIER") #Should be var type check
        else:
            self.checkToken(self.types + ["void"])
        self.checkTokenType("IDENTIFIER")
        self.checkToken("(")
        self.compileParameterList()
        self.checkToken(")")
        self.compileSubroutineBody()

        self.xmlCloseTag("subroutineDec")

    #Compiles the boday of a method, function or constructor.
    def compileSubroutineBody(self):
        self.xmlOpenTag("subroutineBody")

        self.checkToken("{")
        while self.tokenizer.currentToken not in {"let", "if", "while", "do", "return"}:
            self.compileVarDec()
        self.compileStatements()
        self.checkToken("}")

        self.xmlCloseTag("subroutineBody")

    #Compiles a (possibly empty) parameter list, not including the enclosing"()".
    def compileParameterList(self):
        if self.tokenizer.currentToken != ")":
            self.xmlOpenTag("parameterList")

            if self.tokenizer.currentTokenType == "IDENTIFIER":
                self.checkTokenType("IDENTIFIER") #Should be var type check
            else:
                self.checkToken(self.types)
            self.checkTokenType("IDENTIFIER")
            while self.tokenizer.currentToken != ")":
                self.checkToken(",")
                self.checkVarType()
                self.checkTokenType("IDENTIFIER")

            self.xmlCloseTag("parameterList")

    #Compiles a var declaration.
    def compileVarDec(self):
        self.xmlOpenTag("varDec")

        self.checkToken("var")
        if self.tokenizer.currentTokenType == "IDENTIFIER":
            self.checkTokenType("IDENTIFIER") #Should be var type check
        else:
            self.checkToken(self.types)
        self.checkTokenType("IDENTIFIER")
        while self.tokenizer.currentToken != (";"):
            self.checkToken(",")
            self.checkTokenType("IDENTIFIER")
        self.checkToken(";")

        self.xmlCloseTag("varDec")

    #Compiles a sequence of statements, not including the enclosing "{}".

    def compileStatements(self):
        self.xmlOpenTag("statements")

        statementPrefixes = {
            "let"       : self.compileLet,
            "do"        : self.compileDo,
            "if"        : self.compileIf,
            "while"     : self.compileWhile,
            "return"    : self.compileReturn
        }
        while self.tokenizer.currentToken != ("}"):
            if self.tokenizer.currentToken in statementPrefixes:
                statementPrefixes[self.tokenizer.currentToken]()
            else:
                print(self.tokenizer.currentToken)
                self.syntaxError("One of (let, do, if, while, return)", self.tokenizer.currentToken)

        self.xmlCloseTag("statements")

    #Compiles a do statement.
    def compileDo(self):
        self.xmlOpenTag("doStatement")

        self.checkToken("do")
        self.compileExpression()
        self.checkToken(";")

        self.xmlCloseTag("doStatement")

    #Compiles a let statement.
    def compileLet(self):
        self.xmlOpenTag("letStatement")

        self.checkToken("let")
        self.checkTokenType("IDENTIFIER")
        if self.tokenizer.currentToken == "[":
            self.checkToken("[")
            self.compileExpression()
            self.checkToken("]")
        self.checkToken("=")
        self.compileExpression()
        self.checkToken(";")

        self.xmlCloseTag("letStatement")

    #Compiles a while statement.
    def compileWhile(self):
        self.xmlOpenTag("whileStatement")

        self.checkToken("while")
        self.checkToken("(")
        self.compileExpression()
        self.checkToken(")")
        self.checkToken("{")
        self.compileStatements()
        self.checkToken("}")

        self.xmlCloseTag("whileStatement")

    #Compiles a return statement.
    def compileReturn(self):
        self.xmlOpenTag("returnStatement")

        self.checkToken("return")
        if self.tokenizer.currentToken != ";":
            self.compileExpression()
        self.checkToken(";")

        self.xmlCloseTag("returnStatement")

    #Compiles an if statement, possibly with a trailing else clause.
    def compileIf(self):
        self.xmlOpenTag("ifStatement")

        self.checkToken("if")
        self.checkToken("(")
        self.compileExpression()
        self.checkToken(")")
        self.checkToken("{")
        self.compileStatements()
        self.checkToken("}")
        if self.tokenizer.currentToken == "else":
            self.checkToken("else")
            self.checkToken("{")
            self.compileStatements()
            self.checkToken("}")

        self.xmlCloseTag("ifStatement")

    #Compiles an expression.
    def compileExpression(self):
        self.xmlOpenTag("expression")

        self.compileTerm()
        while self.tokenizer.currentToken not in {"]", ")", ";", ",", "("}:
            self.checkToken({"+", "-", "*", "/", "&", "|", ">", "<", "="})
            self.compileTerm()

        self.xmlCloseTag("expression")

    #Compiles a term.
    #This rotuine is faced with a slight difficulty when trying to decide between some of the alternate parsing rules.
    #Specifically, if the current token is an identifier, the subrotuine must distinguish between a varible, an array entry and a subrotune call.
    #A single look ahead token, which may be one of "[", "(" or "." suffices to distinguish between the three possibilities.
    #Any other token is not part of this term and should not be advanced over.
    def compileTerm(self):
        self.xmlOpenTag("term")

        invalidKeywords = {"class", "constructor", "function", "method", "field",
                           "static","var","int", "char", "boolean", "void",
                           "let", "do", "if", "else", "while", "return"}

        if self.tokenizer.currentTokenType == "IDENTIFIER":
            self.checkTokenType("IDENTIFIER")
            if self.tokenizer.currentToken == "[":             #Identifier is an array
                self.checkToken("[")
                self.compileExpression()
                self.checkToken("]")
            elif self.tokenizer.currentToken in {"(", "."}:    #Identifier is a subroutine call
                self.compileSubroutineCall()

        elif self.tokenizer.currentToken in {"-", "~"}:
            self.checkToken({"-", "~"})
            self.compileTerm()

        elif self.tokenizer.currentToken == "(":
            self.checkToken("(")
            self.compileExpression()
            self.checkToken(")")

        elif self.tokenizer.currentToken not in invalidKeywords:
            self.writeXml()
            self.tokenizer.advance()

        else:
            self.syntaxError("One of (true, false, null, this)", self.tokenizer.currentToken)

        self.xmlCloseTag("term")

    def compileSubroutineCall(self):
        self.xmlOpenTag("subroutineCall")

        if self.tokenizer.currentToken == ".":
            self.checkToken(".")
            self.checkTokenType("IDENTIFIER")
        self.checkToken("(")
        self.compileExpressionList()
        self.checkToken(")")

        self.xmlCloseTag("subroutineCall")
    #Compiles a (possibily empty) comma-seperated list of expressions.
    def compileExpressionList(self):
        self.xmlOpenTag("expressionList")

        if self.tokenizer.currentToken != ")":
            self.compileExpression()
        while self.tokenizer.currentToken != ")":
            self.checkToken(",")
            self.compileExpression()

        self.xmlCloseTag("expressionList")
