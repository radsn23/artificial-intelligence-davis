import argparse
import numpy as np
import math
from collections import defaultdict

class Graph:
    """
    Class to take in the inputs and generate an IDDFS
    """
    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)
        self.result = []

    def addEdge(self,u,v):
        self.graph[u].append(v)

    def DepthLimitedSearch(self,source, target, maxDepth, valueMap):
        #print(max(valueMap[source][0]), target,"whatt")
        if max(valueMap[source][0])<=target:
            return [self.result,True]
        if maxDepth < 0:
            return ['No Solution',False]
        #self.result = [source]
        for i in self.graph[source]:
            if self.DepthLimitedSearch(i, target, maxDepth-1, valueMap)[1]:
                self.result.append(i)
                #print(self.result)
                return [self.result,True]
        #self.result=[]
        return ['Not exist',False]

    def IDDFS(self, source, target, maxDepth, valueMap):
        for i in range(maxDepth):
            #print(source, target, i)
            #print(self.DepthLimitedSearch(source, target, i, valueMap)[0])
            if self.DepthLimitedSearch(source, target, i, valueMap)[1]:
                #print(self.DepthLimitedSearch(source, target,i,valueMap)[0])
                return True
        return False

def testIDDFS():
    """
    Unit testing for IDDFS, not required in task workflow
    """
    g = Graph(7)
    g.addEdge(0,1)
    g.addEdge(0,2)
    g.addEdge(1,3)
    g.addEdge(3,4)
    g.addEdge(4,5)
    g.addEdge(3,6)

    target=6
    maxDepth=3
    source=0
    if g.IDDFS(source, target, maxDepth):
        print(g.result)
        print('possible')
    else:
        print('not possible')

def find_num_of_vertices(depth, branches):
    verts = 0
    for i in range(depth+1):
        verts+= pow(branches,i)
    return verts

def fast_level(idx,base):
    """
    Quick function to return any vertex's depth in a tree
    """
    return math.ceil(math.log((idx+1)*2+1, base))

def create_value_map(treeDict ,lengths, speeds):
    """
    Function to calculate the times and values for each path in the tree created above
    """
    valueDict = defaultdict(list)
    valueDict[0] = [[0]*len(speeds),[0]*len(speeds)]
    #print("aaaa",valueDict[0][0])
    for node in treeDict:
        #print(node, fast_level(node,3)-1)
        depth = fast_level(node,len(speeds)+1)-1
        times = lengths[depth]/np.array(speeds)
        sums = np.array([0]*len(speeds))
        sums = (np.reshape(sums, (-1,len(speeds))))
        lens = np.append(np.diag(times*np.array(speeds)),sums,axis=0)
        #print(lens)
        times = (np.append(np.diag(times),sums,axis=0))
        #vals = np.append(times,lens, axis=0)
        #print(times)
        for i in range(len(treeDict[node])):
            #print(np.array(valueDict[node][0]), times[i])
            valueDict[treeDict[node][i]].append((valueDict[node][0]+\
                    times[i]).tolist())
            valueDict[treeDict[node][i]].append((valueDict[node][1]+\
                    lens[i]).tolist())
    return valueDict

if __name__=="__main__":
    #testIDDFS()
    parser = argparse.ArgumentParser()
    parser.add_argument('--file','-f',type=str, required=True,help='add \
            plaintext input file for scheduling in the right format')
    args = parser.parse_args()

    with open(args.file,'r') as inputfile:
        data = inputfile.read().splitlines()

    [length_of_tasks, speed_of_tasks, targets] = [[float(numeric_d) \
            for numeric_d in d.split()] for d in data]
    length_of_tasks= sorted(length_of_tasks, reverse=True)
    print('lengths, speeds, targets')
    print(length_of_tasks, speed_of_tasks, targets)
    print('------------------------')
    #tree = defaultdict(list)
    value_map = defaultdict(list)
    root = 0
    depth = len(length_of_tasks)
    branches = len(speed_of_tasks)+1
    numVertices = find_num_of_vertices(depth, branches)

    t = Graph(numVertices)
    for i in range(math.floor((numVertices)/branches)):
        for b in range(1,branches+1):
            t.addEdge(i, branches*i+b)
    #print(t.graph)

    valueMap = create_value_map(t.graph, length_of_tasks, speed_of_tasks)
    #print(valueMap)
    length_target_lower = targets[1]
    time_target_upper = targets[0]
    nodes_to_start = [key for key,val in valueMap.items() if sum(val[1])>=length_target_lower]
    solution_leaf = ([node for node in nodes_to_start \
            if t.IDDFS(node, time_target_upper, 5,valueMap)] )
    if not solution_leaf:
        print('No solution')
    else:
         key = solution_leaf[0]
         path = []
         while key>0:
             for k, v in t.graph.items():
                 if key in v:
                     path.append((v.index(key)+1)%(branches))
                     break
             key = k
         if len(path)<depth:
            path = [0]*(depth-len(path))+path
         print('Solution-')
         print(path)
