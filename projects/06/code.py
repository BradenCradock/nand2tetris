def dest(mnemonic):
    bits = 0b000
    if "M" in mnemonic:
        bits = bits ^ 0b001
    if "D" in mnemonic:
        bits = bits ^ 0b010
    if "A" in mnemonic:
        bits = bits ^ 0b100
    return format(bits, '03b')

def comp(mnemonic):
    bits = 0b0000000
    compDict = {











    }

    return format(bits, '07b')
    return bits

def jump(mnemonic):
    bits = 0b000
    if "M" in mnemonic:
        bits = bits ^ 0b001
    if "D" in mnemonic:
        bits = bits ^ 0b010
    if "A" in mnemonic:
        bits = bits ^ 0b100
    return format(bits, '03b')
    return bits
