import helper
import sys
from collections import namedtuple

def buildGraph (model, sentance):
    slen = len(sentance)

    graph = []
    for i in range(slen):
        edges = []
        # add edge if the partial word can be found in dict
        for j in range(1, slen):
            subString = sentance[i:j]
            if subString in model:
                p = model[subString]
                edge = Edge(i, j, p)
                edges.append(edge)
                print('appending eage : {}'.format(edge))

        graph.append(edges)


    return graph
                
    

def doSegmentation (model, line):
    sentance = line.strip()
    slen = len(sentance)

    nodeBestScore = [None for i in range(slen+1)]
    nodeBestEdge = [None for i in range(slen+1)]

    graph = buildGraph(model, line)

    print(graph)
    

def SegmentFile(model, segFile, outFile):
    sf = open(segFile, 'r', encoding='utf8')
    of = open(outFile, 'w', encoding='utf8')

    lines = sf.readlines()
    for curLine in lines:
        tokens = doSegmentation (model, curLine)
        #of.write(" ".join(tokens))

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
    
    file3 = sys.argv[4]
    model = helper.LoadModel(file1)

    Edge = namedtuple('Edge', ['S', 'E', 'P'])
    SegmentFile(model, file2, file3)
else:
    print('Unknown execution mode')



