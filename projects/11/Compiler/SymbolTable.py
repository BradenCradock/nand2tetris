import sqlite3

class SymbolTable:

    def __init__(self):

        self.symbolTable = sqlite3.connect(':memory:')
        self.tableCursor = self.symbolTable.cursor()
        self.createTable("class")
        self.createTable("subroutine")
        self.index = {
            "STATIC"    : 0,
            "FIELD"     : 0,
            "ARG"       : 0,
            "VAR"       : 0
        }
        self.scope = "class"

    def createTable(self, name):
        self.tableCursor.execute('''CREATE TABLE {}(
            _index INTEGER,
            name TEXT,
            type TEXT,
            kind TEXT)'''.format(name))


    #Starts a new subroutine scope (Resets the subroutine's symbol table)
    def startSubroutine(self):
        self.tableCursor.execute("DELETE FROM subroutine")
        self.index["ARG"] = 0
        self.index["VAR"] = 0
        return

    #Defines a new identifier of a given name, type and kind and assigns it to a running index.
    #STATIC and FIELD identifiers have a class scope while ARG and VAR identifiers ahve a subroutine scope.
    def define(self, name, type, kind):
        if kind in {"STATIC", "FIELD"}:
            sql =   '''INSERT INTO class(_index, name, type, kind)
                    VALUES(?, ?, ?, ?)'''
            self.tableCursor.execute(sql, (self.index[kind], name, type, kind))
            self.index[kind] += 1
            self.scope = "class"

        elif kind in {"ARG", "VAR"}:
            sql =   '''INSERT INTO subroutine(_index, name, type, kind)
                    VALUES(?, ?, ?, ?)'''
            self.tableCursor.execute(sql, (self.index[kind], name, type, kind))
            self.index[kind] += 1
            self.scope = "subroutine"

        else:
            print("ERROR: INVALID KIND " + kind)

    #Returns the number of varibles of the given kind already defined in the current scope.
    def varCount(self, kind):
        return self.index[kind]

    #Returns the kind of the named identifier in the current scope.
    #if the identifier is unknown in the current scope returns NONE.
    def kindOf(self, name):
        self.tableCursor.execute('''SELECT * FROM subroutine WHERE name = ?''', (name,))
        row = self.tableCursor.fetchone()
        if row is not None:
            return row[3]
        else:
            self.tableCursor.execute('''SELECT * FROM class WHERE name = ?''', (name,))
            row = self.tableCursor.fetchone()
            if row is not None:
                return row[3]
            else:
                return None

    #Returns the type of the named identifier in the current scope
    def typeOf(self, name):
        self.tableCursor.execute('''SELECT * FROM subroutine WHERE name = ?''', (name,))
        row = self.tableCursor.fetchone()
        if row is not None:
            return row[2]
        else:
            self.tableCursor.execute('''SELECT * FROM class WHERE name = ?''', (name,))
            row = self.tableCursor.fetchone()
            if row is not None:
                return row[2]
            else:
                return None

    #Returns the index assigned to the named identifier
    def indexOf(self, name):
        self.tableCursor.execute('''SELECT * FROM ''' + self.scope + ''' WHERE name = ?''', (name,))
        row = self.tableCursor.fetchone()
        if row is not None:
            return row[0]
        else:
            self.tableCursor.execute('''SELECT * FROM class WHERE name = ?''', (name,))
            row = self.tableCursor.fetchone()
            if row is not None:
                return row[0]
            else:
                return None

    def printTable(self, table):
        self.tableCursor.execute('''SELECT * FROM ''' + table)
        rows = self.tableCursor.fetchall()
        for row in rows:
            print(row)
