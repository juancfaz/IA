from search import SearchAlgorithm
from pq import PriorityQueue


class AstarSearch(SearchAlgorithm):
    def __init__(self, problem):
        super().__init__(problem)
        self.frontier = PriorityQueue()
        self.backrefs = {}
        self.frontier.update(problem.startState(), 0)
        self.backrefs[problem.startState()] = (None, None)

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

    def heuristic(self, state):
        # euclidean distance
        return ((state[0] - self.problem.endState()[0])**2 + (state[1] - self.problem.endState()[1])**2)**0.5
        # manhattan distance
        #return abs(state[0] - self.problem.endState()[0]) + abs(state[1] - self.problem.endState()[1])
        # return max(abs(state[0] - self.problem.endState()[0]), abs(state[1] - self.problem.endState()[1]))

    def step(self):
        problem = self.problem
        startState = problem.startState()
        frontier = self.frontier
        backrefs = self.backrefs

        if self.actions:
            return self.path(problem.endState())

        state, priority = frontier.removeMin()

        if state is None:
            return []

        self.numStatesExplored += 1
        path = self.path(state)

        if problem.isEnd(state):
            self.actions = []
            while state != startState:
                action, prevState = backrefs[state]
                self.actions.append(action)
                state = prevState
            self.actions.reverse()
            self.pathCost = self.pastCosts[problem.endState()]
            return path

        for action, newState, cost in problem.successorsAndCosts(state):
            newCost = self.pastCosts.get(state, 0) + cost
            if frontier.update(newState, newCost + self.heuristic(newState)):
                backrefs[newState] = (action, state)
                self.pastCosts[newState] = newCost

        return path