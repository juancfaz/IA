from mdp import MarkovDecisionProcess
import random
from mdp import targets

class MagicBus(MarkovDecisionProcess):
    def __init__(self, blocks, walkCost=1, busCost=2, failProb=0.5, discount=1.0):
        super().__init__(discount)
        self.blocks = blocks
        self.walkReward = -walkCost
        self.busReward = -busCost
        self.failProb = failProb

    def startState(self):
        return 1

    def actions(self, state):
        if state + 1 <= self.blocks:
            yield "walk"
        if 2 * state <= self.blocks:
            yield "bus"

    def transitions(self, source, action):
        if action == "walk":
            yield source + 1
        if action == "bus":
            yield from iter([source, 2 * source])

    def probability(self, source, action, target):
        if action == "bus":
            if source == target:
                return self.failProb
            else:
                return 1 - self.failProb
        return 1.0

    def reward(self, source, action, target):
        if action == "walk":
            return self.walkReward
        if action == "bus":
            return self.busReward

    def isEnd(self, state):
        return state == self.blocks
    
def episodes(mdp):
    ls = list()
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

def Qlearning(eps, eta, epsilon=0.1, gamma=1.0):
    
    Q = {}
    actions = ['take', 'peek', 'quit']
    
    for e in eps:
        for t in e:
            s, a, _, _ = t
            if (s, a) not in Q:
                Q[(s, a)] = 0.0
                    
    for e in eps:
        s = e[0][0]
        for t in e:
            s, a, r, s_ = t
            
            if random.random() < epsilon:
                a_ = random.choice(actions)
            else:
                Qopt = [Q.get((s, act), 0.0) for act in actions]
                maxQ = max(Qopt)
                if Qopt.count(maxQ) > 1:
                    best = [i for i in range(len(actions)) if Qopt[i] == maxQ]
                    i = random.choice(best)
                else:
                    i = Qopt.index(maxQ)
                a_ = actions[i]
                
            Q[(s, a)] = Q.get((s, a), 0.0) + eta * (r + gamma * max([Q.get((s_, act), 0.0) for act in actions]) - Q.get((s, a), 0.0))
            
            s = s_
    return Q


mdp = MagicBus(10, walkCost=1, busCost=2, failProb=0.5, discount=1.0)


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

print()
print("Q-learning")

q_values = Qlearning(eps, 0.2, epsilon=0.1, gamma=0.95)

for key, value in sorted(q_values.items()):
    print(f"{key}: {value}")
