import JackTokenizer
import SymbolTable
import VMWriter
import re
import sys
from functools import partial

class CompilationEngine:

    def __init__(self, inputFilepath, outputFilepath):
        self.tokenizer = JackTokenizer.JackTokenizer(inputFilepath)             #Tokenizer reads input .jack files and parses it for easy access to each token
        self.symbolTable = SymbolTable.SymbolTable()                            #The sumbolTable module uses SQL to store and access static, field, local and argument varibles
        self.xmlFile = open(outputFilepath + ".xml", "w+")
        self.writer = VMWriter.VMWriter(outputFilepath + ".vm")
        self.xmlIndentation = 0
        self.types = ["int", "boolean", "char"]
        self.className = ""
        self.subroutineName = ""
        self.subroutineReturnType = ""
        self.terms = []
        self.whileCounter = 0
        self.whiles = []
        self.ifCounter = 0
        self.ifs = []
        self.compileClass()

    #Replaces reserved symbols and encapsulates the current token in xml tags beofre writing it into an xml file
    def writeXml(self):
        rep = {"<"  : "&lt;",
               ">"  : "$gt;",
               "\"" : "&quot;",
               "&"  : "&amp;"}
        rep = dict((re.escape(k), v) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        token = pattern.sub(lambda m: rep[re.escape(m.group(0))], self.tokenizer.currentToken)

        print("\t" * self.xmlIndentation + "<" + self.tokenizer.currentTokenType + "> " + token + " </" + self.tokenizer.currentTokenType + "> ", file = self.xmlFile)

    #Modified XML writer that allows extra descritors for any identifiers
    def writeIdentifierXml(self, category, state, index):
        rep = { "<"  : "&lt;",
                ">"  : "$gt;",
                "\"" : "&quot;",
                "&"  : "&amp;"}
        rep = dict((re.escape(k), v) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        input = "Identifier: " + self.tokenizer.currentToken + "\n" +\
                "Category: " + category + "\n" +\
                "State: " + state + "\n" +\
                "Index: " + index
        output = pattern.sub(lambda m: rep[re.escape(m.group(0))], input)

        self.xmlOpenTag("Identifier")
        print("\t" * self.xmlIndentation + output, file = self.xmlFile)
        self.xmlCloseTag("Identifier")

    #Called whenever the compiler encounters a token the does not match the syntatic language
    def syntaxError(self, expected, recieved):
        self.xmlIndentation = 0
        self.xmlCloseTag("class")
        sys.exit("Invalid Syntax in " + self.className + ".jack, token number " + str(self.tokenizer.tokenCounter) + ": Expected " + str(expected) + " but recieved " + recieved)

    #Checks the current token agains a string or a list of strings
    def checkToken(self, string):
        if self.tokenizer.currentToken in string:
            self.writeXml()
            self.tokenizer.advance()
        else:
            self.syntaxError(string, self.tokenizer.currentToken)

    #This subroutine handles processing of any token of type IDENTIFIER.
    #If it is a varible it needs to be added to the symbol table.
    def checkIdentifier(self, type, category):

        if self.tokenizer.currentTokenType == "IDENTIFIER":
            if category in {"constructor", "function", "method", "void", "class"}:
                if type != "used":
                    type = "defined"
                self.writeIdentifierXml(category, type, "N/A")
                self.tokenizer.advance()

            elif category in {"field", "static", "var", "arg"}:
                if self.symbolTable.kindOf(self.tokenizer.currentToken) is None:
                    self.symbolTable.define(self.tokenizer.currentToken, type, category.upper())
                    type = "defined"
                else:
                    type = "used"
                self.writeIdentifierXml(category, type, str(self.symbolTable.indexOf(self.tokenizer.currentToken))) #
                self.tokenizer.advance()

        else:
            self.syntaxError("Function or Varible", self.tokenizer.currentTokenType)

    def xmlOpenTag(self, tag):
        print("\t" * self.xmlIndentation + "<" + tag + ">", file = self.xmlFile)
        self.xmlIndentation += 1

    def xmlCloseTag(self, tag):
        self.xmlIndentation -= 1
        print("\t" * self.xmlIndentation + "</" + tag + ">", file = self.xmlFile)

    #Compiles a complete class.
    def compileClass(self):
        self.tokenizer.advance()
        self.xmlOpenTag("class")

        self.checkToken("class")
        self.className = self.tokenizer.currentToken
        self.checkIdentifier("class", "class")
        self.checkToken("{")
        while self.tokenizer.currentToken not in {"}", "constructor", "function", "method", "void"} :
            self.compileClassVarDec()
        while self.tokenizer.currentToken != "}":
            self.compileSubroutineHeader()

        self.xmlCloseTag("class")

        self.writer.close()

    #Compiles a static or field declaration.
    def compileClassVarDec(self):
        self.xmlOpenTag("classVarDec")

        category = self.tokenizer.currentToken
        self.checkToken({"field", "static"})
        type = self.tokenizer.currentToken
        if self.tokenizer.currentTokenType == "IDENTIFIER":
            self.writeXml()
            self.tokenizer.advance()
        else:
            self.checkToken(self.types)
        self.checkIdentifier(type, category)
        while self.tokenizer.currentToken != ";":
            self.checkToken(",")
            self.checkIdentifier(type, category)
        self.checkToken(";")

        self.xmlCloseTag("classVarDec")

    #Compiles the declaration of a method, function or constructor.
    def compileSubroutineHeader(self):
        self.xmlOpenTag("subroutineDec")

        self.symbolTable.startSubroutine()
        self.subroutineCategory = self.tokenizer.currentToken
        if self.subroutineCategory == "method":
            self.symbolTable.define("this", self.className, "ARG")
        self.checkToken({"constructor", "function", "method", "void"})
        type = self.tokenizer.currentToken
        if self.tokenizer.currentTokenType == "IDENTIFIER":
            self.writeXml()
            self.tokenizer.advance()
        else:
            self.subroutineReturnType = self.tokenizer.currentToken
            self.checkToken(self.types + ["void"])                              #TODO: Change this to handle objects
        self.subroutineName = self.tokenizer.currentToken
        self.checkIdentifier(type, self.subroutineCategory)
        self.checkToken("(")
        self.compileParameterList()
        self.checkToken(")")
        self.compileSubroutineBody()
        self.xmlCloseTag("subroutineDec")

    #Compiles the body of a method, function or constructor.
    def compileSubroutineBody(self):
        self.xmlOpenTag("subroutineBody")

        self.checkToken("{")
        nLocals = 0
        while self.tokenizer.currentToken not in {"let", "if", "while", "do", "return"}:
            nLocals += self.compileVarDec()
        self.writer.writeFunction(self.className + "." + self.subroutineName, nLocals)
        if self.subroutineCategory == "method":
            self.writer.writePush("argument", 0)
            self.writer.writePop("pointer", 0)
        elif self.subroutineCategory == "constructor":
            self.pushTerm(str(self.symbolTable.varCount("FIELD")))
            self.writer.writeCall("Memory.alloc", 1)
            self.writer.writePop("pointer", 0)
        self.compileStatements()
        self.checkToken("}")

        self.xmlCloseTag("subroutineBody")

    #Compiles a (possibly empty) parameter list, not including the enclosing"()".
    def compileParameterList(self):
        if self.tokenizer.currentToken != ")":
            self.xmlOpenTag("parameterList")
            type = self.tokenizer.currentToken
            if self.tokenizer.currentTokenType == "IDENTIFIER":
                self.writeXml()
                self.tokenizer.advance()
            else:
                self.checkToken(self.types)
            self.checkIdentifier(type, "arg")
            while self.tokenizer.currentToken != ")":
                self.checkToken(",")
                type = self.tokenizer.currentToken
                self.writeXml()
                self.tokenizer.advance()
                self.checkIdentifier(type, "arg")

            self.xmlCloseTag("parameterList")

    #Compiles a var declaration.
    def compileVarDec(self):
        self.xmlOpenTag("varDec")

        self.checkToken("var")
        type = self.tokenizer.currentToken
        if self.tokenizer.currentTokenType == "IDENTIFIER":
            self.writeXml()
            self.tokenizer.advance()
        else:
            self.checkToken(self.types)
        self.checkIdentifier(type, "var")
        nVars = 1
        while self.tokenizer.currentToken != (";"):
            self.checkToken(",")
            self.checkIdentifier(type, "var")
            nVars += 1
        self.checkToken(";")

        self.xmlCloseTag("varDec")

        return nVars

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
        while self.tokenizer.currentToken != "}":
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
        self.writer.writePop("temp", 0)
        self.checkToken(";")

        self.xmlCloseTag("doStatement")

    #Compiles a let statement.
    def compileLet(self):
        self.xmlOpenTag("letStatement")

        self.checkToken("let")
        varName = self.tokenizer.currentToken
        self.checkIdentifier("var", "var")
        if self.tokenizer.currentToken == "[":
            self.checkToken("[")
            self.compileExpression()
            self.checkToken("]")
        self.checkToken("=")
        self.compileExpression()
        if self.terms:
            self.pushTerm(self.terms.pop())

        termKindDict = {
            "ARG"   : "argument",
            "VAR"   : "local",
            "STATIC": "static",
            "FIELD" : "this"
        }
        if self.symbolTable.kindOf(varName) is not None:
            self.writer.writePop(termKindDict[self.symbolTable.kindOf(varName)], self.symbolTable.indexOf(varName))

        self.checkToken(";")

        self.xmlCloseTag("letStatement")

    #Compiles a while statement.
    def compileWhile(self):
        self.xmlOpenTag("whileStatement")

        self.writer.writeLabel("WHILE_EXP" + str(self.whileCounter))
        self.whiles.append(self.whileCounter)
        self.whileCounter += 1

        self.checkToken("while")
        self.checkToken("(")
        self.compileExpression()
        if self.terms:
            self.pushTerm(self.terms.pop())
        self.writer.writeArithmetic("not")
        self.writer.writeIf("WHILE_END" + str(self.whiles[-1]))
        self.checkToken(")")
        self.checkToken("{")
        self.compileStatements()
        self.checkToken("}")
        self.writer.writeGoto("WHILE_EXP" + str(self.whiles[-1]))
        self.writer.writeLabel("WHILE_END" + str(self.whiles.pop()))

        self.xmlCloseTag("whileStatement")

    #Compiles a return statement.
    def compileReturn(self):
        self.xmlOpenTag("returnStatement")

        self.checkToken("return")
        if self.tokenizer.currentToken != ";":
            self.compileExpression()
            self.pushTerm(self.terms.pop())
        else:
            self.pushTerm("0")
        self.checkToken(";")
        self.writer.writeReturn()

        self.xmlCloseTag("returnStatement")

    #Compiles an if statement, possibly with a trailing else clause.
    def compileIf(self):
        self.xmlOpenTag("ifStatement")

        self.ifs.append(self.ifCounter)
        self.ifCounter += 1

        self.checkToken("if")
        self.checkToken("(")
        self.compileExpression()
        if self.terms:
            self.pushTerm(self.terms.pop())
        self.writer.writeArithmetic("not")
        self.writer.writeIf("IF_TRUE" + str(self.ifs[-1]))
        self.checkToken(")")
        self.checkToken("{")
        self.compileStatements()
        self.checkToken("}")
        self.writer.writeGoto("IF_FALSE" + str(self.ifs[-1]))
        self.writer.writeLabel("IF_TRUE" + str(self.ifs[-1]))
        if self.tokenizer.currentToken == "else":
            self.checkToken("else")
            self.checkToken("{")
            self.compileStatements()
            self.checkToken("}")
        self.writer.writeLabel("IF_FALSE" + str(self.ifs.pop()))
        self.xmlCloseTag("ifStatement")

    #Compiles an expression.
    def compileExpression(self):

        self.xmlOpenTag("expression")

        self.compileTerm()
        while self.tokenizer.currentToken not in {"]", ")", ";", ",", "("}:
            operator = self.tokenizer.currentToken
            self.checkToken({"+", "-", "*", "/", "&", "|", ">", "<", "="})
            self.compileTerm()
            self.compileOperator(operator)

        self.xmlCloseTag("expression")

    #Evaluates and compiles an expression
    def compileOperator(self, operator):

        operatorDictionary = {
            "+" : "add",
            "-" : "sub",
            "=" : "eq",
            ">" : "gt",
            "<" : "lt",
            "&" : "and",
            "|" : "or",
        }

        term2 = self.terms.pop()
        term1 = self.terms.pop()

        if operator in {"+", "-", "*", "/"} and term1.isdigit() and term2.isdigit():
            self.terms.append(str(eval(term1 + operator + term2)))
            return

        self.pushTerm(term1)
        self.pushTerm(term2)

        self.terms.append(" ".join((term1, operator, term2)))
        if operator == "*":
            self.writer.writeCall("Math.multiply", 2)
        elif operator == "/":
            self.writer.writeCall("Math.divide", 2)
        else:
            self.writer.writeArithmetic(operatorDictionary[operator])

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
            varName = self.tokenizer.currentToken
            if self.tokenizer.currentToken == "[":                              #Identifier is an array
                self.checkIdentifier("used", "var")
                self.checkToken("[")
                self.compileExpression()
                self.checkToken("]")
            elif self.symbolTable.kindOf(varName) is not None:        #Identifier is a varible or object
                self.checkIdentifier("used", "var")
                if self.tokenizer.currentToken == ".":                          #Variable is an object
                    self.compileSubroutineCall(varName)
                else:
                    self.terms.append(varName)
            else:                                                               #Identifier is a subroutine call
                self.checkIdentifier("used", "function")
                self.compileSubroutineCall(varName)

        elif self.tokenizer.currentToken in {"-", "~"}:                         #Term is a Unary op
            operator = self.tokenizer.currentToken
            self.checkToken({"-", "~"})
            self.compileTerm()
            term = self.terms.pop()
            self.pushTerm(term)
            if operator == "-":                                                 #The term following the unary op needs to be operated on by the unary op before performing other operations
                self.writer.writeArithmetic("neg")
                if term.isdigit():
                    self.terms.append(str(int(term) * -1))                      #Manipulating the term if it is a number allows the compiler to remove instructions if the next term is also a number
                else:
                    self.terms.append(term)
            else:
                self.writer.writeArithmetic("not")
                if term.isdigit():
                    self.terms.append(str(~int(term)))
                else:
                    self.terms.append(term)


        elif self.tokenizer.currentToken == "(":                                #Parenthesis indicated nested expressions
            self.checkToken("(")
            self.compileExpression()
            self.checkToken(")")

        elif self.tokenizer.currentToken not in invalidKeywords:                #Terms is a number/string/bool etc
            self.writeXml()
            self.terms.append(self.tokenizer.currentToken)
            self.tokenizer.advance()

        else:
            self.syntaxError("One of (true, false, null, this)", self.tokenizer.currentToken)

        self.xmlCloseTag("term")

    #Compiles a subroutine call
    def compileSubroutineCall(self, name):
        self.xmlOpenTag("subroutineCall")

        nArgs = 0
        if self.tokenizer.currentToken == ".":
            if self.symbolTable.kindOf(name) is not None:       #If the call is for a method the object needs to be pushed first
                if self.symbolTable.kindOf(name) != self.className:
                    self.pushTerm(name)
                else:
                    self.pushTerm("this")
                name = self.symbolTable.typeOf(name)
                nArgs += 1
            self.checkToken(".")
            name = name + "." + self.tokenizer.currentToken
            self.checkIdentifier("used", "function")
        else:
            self.pushTerm("this")
            name = self.className + "." + name
            nArgs += 1
        self.checkToken("(")
        nArgs += self.compileExpressionList()
        self.checkToken(")")
        self.writer.writeCall(name, nArgs)

        self.xmlCloseTag("subroutineCall")

    #Compiles a (possibily empty) comma-seperated list of expressions.
    def compileExpressionList(self):
        nExp = 0
        self.xmlOpenTag("expressionList")

        if self.tokenizer.currentToken != ")":
            self.compileExpression()
            self.pushTerm(self.terms.pop())
            nExp = 1
        while self.tokenizer.currentToken != ")":
            self.checkToken(",")
            self.compileExpression()
            self.pushTerm(self.terms.pop())
            nExp += 1

        self.xmlCloseTag("expressionList")

        return nExp

    def pushTerm(self, term):
        termKindDict = {
            "ARG"   : "argument",
            "VAR"   : "local",
            "STATIC": "static",
            "FIELD" : "this"
        }
        if term == "this":
            self.writer.writePush("pointer", 0)
        elif self.symbolTable.kindOf(term) is not None:
            self.writer.writePush(termKindDict[self.symbolTable.kindOf(term)], self.symbolTable.indexOf(term))
        elif term.isdigit():
            self.writer.writePush("constant", term)
        elif term == "true":
            self.writer.writePush("constant", 1)
            self.writer.writeArithmetic("neg")
        elif term ==  "false":
            self.writer.writePush("constant", 0)
