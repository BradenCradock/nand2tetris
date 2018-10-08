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

    #Compiles a complete class.
    def compileClass(self):
        self.tokenizer.advance()
        print("<class>", file = self.file)
        self.xmlIndentation += 1

        if self.tokenizer.currentToken == "class":
            self.writeXml()
            self.tokenizer.advance()

            if self.tokenizer.currentTokenType == "IDENTIFIER":
                self.writeXml()
                self.tokenizer.advance()

                if self.tokenizer.currentToken == "{":
                    self.writeXml()
                    self.tokenizer.advance()

                    while self.tokenizer.currentToken not in {"}", "constructor", "function", "method", "void"} :
                        if self.tokenizer.currentToken in {"field", "static"}:
                            self.compileClassVarDec()
                        else:
                            print("</class>", file = self.file)
                            sys.exit("Invalid Syntax: Expected declaration of a variable or subrotuine.")

                    while self.tokenizer.currentToken != "}":
                        if self.tokenizer.currentToken in {"constructor", "function", "method", "void"}:
                            self.compileSubroutine()
                        elif self.tokenizer.currentToken in {"field", "static"}:
                            print("</class>", file = self.file)
                            sys.exit("Invalid Syntax: Declaration of all class variables must occur before subrotuines.")
                        else:
                            print("</class>", file = self.file)
                            sys.exit("Invalid Syntax: Expected declaration of a variable or subrotuine.")

                else:
                    print("</class>", file = self.file)
                    sys.exit("Invalid Syntax: Expected \"{\" after class identifier.")
            else:
                print("</class>", file = self.file)
                sys.exit("Invalid Syntax: Expected identifier after class declaration.")
        else:
            print("</class>", file = self.file)
            sys.exit("Invalid Syntax: Module must begin with class declaration.")
        print("</class>", file = self.file)
        self.xmlIndentation -= 1
        return

    #Compiles a static or field declaration.
    def compileClassVarDec(self):
        print("\t" * self.xmlIndentation + "<classVarDec>", file = self.file)
        self.xmlIndentation += 1
        self.writeXml()
        self.tokenizer.advance()

        if self.tokenizer.currentToken in self.types:
            self.writeXml()
            self.tokenizer.advance()

            if self.tokenizer.currentTokenType == "IDENTIFIER":
                self.writeXml()
                self.tokenizer.advance()

                while self.tokenizer.currentToken != ";":
                    if self.tokenizer.currentToken == ",":
                        self.writeXml()
                        self.tokenizer.advance()
                        if self.tokenizer.currentTokenType == "IDENTIFIER":
                            self.writeXml()
                            self.tokenizer.advance()

                        else:
                            print("</class>", file = self.file)
                            sys.exit("Invalid Syntax: Variable names cannot begin with a digit.")
                    else:
                        print("</class>", file = self.file)
                        sys.exit("Invalid Syntax: Expected \",\" or \";\"")

                self.writeXml()
                self.tokenizer.advance()

            else:
                print("</class>", file = self.file)
                sys.exit("Invalid Syntax: Idenfifier cannot begin with a digit.")
        else:
            print("</class>", file = self.file)
            sys.exit("Invalid syntax or invalid variable type.")

        self.xmlIndentation -= 1
        print("\t" * self.xmlIndentation + "</classVarDec>", file = self.file)
        return

    #Compiles a complete method, function or constructor.
    def compileSubroutine(self):
        print("\t" * self.xmlIndentation + "<subroutineDec>", file = self.file)
        self.xmlIndentation += 1
        self.writeXml()
        self.tokenizer.advance()
        if (self.tokenizer.currentToken in self.types) | (self.tokenizer.currentToken == "void"):
            self.writeXml()
            self.tokenizer.advance()

            if self.tokenizer.currentTokenType == "IDENTIFIER":
                self.writeXml()
                self.tokenizer.advance()

                if self.tokenizer.currentToken == "(":
                    self.writeXml()
                    self.tokenizer.advance()
                    self.compileParameterList()

                    if self.tokenizer.currentToken == ")":
                        self.writeXml()
                        self.tokenizer.advance()
                        self.compileSubroutineBody()

                    else:
                        print("</class>", file = self.file)
                        sys.exit("Invalid Syntax: Expected \")\" after definition of function parameters.")
                else:
                    print("</class>", file = self.file)
                    sys.exit("Invalid Syntax: Expected \"(\" after subroutine name.")
            else:
                print("</class>", file = self.file)
                sys.exit("Invalid Syntax: Subroutine names cannot begin with a digit.")
        else:
            print("</class>", file = self.file)
            sys.exit("Invalid subrotuine type.")
        self.xmlIndentation -= 1
        print("\t" * self.xmlIndentation + "</subroutineDec>", file = self.file)
        return


    #Compiles the boday of a method, function or constructor.
    def compileSubroutineBody(self):
        print("\t" * self.xmlIndentation + "<subroutineBody>", file = self.file)
        self.xmlIndentation += 1
        if self.tokenizer.currentToken == "{":
            self.writeXml()
            self.tokenizer.advance()
            while self.tokenizer.currentToken != "return":
                if self.tokenizer.currentToken = "var":

            if self.tokenizer.currentToken == "}":
                self.writeXml()
                self.tokenizer.advance()

            else:
                print("</class>", file = self.file)
                sys.exit("Invalid Syntax: Expected \"}\" after return.")
        else:
            print("</class>", file = self.file)
            sys.exit("Invalid Syntax: Expected \"{\" after declaration of function.")
        while
        return
    #Compiles a (possibly empty) parameter list, not including the enclosing"()".
    def compileParameterList(self):
        print("\t" * self.xmlIndentation + "<parameterList>", file = self.file)
        self.xmlIndentation += 1

        while self.tokenizer.currentToken != ")":

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

    def writeXml(self):
        rep = {"<"  : "&lt;",
               ">"  : "$gt;",
               "\"" : "&quot;",
               "&"  : "&amp;"}
        rep = dict((re.escape(k), v) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        token = pattern.sub(lambda m: rep[re.escape(m.group(0))], self.tokenizer.currentToken)

        print("\t" * self.xmlIndentation + "<" + self.tokenizer.currentTokenType + "> " + token + " </" + self.tokenizer.currentTokenType + "> ", file = self.file)
