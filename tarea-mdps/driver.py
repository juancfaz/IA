from operator import itemgetter as nth
from random import random
from mdp import targets
from camion import MagicBus

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


def noop(*args):
    return None


def run(mdp, policy, log=print):
    utility = 0.0
    state = mdp.startState()
    k = 0
    while not mdp.isEnd(state):
        action = policy(state)
        accProb = 0.0
        for target, prob, reward in targets(mdp, state, action):
            accProb += prob
            if random() < accProb:
                log(f"At {state} perform {action} to reach {target}")
                state = target
                utility += reward * mdp.discount() ** k
                break
        k += 1
    log(f"Final state {state} reached, returning utility")
    return utility


def experiment(mdp, policy, report, trials=10**4):
    utilities = {}
    average = 0.0
    for _ in range(trials):
        utility = run(mdp, policy, noop)
        average += utility
        utilities[utility] = utilities.get(utility, 0) + 1
    average /= trials
    distribution = {utility: count / trials for utility, count in utilities.items()}
    return report(distribution, average)


def plain_report(distribution, average):
    print("EXPECTED_UTILITY:", average)
    print("DISTRIBUTION:")
    print("| utility | probability |")
    print("|---------+-------------|")
    for utility, probability in sorted(distribution.items(), key=nth(1), reverse=True):
        bar = "#" * int(probability * 40)
        print(f"| {utility:^7.2f} | {probability:^11.5f} |", bar)
