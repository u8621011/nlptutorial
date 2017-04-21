import helper
import sys
import math
from collections import namedtuple
from a01 import TrainModel

class A03:
    def __init__ (self):
        self.logger = helper.GetMyLogger('A03', 'myapp.log')

    def buildGraph (self, model, sentance):
        self.logger.debug ('Building graph for sentance: {}'.format(sentance))

        slen = len(sentance)
        scoreUknown = -math.log(10/float(100000))

        graph = [None] * slen
        for i in range(slen):
            # add first edge (i, i+1)
            # add edge if the partial word can be found in dict
            for j in range(i+1, slen):
                subString = sentance[i:j]
                #self.logger.debug('substring[{}:{}]: {}'.format(i, j, subString))
                if subString in model:
                    p = model[subString]
                    score = -math.log(p)
                    edge = Edge(i, j, score)

                    self.logger.debug('new edge found, str:{}, edge:{}'.format(subString, edge))
                    curEdges = graph[j]
                    if curEdges == None:
                        graph[j] = [edge]
                    else:
                        curEdges.append(edge)
                elif len(subString) == 1:
                    edge = Edge(i, j, scoreUknown)
                    self.logger.debug('add unknown word edge, str:{}, edge:{}'.format(subString, edge))
                    curEdges = graph[j]
                    if curEdges == None:
                        graph[j] = [edge]
                    else:
                        curEdges.append(edge)

        self.logger.info ('Graph built: {}'.format(graph))

        return graph
                
    def doViterbiSegmentation (self, model, line):
        sentance = line.strip()
        slen = len(sentance)

        nodeBestScore = [None for i in range(slen+1)]
        nodeBestEdge = [None for i in range(slen+1)]

        graph = self.buildGraph(model, line)

        # forward steps
        nodeBestScore[0] = 0
        for i in range(1, slen+1):
            curNodeIncomingEdges = graph[i]
            if curNodeIncomingEdges != None:
                for curEdge in curNodeIncomingEdges:
                    if nodeBestScore[i] == None:
                        if nodeBestScore[curEdge.S] == None:
                            nodeBestScore[i] = curEdge.Score
                        else:
                            nodeBestScore[i] = nodeBestScore[curEdge.S] + curEdge.Score
                        nodeBestEdge[i] = curEdge
                    else:
                        if nodeBestScore[curEdge.S] == None:
                            curScore = curEdge.Score
                        else:
                            curScore = nodeBestScore[curEdge.S] + curEdge.Score
                        if curScore < nodeBestScore[i]:
                             nodeBestScore[i] = curScore
                             nodeBestEdge[i] = curEdge


        self.logger.debug('Best scores: {}'.format(nodeBestScore))
        self.logger.debug('Best edges: {}'.format(nodeBestEdge))

        # backward steps
        bestPath = []
        curBestEdge = nodeBestEdge[slen]
        while curBestEdge != None:
            bestPath.append(curBestEdge)
            curBestEdge = nodeBestEdge[curBestEdge.S]

        self.logger.debug('Best Path: {}'.format(bestPath))
        tokens = []
        for curEdge in reversed(bestPath):
            sub = sentance[curEdge.S:curEdge.E]
            tokens.append(sub)

        self.logger.debug('Segment Result: {}'.format(' '.join(tokens)))

        return tokens

    def SegmentFile(self, model, segFile, outFile):
        sf = open(segFile, 'r', encoding='utf8')
        of = open(outFile, 'w', encoding='utf8')

        lines = sf.readlines()
        for curLine in lines:
            tokens = self.doViterbiSegmentation (model, curLine)
            of.write(" ".join(tokens))
            of.write('\n')

        sf.close()
        of.close()

if __name__ == '__main__':
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
        TrainModel(file1, file2)

    elif mode == 'seg':
        if len(sys.argv) != 5:
            print("""execute format:
            python a03.py train {input_file} {output_file}
            python a03.py seg {trained_model_file} {segmenting_file} {segment_result_file}
            """)
            exit(0)

        o = A03()
        file3 = sys.argv[4]
        model = helper.LoadModel(file1)

        Edge = namedtuple('Edge', ['S', 'E', 'Score'])
        o.SegmentFile(model, file2, file3)
    else:
        print('Unknown execution mode')



