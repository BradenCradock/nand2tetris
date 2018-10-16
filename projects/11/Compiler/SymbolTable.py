import sqlite3

class SymbolTable:

    def __init__(self):

        self.symbolTable = sqlite3.connect(':memory:')
        self.tableCursor = self.symbolTable.cursor()
        self.createTable("class")
        self.createTable("subroutine")
        self.index = {
            "STATIC"    : 0
            "FIELD"     : 0
            "ARG"       : 0
            "VAR"       : 0
        }
        self.scope = "class"

    def createTable(self, cur, name):
        self.tableCursor.execute('''CREATE TABLE {}(
            _index INTEGER,
            name TEXT,
            type TEXT,
            kind TEXT)'''.format(name))


    #Starts a new subroutine scope (Resets the subroutine's symbol table)
    def startSubroutine(self):
        self.tableCursor.execute("DELETE FROM subroutine")
        self.index["ARG", "VAR"] = 0
        return

    #Defines a new identifier of a given name, type and kind and assigns it to a running index.
    #STATIC and FIELD identifiers have a class scope while ARG and VAR identifiers ahve a subroutine scope.
    def define(self, name, type, kind):
        if kind in {"STATIC", "FIELD"}:
            sql =   '''INSERT INTO class(_index, name, type, kind)
                    VALUES(?, ?, ?, ?)'''
            self.tableCursor.execute(sql, self.index[kind], name, type, kind)
            self.index[kind] += 1
            self.scope = "class"

        elif kind in {"ARG", "VAR"}:
            sql =   '''INSERT INTO subroutine(_index, name, type, kind)
                    VALUES(?, ?, ?, ?)'''
            self.tableCursor.execute(sql, self.index[kind], name, type, kind)
            self.index[kind] += 1
            self.scope = "subroutine"

        else:
            print("ERROR: INVALID KIND")

    #Returns the number of varibles of the given kind already defined in the current scope.
    def varCount(self, kind):
        return self.index[kind]

    #Returns the kinf of the named identifier in the current scope.
    #if the identifier is unknown in the current scope returns NONE.
    def kindOf(self, name):
        return self.tableCursor.execute('''SELECT kind FROM ? WHERE name = ?''', (self.scope, name,))

    #Returns the type of the named identifier in the current scope
    def typeOf(self, name):
        return self.tableCursor.execute('''SELECT type FROM ? WHERE name = ?''', (self.scope, name,))

    #Returns the index assigned to the named identifier
    def indexOf(self, name):
        return self.tableCursor.execute('''SELECT index FROM ? WHERE name = ?''', (self.scope, name,))
