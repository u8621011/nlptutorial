import logging

def GetMyLogger(loggerName, filename):
    logger = logging.getLogger(loggerName)
    hdlr = logging.FileHandler(filename, 'w', 'utf8')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.DEBUG)

    return logger
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
