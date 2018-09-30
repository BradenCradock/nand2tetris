import sys
import JackTokenizer
import os
import re
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


def writeXml(file, tokenType, token):
    rep = {"<"  : "&lt;",
           ">"  : "$gt;",
           "\"" : "&quot;",
           "&"  : "&amp;"}
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    token = pattern.sub(lambda m: rep[re.escape(m.group(0))], token)

    print(" <" + tokenType + "> " + token + " </" + tokenType + "> ", file = file)

def main():
    root = Tk()
    root.withdraw()
    filePath =  filedialog.askopenfilename(initialdir = "/", title = "Select a file", filetypes = (("jack files","*.jack"), ("all files","*.*")))

    tokenizer = JackTokenizer.JackTokenizer(filePath)

    xmlFile = open(filePath[:-4] + ".xml", "w+")
    print("<tokens>", file = xmlFile)
    while tokenizer.hasMoreTokens():

        tokenizer.advance()
        tokenType = tokenizer.tokenType()
        if tokenType == "KEYWORD":
            writeXml(xmlFile, tokenType, tokenizer.keyWord())
        elif tokenType == "SYMBOL":
            writeXml(xmlFile, tokenType, tokenizer.symbol())
        elif tokenType == "IDENTIFIER":
            writeXml(xmlFile, tokenType, tokenizer.identifier())
        elif tokenType == "INT_CONST":
            writeXml(xmlFile, tokenType, tokenizer.intVal())
        elif tokenType == "STRING_CONST":
            writeXml(xmlFile, tokenType, tokenizer.stringVal())

    print("</tokens>", file = xmlFile)

if __name__ == "__main__":
    main()
