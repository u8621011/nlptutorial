import sys

if len(sys.argv) < 2:
    print("please input file to parse")
    exit(0)

filename = sys.argv[1]

f = open(filename, 'r', encoding='utf8')
lines = f.readlines()

dictTokens = dict()
for curLine in lines:
    line = curLine.strip()
    tokens = line.split(' ')

    for curToken in tokens:
        if curToken in dictTokens:
            dictTokens[curToken] += 1
        else:
            dictTokens[curToken] = 1

for k, v in dictTokens.items():
    print ("%s %s" % (k, v))

