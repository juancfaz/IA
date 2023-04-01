from search import SearchAlgorithm

class DynamicProgrammingSearch(SearchAlgorithm):
    def __init__(self, problem):
        super().__init__(problem)
        self.fCosts = {}
        self.backrefs = {}
        self.futureQueue = [problem.endState()]
        self.currentState = problem.startState()
        self.finished = False

    def futureCosts(self):
        state = self.futureQueue.pop(0)

        if self.problem.isEnd(state):
            self.fCosts[state] = 0
            for _, previousState, _ in self.problem.successorsAndCosts(state):
                self.futureQueue.append(previousState)
        elif state not in self.fCosts:
            alreadyVisited = []
            for _, nextState, nextCost in self.problem.successorsAndCosts(state):
                if nextState in self.fCosts:
                    alreadyVisited.append((nextState, nextCost))
                else:
                    self.futureQueue.append(nextState)

            self.fCosts[state] = min(nextCost + self.fCosts[nextState] for nextState, nextCost in alreadyVisited)

    def stateCost(self, state):
        return self.fCosts.get(state, None)

    def path(self, state):
        path = []
        while state != self.problem.startState():
            _, prevState = self.backrefs[state]
            path.append(state)
            state = prevState
        path.reverse()
        return path

    def step(self):
        if self.finished:
            return self.path(self.currentState)

        self.numStatesExplored += 1
        path = self.path(self.currentState)

        if self.problem.isEnd(self.currentState):
            self.finished = True
            return path

        if self.currentState not in self.fCosts:
            while len(self.futureQueue) > 0:
                self.futureCosts()
            return path

        nextState = self.currentState
        for action, neighbour, _ in self.problem.successorsAndCosts(self.currentState):
            if self.fCosts[neighbour] < self.fCosts[nextState]:
                nextState = neighbour
                bestAction = action

        self.backrefs[nextState] = (bestAction, self.currentState)
        self.currentState = nextState
        return path
