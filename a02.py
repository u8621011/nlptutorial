import sys
import math

def TrainBigramModel(ifile, ofile):
    fin = open(ifile, 'r', encoding='utf8')

    tokenCounts = dict()
    model = dict()
    tokenTotalCount = 0
    unigramTotalCount = 0
    lines = fin.readlines()
    for curLine in lines:
        line = curLine.strip()
        tokens = line.split()
        tokens.insert (0, '<s>')
        tokens.append('</s>')

        # placeholder of bigram tokens
        tokenWindow = []
        while len(tokens) > 0:
            curToken = tokens.pop(0)

            tokenTotalCount += 1
            # we still dont understand why unigram not include <s> but n-gram include?
            if curToken != '<s>':
                unigramTotalCount += 1

            tokenWindow.append(curToken)

            # calc for unigram
            if curToken in tokenCounts:
                tokenCounts[curToken] += 1
            else:
                tokenCounts[curToken] = 1

            # calc for bigram
            if (len(tokenWindow) > 2):
                tokenWindow.pop(0)
            bigramString = " ".join(tokenWindow)
            if bigramString in tokenCounts:
                tokenCounts[bigramString] += 1
            else:
                tokenCounts[bigramString] = 1

    for k, v in tokenCounts.items():
        keyTokens = k.split()
        if len(keyTokens) == 1:
            # unigram model properbility
            if k != '<s>':
                model[k] = v / float(unigramTotalCount)
        else:
            # bigram model properbility
            tokenHead = keyTokens[0]
            model[k] = float(v) / tokenCounts[tokenHead]

    fout = open(ofile, 'w', encoding='utf8')
    for k, v in model.items():
        outString = "%s %f" % (k, v)
        print(outString)
        fout.write("%s\n" % outString)

    fin.close()
    fout.close()

    return tokenCounts

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

def CalcBigramProp (model, filename):
    # entropy calc properties
    v = 1000000
    lamda1 = 0.95
    lamda2 = 1 - lamda1

    ofile = open(filename, 'r', encoding='utf8')

    lines = ofile.readlines()

    Entropy = 0
    BigramCount = 0
    for curLine in lines:
        line = curLine.strip()
        tokens = line.split()

        tokens.insert(0, '<s>')
        tokens.append('</s>')

        propTokenBigram = 0.0
        propTokenLast = 0.0
        for i in range(len(tokens) - 1):
            tokenBigram = tokens[i] + ' ' + tokens[i+1]
            tokenLast = tokens[i + 1]
            # calc unigram properbility
            if tokenLast in model:
                propTokenLast = model[tokenLast]
            p1 = lamda1 * propTokenLast + lamda2 / float(v)

            # calc bigram properbility
            if tokenBigram in model:
                propTokenBigram = model[tokenBigram]
            p2 = lamda1 * propTokenBigram + lamda2 * p1

            Entropy += -math.log2(p2)
            BigramCount += 1

    Entropy = Entropy / BigramCount
    print('Entropy: %f' % Entropy)
    return Entropy

def DoTest(modelFIle, testFile):
    model = LoadModel(modelFIle)

    CalcBigramProp(model, testFile)
    return 
    
if len(sys.argv) < 4:
    print("""execute format:
    python a02.py train {input_file} {output_file}
    python a02.py test {trained_model_file} {test_file}
    """)
    exit(0)

mode = sys.argv[1]
file1 = sys.argv[2]
file2 = sys.argv[3]

if mode == 'train':
    TrainBigramModel(file1, file2)
elif mode == 'test':
    DoTest(file1, file2)
else:
    print('Unknown execution mode')