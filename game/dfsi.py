from search import SearchAlgorithm


class DepthFirstSearchIterative(SearchAlgorithm):
    def __init__(self, problem):
        super().__init__(problem)
        self.frontier = []
        self.BestPath = None
        self.BestCost = float('inf')
        self.encontro = False
        self.maxdeeplimit = 1
        self.pastCosts[self.startState] = 0
        self.visited = set()
        
    def stateCost(self, state):
        return self.pastCosts.get(state, None)

    def step(self):
        problem = self.problem
        startState = self.startState
        frontier = self.frontier
        
        if not frontier and self.BestPath is None:
            frontier.append([0, [startState]])
        
        if not frontier:
            return self.BestPath
        
        cost, path = frontier.pop()
        lastState = path[-1]
        
        if problem.isEnd(lastState):
            if cost < self.BestCost:
                self.BestCost = cost
                self.BestPath = path
            frontier.clear()
            return self.BestPath
        else:
            if len(path) < self.maxdeeplimit:
                for _, newState, newcost in problem.successorsAndCosts(lastState):
                    if newState not in self.visited:
                        self.visited.add(newState)
                        frontier.append([cost+newcost, path + [newState]])
                        self.pastCosts[newState] = self.pastCosts[lastState] + newcost
            else:
                frontier.clear()
                self.visited.clear()
                self.maxdeeplimit += 6
        
        if self.BestPath != None and frontier == []:
            print(f'BestCost: {self.BestCost}, BestPath: {self.BestPath}')
            return self.BestPath
        
        return path