class SearchAlgorithm:
    def __init__(self, problem):
        self.problem = problem
        self.startState = problem.startState()
        self.actions = None
        self.pathCost = None
        self.numStatesExplored = 0
        self.pastCosts = {}

    def stateCost(self, state):
        raise NotImplementedError("Override me")

    def step(self):
        raise NotImplementedError("Override me")
