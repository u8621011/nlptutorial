
def LoadModel(filename):
    fin = open(filename, 'r', encoding='utf8')
    lines = fin.readlines()

    model = dict()
    for curLine in lines:
        line = curLine.strip()
        tokens = line.split()

        popToken = tokens.pop()
        model[" ".join(tokens)] = float(popToken)

    fin.close()

    return model
