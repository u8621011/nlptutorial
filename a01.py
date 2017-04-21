import sys
import math
import helper

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
    logger = helper.GetMyLogger('A01', 'myapp.log')
    fin = open(ifile, 'r', encoding='utf8')

    d = getTokenDict(fin)
    total = sum(d.values())
    model = {k: v/float(total) for k, v in d.items()}

    fout = open(ofile, 'w', encoding='utf8')

    for k, v in model.items():
        outString = "%s %s" % (k, v)
        
        logger.debug(outString)
        fout.write("%s\n" % outString)

    fin.close()
    fout.close()

    return model

def LoadModelFile (fmodel):
    f = open(fmodel, 'r', encoding='utf8')
    lines = f.readlines()

    model = dict()
    for curLine in lines:
        line = curLine.strip()
        tokens = line.split()

        model[tokens[0]] = float(tokens[1])

    f.close()
    return model

# return properbility of each lin
def CalcEntropyAndCoverage (model, lines):
    lamda1 = 0.95
    lamdaUnk = 1 - lamda1
    v = 1000000

    # statistic variables
    totalTokenCount = 0
    unknownCount = 0
    entropy = 0

    print('Calculating Entropy and coeverage')
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

            print('prop(%s) = %f, ' % (curToken, tokenProp))

            entropy -= math.log2(tokenProp)            

    coverage = (totalTokenCount-unknownCount) / float(totalTokenCount)
    entropy = entropy / totalTokenCount

    print("entropy: %f, coverage: %f" % (entropy, coverage))

    return {
        'Coverage': coverage,
        'Entropy': entropy
    }

if len(sys.argv) < 4:
    print("argv: %s" % sys.argv)
    print("""execute format:
    python a01.py train {input_file} {output_file}
    python a01.py test {trained_model_file} {test_file}
    """)
    exit(0)

mode = sys.argv[1]
file1 = sys.argv[2]
file2 = sys.argv[3]

if mode == 'train':
    TrainModel(file1, file2)
elif mode == 'test':
    model = LoadModelFile(file1)
    fTesting = open(file2, 'r', encoding='utf8')
    lines = fTesting.readlines()
    CalcEntropyAndCoverage(model, lines)
else:
    print('Unknown execution mode')