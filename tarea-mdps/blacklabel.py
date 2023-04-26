import random, math
from mdp import MarkovDecisionProcess, targets

###############################
# MDP para el Blackjack mirón #
###############################


class BlackjackMiron(MarkovDecisionProcess):
    def __init__(self, values, multiplicity, threshold, peek_cost):
        super().__init__(1)
        self.values = values
        self.multiplicity = multiplicity
        self.threshold = threshold
        self.peek_cost = peek_cost

    def startState(self):
        return (0, None, (self.multiplicity,) * len(self.values))

    def isEnd(self, state):
        total, _, dist = state
        bust = total > self.threshold
        empty_deck = dist is None
        return bust or empty_deck

    def actions(self, state):
        if not self.isEnd(state):
            yield "take"
            if state[1] is None:
                yield "peek"
            yield "quit"

    def take(self, total, dist, i):
        ws = list(dist)
        ws[i] -= 1
        new_total = total + self.values[i]
        is_empty = sum(ws) == 0
        is_bust = new_total > self.threshold
        new_dist = None if is_bust or is_empty else tuple(ws)
        return (new_total, None, new_dist)

    def transitions(self, source, action):
        total, peek_index, dist = source
        if dist is None:
            return
        n = len(dist)
        take = self.take
        if action == "quit":
            yield (total, None, None)
        elif action == "take" and peek_index is None:
            yield from (take(total, dist, i) for i in range(n) if dist[i] > 0)
        elif action == "take":
            yield take(total, dist, peek_index)
        elif action == "peek" and peek_index is None:
            yield from [(total, i, dist) for i in range(n) if dist[i] > 0]

    def probability(self, source, action, target):
        if action == "quit":
            return 1
        if action == "take":
            if source[1] is not None:
                return 1
            i = self.values.index(target[0] - source[0])
            return source[2][i] / sum(source[2])
        if action == "peek":
            return source[2][target[1]] / sum(source[2])
        return 1

    def reward(self, source, action, target):
        if action == "quit":
            return target[0]
        if action == "peek":
            return -self.peek_cost
        if target[0] > self.threshold:
            return 0
        if target[2] is None:
            return target[0]
        return 0


##############################
# Jugando al Blackjack mirón #
##############################


def play_blackjack(mdp, log, prompt, report):
    state = mdp.startState()
    episode = []
    while not mdp.isEnd(state):
        log(mdp, state)
        action = prompt(mdp, state)
        acc_prob = 0
        for target, prob, reward in targets(mdp, state, action):
            acc_prob += prob
            if random.random() < acc_prob:
                episode.append([state[0], action, reward, target[0]])
                state = target
                break
    return report(mdp, episode)


# Blackjack plano


def plain_log(mdp, state):
    print(state)
    return


def plain_prompt(mdp, state):
    return input("Choose an action: ")


def plain_report(mdp, episode):
    return print(episode)


def play_plain_blackjack():
    return play_blackjack(
        mdp=BlackjackMiron(
            values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
            multiplicity=4,
            threshold=21,
            peek_cost=-1,
        ),
        log=plain_log,
        prompt=plain_prompt,
        report=plain_report,
    )


# Blackjack fancy

def fancy_log(mdp, state):
    total, peek_index, dist = state
    print(f"   HAND VALUE :: {total}")
    print(f" PEEKED VALUE :: {None if peek_index is None else mdp.values[peek_index]}")
    print("REMAINING CARDS :: {")
    for i, n in enumerate(dist):
        print(f"    {mdp.values[i]} => {n} left,")
    print("}")
    return


def fancy_prompt(mdp, state):
    valid_actions = list(mdp.actions(state))
    while True:
        print("Choose an action...")
        for i, action in enumerate(valid_actions):
            print(f"{i}. {action}")
        action = input(f"[{valid_actions[0]}] > ").strip()
        if action == "":
            action = valid_actions[0]
        if action.isdigit() and int(action) < len(valid_actions):
            action = valid_actions[int(action)]
        if action in mdp.actions(state):
            return action
        print(f"Action {action} is not valid! Try again...")


def fancy_report(mdp, episode):
    utility = 0
    for i in range(2, len(episode), 3):
        reward = episode[i]
        utility += reward
    print(f"\nGame finished!")
    print(f"   HAND VALUE :: {episode[-1][0]}")
    print(f"  FINAL SCORE :: {utility}")


def play_fancy_blackjack():
    return play_blackjack(
        mdp=BlackjackMiron(
            values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
            multiplicity=4,
            threshold=21,
            peek_cost=-1,
        ),
        log=fancy_log,
        prompt=fancy_prompt,
        report=fancy_report,
    )


# Blackjack simulado con acciones aleatorias


def noop(*args):
    return None


def play_random_blackjack(
    mdp=BlackjackMiron(
        values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        multiplicity=4,
        threshold=21,
        peek_cost=-1,
    )
):
    return play_blackjack(
        mdp,
        log=noop,
        prompt=lambda mdp, state: random.choice(list(mdp.actions(state))),
        report=lambda mdp, episode: episode,
    )

def Qlearning(eps, eta, epsilon=0.1, gamma=1.0):
    
    Q = {}
    actions = ['take', 'peek', 'quit']
    numUpdates = 0
    
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
            numUpdates += 1
            epsilon = 1.0 / math.sqrt(numUpdates)
            s = s_
    return Q

def SARSA(eps, eta, gamma):
    for episode in eps:
        for i, transition in enumerate(episode):
            if i < len(episode)-1:
                transition.append(episode[i+1][1])
            else:
                transition.append(None)
            
    Q = {}
    
    for e in eps:
        for t in e:
            s, a, r, s_, a_ = t
            if (s, a) not in Q:
                Q[(s, a)] = 0.0
    
    for e in eps:
        s = e[0][0]
        a = e[0][1]
        for t in e:
            s, a, r, s_, a_ = t
            Q[(s, a)] = Q.get((s, a), 0.0) + eta * (r + gamma * Q.get((s_, a_), 0.0) - Q.get((s, a), 0.0))
            s = s_
            a = a_
    
    return Q

def utility(eps, eta):
    Q = {}
    numUpdates = 0
    
    for e in eps:
        for t in e:
            s, a, r, s_ = t
            if (s, a) not in Q:
                Q[(s, a)] = 0.0
                
    def utility_episode(e):
        utility = 0
        for i in range(2, len(e), 3):
            reward = e[i][2]
            utility += reward
        return utility
    
    for e in eps:
        for t in e:
            s, a, r, s_ = t
            Q[(s, a)] = (1 - eta)*Q.get((s, a), 0.0) + eta * utility_episode(e)
            numUpdates += 1
            eta = 1.0 / math.sqrt(numUpdates)
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
            print(state, V[state], pi[state])

mdp=BlackjackMiron(
        values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        multiplicity=4,
        threshold=21,
        peek_cost=-1,
    )

# Policy Evaluation take quit peek
print("Policy Evaluation")
policy = lambda s: 'quit' if s[0] < 10000 else 'peek'
print(poleval(mdp, policy))

'''
eps = []
for i in range(100000):
    eps.append(play_random_blackjack())

# Q-learning
print("Q-learning")
for key, value in sorted(Qlearning(eps, 0.2, epsilon=0.1, gamma=0.95).items()):
    print(f"{key}: {value}")

# SARSA
print("SARSA")
for key, value in sorted(SARSA(eps, 0.1, 0.95).items()):
    print(f"{key}: {value}")

# Utility
print("Utility")
for key, value in sorted(utility(eps, 0.1).items()):
    print(f"{key}: {value}")
'''