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

def doTrain(ifile, ofile):
    fin = open(ifile, 'r', encoding='utf8')

    d = getTokenDict(fin)
    total = sum(d.values())
    p = {k: v/float(total) for k, v in d.items()}

    fout = open(ofile, 'w', encoding='utf8')

    for k, v in p.items():
        outString = "%s %s" % (k, v)
        print(outString)
        fout.write("%s\n" % outString)

    fin.close()
    fout.close()

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
    doTrain(ifile, ofile)
elif mode == 'test':
    doTest()
else:
    print('Unknown execution mode')