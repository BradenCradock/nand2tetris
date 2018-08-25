#These 3 functions take a string/mnemonic and use this as a key to return the associated binary value
#Except the first one because I wanted to try something different
def dest(mnemonic):
    if mnemonic is not None:
        bits = 0b000
        if "M" in mnemonic:
            bits = bits ^ 0b001
        if "D" in mnemonic:
            bits = bits ^ 0b010
        if "A" in mnemonic:
            bits = bits ^ 0b100
        return format(bits, '03b')
    else:
        return "000"

def comp(mnemonic):
    if mnemonic is not None:
        compDict = {
            "0"     : "101010",
            "1"     : "111111",
            "-1"    : "111010",
            "D"     : "001100",
            "A"     : "110000",
            "!D"    : "001101",
            "!A"    : "110001",
            "-D"    : "001111",
            "-A"    : "110011",
            "D+1"   : "011111",
            "A+1"   : "110111",
            "D-1"   : "001110",
            "A-1"   : "110010",
            "D+A"   : "000010",
            "D-A"   : "010011",
            "A-D"   : "000111",
            "D&A"   : "000000",
            "D|A"   : "010101",
            "M"     : "110000",
            "!M"    : "110001",
            "-M"    : "110011",
            "M+1"   : "110111",
            "M-1"   : "110010",
            "D+M"   : "000010",
            "D-M"   : "010011",
            "M-D"   : "000111",
            "D&M"   : "000000",
            "D|M"   : "010101"
        }
        return compDict[mnemonic]
    else:
        return "000"

def jump(mnemonic):
    if mnemonic is not None:
        jumpDict = {
            "JGT"   : "001",
            "JEQ"   : "010",
            "JGE"   : "011",
            "JLT"   : "100",
            "JNE"   : "101",
            "JLE"   : "110",
            "JMP"   : "111"
        }
        return jumpDict[mnemonic]
    else:
        return "000"
