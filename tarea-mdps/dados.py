from mdp import MarkovDecisionProcess
import random
from mdp import targets


class DiceGame(MarkovDecisionProcess):
    def __init__(self, continueReward=4, exitReward=10, discount=1.0):
        super().__init__(discount)
        self.continueReward = continueReward
        self.exitReward = exitReward
        self.rules = {
            "play": {
                "continue": {
                    "play": {
                        "prob": 2/3,
                        "target": "play",
                        "reward": self.continueReward,
                    },
                    "end": {
                        "prob": 1/3,
                        "target": "end",
                        "reward": self.continueReward,
                    },
                },
                "exit": {
                    "end": {
                        "prob": 1,
                        "target": "end",
                        "reward": self.exitReward,
                    },
                },
            },
            "end": {},
        }

    def startState(self):
        return "play"

    def actions(self, state):
        if state == "play":
            return iter(["continue", "exit"])
        return iter([])

    def transitions(self, source, action):
        yield from iter(self.rules.get(source, {}).get(action, {}))

    def probability(self, source, action, target):
        return (
            self.rules.get(source, {})
            .get(action, {})
            .get(target, {"prob": 0.0})["prob"]
        )

    def reward(self, source, action, target):
        return (
            self.rules.get(source, {})
            .get(action, {})
            .get(target, {"reward": 0.0})["reward"]
        )

    def isEnd(self, state):
        return state == "end"

def episodes(mdp):
    ls = []
    state = mdp.startState()
    while not mdp.isEnd(state):
        action = random.choice(list(mdp.actions(state)))
        accProb = 0.0
        for target, prob, reward in targets(mdp, state, action):
            accProb += prob
            if random.random() < accProb:
                break
        reward = mdp.reward(state, action, target)
        ls.append([state, action, reward, target])
        state=target
    return ls

def montecarlo(episodes):
    T = {}
    N = {}
    R = {}
    for episode in episodes:
        for state, action, reward, target in episode:
            stateAction_pair = (state, action)
            if stateAction_pair not in N:
                N[stateAction_pair] = 1
            else:
                N[stateAction_pair] += 1
                
            stateAction_target_pair = (state, action, target)
            if stateAction_target_pair not in T:
                T[stateAction_target_pair] = 1
            else:
                T[stateAction_target_pair] += 1
            
            R[(state, action)] = reward
                
    probabilities = {}
    for sa_target_pair in T:
        sa_pair = (sa_target_pair[0], sa_target_pair[1])
        probabilities[sa_target_pair] = T[sa_target_pair] / N[sa_pair]
        
    return probabilities, R

mdp = DiceGame()
eps = []
for i in range(10000):
    eps.append(episodes(mdp))
prob, R = montecarlo(eps)

for state, action, next_state in sorted(prob.keys()):
    probability = prob[(state, action, next_state)]
    print("T({}, {}, {}) = {}".format(state, action, next_state, probability))

print()

for state, action in sorted(R.keys()):
    reward = R[(state, action)]
    print("R({}, {}) = {}".format(state, action, reward))