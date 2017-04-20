import helper
import sys
import math
from collections import namedtuple

def buildGraph (model, sentance):
    print ('Building graph for sentance: {}'.format(sentance))

    slen = len(sentance)

    graph = [None] * slen
    for i in range(slen):
        # add first edge (i, i+1)
        # add edge if the partial word can be found in dict
        for j in range(i+1, slen):
            subString = sentance[i:j]
            print('substring[{}:{}]: {}'.format(i, j, subString))
            if subString in model:
                p = model[subString]
                score = -math.log(p)
                edge = Edge(i, j, score)

                curEdges = graph[j]
                if curEdges == None:
                    graph[j] = [edge]
                else:
                    curEdges.append(edge)

    print('Graph built: {}'.format(graph))

    return graph
                
def doViterbiSegmentation (model, line):
    sentance = line.strip()
    slen = len(sentance)

    nodeBestScore = [None for i in range(slen+1)]
    nodeBestEdge = [None for i in range(slen+1)]

    graph = buildGraph(model, line)

    # forward steps
    nodeBestScore[0] = 0
    for i in range(1, slen+1):
        curNodeIncomingEdges = graph[i]
        for curEdge in curNodeIncomingEdges:
            if nodeBestScore[i] == None:
                nodeBestScore[i] = nodeBestScore[curEdge.S] + curEdge.Score
                nodeBestEdge[i] = curEdge
            else:
                curScore = nodeBestScore[curEdge.S] + curEdge.Score
                if curScore < nodeBestScore[i]:
                     nodeBestScore[i] = curScore
                     nodeBestEdge[i] = curEdge

    print('Best scores: {}'.format(nodeBestScore))
    print('Best edges: {}'.format(nodeBestEdge))

    # backward steps
    bestPath = []
    curBestEdge = nodeBestEdge[slen]
    while curBestEdge != None:
        bestPath.append(curBestEdge)
        curBestEdge = nodeBestEdge[curBestEdge.S]

    print('Best Path: {}'.format(bestPath))
    tokens = []
    for curEdge in reversed(bestPath):
        sub = sentance[curEdge.S:curEdge.E]
        tokens.append(sub)

    print('Segment Result: {}'.format(' '.join(tokens)))

def SegmentFile(model, segFile, outFile):
    sf = open(segFile, 'r', encoding='utf8')
    of = open(outFile, 'w', encoding='utf8')

    lines = sf.readlines()
    for curLine in lines:
        tokens = doViterbiSegmentation (model, curLine)
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

    Edge = namedtuple('Edge', ['S', 'E', 'Score'])
    SegmentFile(model, file2, file3)
else:
    print('Unknown execution mode')



