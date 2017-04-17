import sys

def TrainBigramModel(ifile, ofile):
    fin = open(ifile, 'r', encoding='utf8')

    tokenCounts = dict()
    model = dict()
    tokenTotalCount = 0
    lines = fin.readlines()
    for curLine in lines:
        line = curLine.strip()
        tokens = line.split()
        tokens.insert (0, '<s>')
        tokens.append('</s>')

        # placeholder of bigram tokens
        tokenWindow = []
        while len(tokens) > 0:
            tokenTotalCount += 1
            curToken = tokens.pop(0)
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
            model[k] = v / float(tokenTotalCount)
        else:
            # bigram model properbility
            tokenHead = keyTokens[0]
            model[k] = float(v) / tokenCounts[tokenHead]

    fout = open('ofile', 'w', encoding='utf8')
    for k, v in model.items():
        outString = "%s %s" % (k, v)
        print(outString)
        fout.write("%s\n" % outString)

    fin.close()
    fout.close()

    return tokenCounts

if len(sys.argv) < 4:
    print("""execute format:
    python a02.py train {input_file} {output_file}
    python a02.py test {trained_model_file} {test_file}
    """)
    exit(0)

mode = sys.argv[1]
ifile = sys.argv[2]
ofile = sys.argv[3]

if mode == 'train':
    TrainBigramModel(ifile, ofile)
elif mode == 'test':
    doTest()
else:
    print('Unknown execution mode')