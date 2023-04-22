import random
from typing import List, Tuple
from mdp import MarkovDecisionProcess
from mdp import targets

class BlackJackMDP(MarkovDecisionProcess):
    def __init__(self, v, multiplicity, peek_cost, threshold):
        self.v = v
        self.multiplicity = multiplicity
        self.peek_cost = peek_cost
        self.threshold = threshold
        
    def startState(self):
        v = self.v
        return (0, (), (self.multiplicity,)*len(v))
    
    def actions(self, state):
        total, peek_index, deck_counts = state
        if total > self.threshold or not any(deck_counts):
            return []
        if not peek_index or len(peek_index) == 2:
            return ["take", "peek", "quit"]
        else:
            return ["take", "quit"]
    
    def transitions(self, state, action):
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
    
    def probability(self, source, action, target):
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
    
    def reward(self, source, action, target):
        if action == "peek":
            return -self.peek_cost
        elif target[0] == 21:
            return 21
        else:
            return 0
        
    def isEnd(self, state):
        total, _, _ = state
        return total > self.threshold or total == 21 or not any(state[2])

def episodes(mdp):
    ls = list()
    state = mdp.startState()
    while not mdp.isEnd(state):
        action = random.choice(list(mdp.actions(state)))
        accProb = 0.0
        if (action == "quit" and state[0] <= 21):
            ls.append([state[0], action, state[0], state[0]])
            break
        elif (action == "quit" and state[0] > 21):
            ls.append([state[0], action, 0, state[0]])
            break
        for target, prob, reward in targets(mdp, state, action):
            accProb += prob
            if random.random() < accProb:
                break
        reward = mdp.reward(state, action, target)
        ls.append([state[0], action, reward, target[0]])
        state=target
    return ls

v = random.sample(range(1, 14), 13)
print(v)
mdp = BlackJackMDP(v, 4, 1, 21)

eps = []
for i in range(10000):
    eps.append(episodes(mdp))


def Qlearning(eps, eta, epsilon=0.1, gamma=1.0):
    # Inicializar la función de valor Q con un valor arbitrario para cada par (estado, acción).
    Q = {}
    for e in eps:
        for t in e:
            s, a, _, _ = t
            if (s, a) not in Q:
                Q[(s, a)] = 0.0

    # Para cada episodio en eps, realizar el aprendizaje Q.
    for e in eps:
        s = e[0][0]
        for t in e:
            s, a, r, s_ = t
            # Seleccionar una acción utilizando una política epsilon-greedy.
            if random.random() < epsilon:
                a_ = random.choice(['take', 'peek', 'quit'])
            else:
                Qsa = [Q.get((s, act), 0.0) for act in ['take', 'peek', 'quit']]
                maxQ = max(Qsa)
                if Qsa.count(maxQ) > 1:
                    best = [i for i in range(len(['take', 'peek', 'quit'])) if Qsa[i] == maxQ]
                    i = random.choice(best)
                else:
                    i = Qsa.index(maxQ)
                a_ = ['take', 'peek', 'quit'][i]
            # Actualizar la función de valor Q utilizando la regla de actualización Q-learning.
            Q[(s, a)] = Q.get((s, a), 0.0) + eta * (r + gamma * max([Q.get((s_, act), 0.0) for act in ['take', 'peek', 'quit']]) - Q.get((s, a), 0.0))
            # Actualizar el estado actual.
            s = s_

    return Q

q_values = Qlearning(eps, 0.01)

for key, value in q_values.items():
    print(f"{key}: {value}")
