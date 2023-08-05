

class ParseGraph:

    def __init__(self):
        self.vertexSet = set()
        self.transitions = {}

    def vertexExists(self, vertex):
        if vertex == None:
            return False
        else:
            return vertex in self.vertexSet
    
    def addEdge(self, vertexA, pattern, vertexB):
        if self.addVertex(vertexA) and self.addVertex(vertexB):
            self.transitions[vertexA].add((pattern, vertexB))
            return True
        else:
            return False

    def removeEdge(self, vertexA, pattern, vertexB):
        try:
            if self.vertexExtists(vertexA):
                self.transitions[vertexA].remove((pattern, vertexB))
                if len(self.transitions[vertexA]) <= 0:
                    # clean up
                    self.removeVertex(vertexA)
            return True
        except:
            return False

    def addVertex(self, vertex):
        try:
            if not self.vertexExists(vertex):
                self.vertexSet.add(vertex)
                self.transitions[vertex] = set()
            return True
        except:
            return False

    def removeVertex(self, vertex):
        try:
            if self.vertexExtists(vertex):
                self.vertexSet.remove(vertex)
                del self.transitions[vertex]
            return True
        except:
            return False

    def getAttachedVertex(self, vertex):
        attached = set()
        for _, state in self.transitions[vertex]:
            attached.add(state)
        return attached

    def bfs(self, start, end):
        if self.vertexExists(start) and self.vertexExists(end):
            seen = set()
            queue = []
            queue.add(start)
            while len(queue) > 0:
                cur = queue.pop(0)
                if cur == end:
                    return True
                else:
                    unseen = seen ^ self.getAttachedVertex(cur)
                    if len(unseen) > 0:
                        queue.extend(unseen)
                        seen = seen | unseen
                    else:
                        continue
            return False
        else:
            return False

    def path(self, start, end=None):
        if end == None:
            return self.vertexExists(start) and len(self.transitions[start]) > 0
        else:
            return self.bfs(start, end)

    def getTransitions(self, curVertex):
        patterns = []
        states = []
        for pattern, state in self.transitions[curVertex]:
            patterns.append(pattern)
            states.append(state)
        return patterns, states

'''
Provides a Context to a Parse Graph

context is where to start and possible terminal verticies.

'''
class Grammar:

    def __init__(self, startState, endStates, graph):

        if isinstance(graph, ParseGraph):
            self.hidden = graph
        else:
            raise ValueError(f'passed {type(graph)} as graph parameter, when should be ParseGraph')

        if isinstance(endStates, list):
            self.terminals = set(endStates)
        elif isinstance(endStates, set):
            self.terminals = endStates
        elif isinstance(endStates, str):    #single hashable symbol
            self.terminals = set([endStates])
        else:
            raise ValueError(f'passed {type(endStates)} as endStates parameter, when should be list or set')

        joinSet = (self.terminals & graph.vertexSet) ^ self.terminals
        if len((self.terminals & graph.vertexSet) ^ self.terminals) > 0:
            raise ValueError(f'terminal state set is not a subset of graph vertex set')
        elif not startState in graph.vertexSet:
            raise ValueError(f'start state is not in the graph vertex set')
        elif not self.hidden.path(startState):
            raise ValueError(f'there is no path from the start state')
        else:
            self.start = startState
        
    def pathExists(self, all=True):
        if all:
            # Test if all terminals are reachable
            for end in self.terminals:
                if self.hidden.path(self.start, end):
                    continue
                else:
                    return False
            return True
        else:
            # Test if there exists at least one terminal is reachable
            for end in self.terminals:
                if self.hidden.path(self.start, end):
                    return True
                else:
                    continue
            return False

    def getPossibleNext(self, vertex):
        if vertex in self.terminals:
            return [], []
        elif self.hidden.vertexExists(vertex):
            return self.hidden.getTransitions(vertex)
        else:
            raise ValueError(f'vertex: {vertex} is not in Grammar')

    def getStart(self):
        return self.start
    
    def isTerminal(self, state):
        return state in self.terminals
        
        
            