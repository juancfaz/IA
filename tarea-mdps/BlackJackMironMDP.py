import random
from typing import List, Tuple
from mdp import MarkovDecisionProcess
from mdp import targets

class BlackJackMDP(MarkovDecisionProcess):
    def __init__(self, v: List[int], multiplicity: int, peek_cost: float, threshold: int):
        self.v = v
        self.multiplicity = multiplicity
        self.peek_cost = peek_cost
        self.threshold = threshold
        
    def startState(self) -> Tuple[int, List[int], List[int]]:
        v = self.v
        v = random.sample(range(1, 14), 13)
        return (0, (), (self.multiplicity,)*len(v))
    
    def actions(self, state: Tuple[int, List[int], List[int]]) -> List[str]:
        total, peek_index, deck_counts = state
        if total > self.threshold or not any(deck_counts):
            return []
        if not peek_index or len(peek_index) == 2:
            return ["take", "peek", "quit"]
        else:
            return ["take", "quit"]
    
    def transitions(self, state: Tuple[int, Tuple[int], Tuple[int]], action: str) -> List[Tuple[int, Tuple[int], Tuple[int]]]:
        total, peek_index, deck_counts = state
        results = []
        if action == "take":
            if not peek_index:
                for i in range(len(deck_counts)):
                    if deck_counts[i] > 0:
                        new_total = total + self.v[i]
                        new_deck_counts = tuple(d - int(i == j) for j, d in enumerate(deck_counts))
                        results.append((new_total, (), new_deck_counts))
            else:
                i = peek_index[0]
                new_total = total + self.v[i]
                new_deck_counts = tuple(d - int(i == j) for j, d in enumerate(deck_counts))
                new_peek_index = tuple(peek_index[1:])
                results.append((new_total, new_peek_index, new_deck_counts))
        elif action == "peek":
            for i in range(len(deck_counts)):
                if deck_counts[i] > 0:
                    new_peek_index = tuple(list(peek_index) + [i])
                    new_deck_counts = tuple(d - int(i == j) for j, d in enumerate(deck_counts))
                    results.append((total, new_peek_index, new_deck_counts))
        elif action == "quit":
            results.append((total, (), tuple(deck_counts)))
        return results
    
    def probability(self, source: Tuple[int, List[int], List[int]], action: str, target: Tuple[int, List[int], List[int]]) -> float:
        if action == "take":
            if not source[1]:
                total, _, deck_counts = source
                i = self.v.index(target[0] - total)
                return deck_counts[i] / sum(deck_counts)
            else:
                i = source[1][0]
                return 1 if target[0] == source[0] + self.v[i] else 0
        elif action == "peek":
            if len(source[1]) == 1:
                i = source[1][0]
                return target[1] == [i] and target[2][i] == source[2][i] - 1
            elif not source[1]:
                return 1 / len(self.v)
            else:
                return 0
        elif action == "quit":
            return 1 if source == target else 0
    
    def reward(self, source: Tuple[int, List[int], List[int]], action: str, target: Tuple[int, List[int], List[int]]) -> float:
        if target[0] == 21:
            return 1
        if action == "peek":
            return -self.peek_cost
        else:
            return 0
        
    def isEnd(self, state: Tuple[int, List[int], List[int]]) -> bool:
        total, _, _ = state
        return total > self.threshold or total == 21 or not any(state[2])


mdp = BlackJackMDP([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10], 4, 1, 21)


'''
def reachable_states(mdp, n=0):
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
        if n == 100:
            break
        n += 1
    return reachable

def poleval(mdp, policy, n=100):
    states = reachable_states(mdp)
    v1 = {s: 0 for s in states}
    v2 = {}

    def Q(src, act):
        dis = mdp.discount()
        return max(sum(p * (r + dis * v1[tgt]) for tgt, p, r in targets(mdp, src, act)))

    for _ in range(n):
        for s in states:
            if mdp.isEnd(s):
                v2[s] = 0
            else:
                if policy == "take":
                    v2[s] = Q(s, "take")
        v1, v2 = v2, v1
    return v1

def always_take():
    return "take"

print(poleval(mdp, always_take))
'''

'''
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
        ls.append([state[0], action, reward, target[0]])
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



eps = []
for i in range(1000):
    eps.append(episodes(mdp))

prob, R = montecarlo(eps)

for state, action, next_state in sorted(prob.keys()):
    probability = prob[(state, action, next_state)]
    print("T({}, {}, {}) = {}".format(state, action, next_state, probability))

print()

for state, action in sorted(R.keys()):
    reward = R[(state, action)]
    print("R({}, {}) = {}".format(state, action, reward))
'''