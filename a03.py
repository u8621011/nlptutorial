import helper

def doSegmentation (model, line):
    Edge = namedtuple('Edge', ['StartNode', 'EndNode'])
    sentance = line.strip()
    tokens = sentance.split()
    tokenCount = len(tokens)
    
    nodeBestScore = [None for i in range(tokenCount+1)]
    nodeBestEdge = [None for i in range(tokenCount+1)]


    

def SegmentFile(model, segFile, outFile):
    sf = open(segFile, 'r', encoding='utf8')
    of = open(outFile, 'w', encoding='utf8')

    lines = sf.readlines()
    for curLine in lines:
        tokens = doSegmentation (model, curLine)
        of.write(" ".join(tokens))

    sf.close()
    of.close()

if len(sys.argv) < 4:
    print("""execute format:
    python a03.py train {input_file} {output_file}
    python a03.py seg {trained_model_file} {segmenting_file} {segment_result_file}
    """)
    exit(0)

mode = sys.argv[1]
file1 = sys.argv[2]
file2 = sys.argv[3]

if mode == 'train':
    TrainBigramModel(file1, file2)
elif mode == 'seg':
    if len(sys.argv) != 5:
        print("""execute format:
        python a03.py train {input_file} {output_file}
        python a03.py seg {trained_model_file} {segmenting_file} {segment_result_file}
        """)
        exit(0)
    
    file3 = sys.args[4]
    model = helper.LoadModel(file1)

    SegmentFile(model, file2, file3)
else:
    print('Unknown execution mode')



