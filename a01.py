import sys

def getTokenDict (fin):
    lines = fin.readlines()
    dictTokens = dict()
    for curLine in lines:
        line = curLine.strip()
        tokens = line.split(' ')

        for curToken in tokens:
            if curToken in dictTokens:
                dictTokens[curToken] += 1
            else:
                dictTokens[curToken] = 1

        # the </s> calc
        if "</s>" in dictTokens:
            dictTokens["</s>"] += 1
        else:
            dictTokens["</s>"] = 1

    return dictTokens

def TrainModel(ifile, ofile):
    fin = open(ifile, 'r', encoding='utf8')

    d = getTokenDict(fin)
    total = sum(d.values())
    model = {k: v/float(total) for k, v in d.items()}

    fout = open(ofile, 'w', encoding='utf8')

    for k, v in model.items():
        outString = "%s %s" % (k, v)
        print(outString)
        fout.write("%s\n" % outString)

    fin.close()
    fout.close()

    return model

# return properbility of each lin
def DoEntropy (model, lines):
    lamda1 = 0.95
    lamdaUnk = 1 - lamda1
    v = 1000000

    # statistic variables
    totalTokenCount = 0
    unknownCount = 0
    dictTokenProps = dict()

    # calc token total count
    unkProp = lamdaUnk / v
    for curLine in lines:
        line = curLine.strip()
        tokens = line.split()
        # include end of sentance symbo </s>
        tokens.append('</s>')

        # calc properbility of each token
        for curToken in tokens:
            totalTokenCount += 1
            tokenProp = unkProp
            if curToken in model:
                tokenProp += model[curToken] * lamda1
            else:
                unknownCount += 1

            if curToken in dictTokenProps:
                dictTokenProps[curToken] += tokenProp
            else:
                dictTokenProps[curToken] = tokenProp


    return {
        'TotalCount': totalTokenCount,
        'UnknownCount': unknownCount,
        'LogLikes': logLikes
    }

if len(sys.argv) < 4:
    print("""execute format:
    python a01.py train {input_file} {output_file}
    python a01.py test {trained_model_file} {test_file}
    """)
    exit(0)

mode = sys.argv[1]
ifile = sys.argv[2]
ofile = sys.argv[3]

if mode == 'train':
    TrainModel(ifile, ofile)
elif mode == 'test':
    doTest()
else:
    print('Unknown execution mode')