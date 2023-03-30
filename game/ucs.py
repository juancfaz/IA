from search import SearchAlgorithm
from pq import PriorityQueue


class UniformCostSearch(SearchAlgorithm):
    def __init__(self, problem):
        super().__init__(problem)
        self.frontier = PriorityQueue()
        self.backrefs = {}
        self.frontier.update(self.startState, 0.0)

    def stateCost(self, state):
        return self.pastCosts.get(state, None)

    def path(self, state):
        path = []
        while state != self.problem.startState():
            _, prevState = self.backrefs[state]
            path.append(state)
            state = prevState
        path.reverse()
        return path

    def step(self):
        problem = self.problem
        startState = self.startState
        frontier = self.frontier
        backrefs = self.backrefs

        if self.actions:
            return self.path(problem.endState())

        state, pastCost = frontier.removeMin()
        if state is None and pastCost is None:
            return []

        self.pastCosts[state] = pastCost
        self.numStatesExplored += 1
        path = self.path(state)

        if problem.isEnd(state):
            self.actions = []
            while state != startState:
                action, prevState = backrefs[state]
                self.actions.append(action)
                state = prevState
            self.actions.reverse()
            self.pathCost = pastCost
            return path
        
        
        for action, newState, cost in problem.successorsAndCosts(state):
            if frontier.update(newState, pastCost + cost):
                backrefs[newState] = (action, state)
        return path
