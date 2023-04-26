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

def reachable_states(mdp):
    pending = {mdp.startState()}
    reachable = set()
    while len(pending) > 0:
        source = pending.pop()
        reachable.add(source)
        for action in mdp.actions(source):
            for target in mdp.transitions(source, action):
                if target in reachable:
                    continue
                pending.add(target)
    return reachable

def poleval(mdp, policy, n=100):
    states = reachable_states(mdp)
    v1 = {s: 0 for s in states}
    v2 = {}

    def Q(src, act):
        dis = mdp.discount()
        return sum(p * (r + dis * v1[tgt]) for tgt, p, r in targets(mdp, src, act))

    for _ in range(n):
        for s in states:
            if mdp.isEnd(s):
                v2[s] = 0
            else:
                v2[s] = Q(s, policy(s))
        v1, v2 = v2, v1
    return v1

def ValueIteration(mdp):
    V = {}
    for state in reachable_states(mdp):
        V[state] = 0

    def Q(state, action):
        return (sum(prob * ( reward + mdp.discount() * V[newState] )
                   for newState, prob, reward in targets(mdp, state, action)), action)
        
    while True:
        newV = {}
        pi = {}
        for state in reachable_states(mdp):
            if mdp.isEnd(state):
                newV[state] = 0
                pi[state] = 'None'
            else:
                newV[state], pi[state] = max(Q(state, action) for action in mdp.actions(state))
        if max(abs(newV[state] - V[state]) for state in reachable_states(mdp)) < 1e-10:
            break
        V = newV
        print('{:15} {:15} {:15}'.format('s', 'V(s)', 'pi(s)'))
        for state in reachable_states(mdp):
            print('{:15} {:15} {:15}'.format(state, V[state], pi[state]))

mdp = DiceGame()


eps = []
for i in range(100000):
    eps.append(episodes(mdp))
    
prob, R = montecarlo(eps)

print("Monte Carlo")

for state, action, next_state in sorted(prob.keys()):
    probability = prob[(state, action, next_state)]
    print("T({}, {}, {}) = {}".format(state, action, next_state, probability))

print()

for state, action in sorted(R.keys()):
    reward = R[(state, action)]
    print("R({}, {}) = {}".format(state, action, reward))

print()
print("Q-learning")

q_values = Qlearning(eps, 0.1, epsilon=0.2, gamma=0.95)

for key, value in sorted(q_values.items()):
    print(f"{key}: {value}")
