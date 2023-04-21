import random

class BlackJackMiron():
    def __init__(self, v, multiplicity, peek_cost, threshold):
        
        self.v = v
        self.multiplicity = multiplicity
        self.peek_cost = peek_cost
        self.threshold = threshold
        
    def initialState(self):
        
        v = self.v
        v = random.sample(range(1, 14), 13)
        return v
    
    def play_game(self):
        
        v = self.initialState()
        print(v)
        print("\n")
        deck_counts = [self.multiplicity] * len(v)
        total = 0
        peek_index = []
        episode = []

        while True:
            state = [total, peek_index, list(deck_counts)]
            print(state)
            
            if total > self.threshold:
                episode.append([state, None, 0, None])
                return episode
            if not any(deck_counts):
                episode.append([state, None, 0, None])
                return episode
            
            weights = [count / sum(deck_counts) for count in deck_counts]
            action = input("Take, peek, or quit? ").strip().lower()
            
            if action == "take":
                if state[1] == []:
                    rnd_index = random.choices(range(len(v)), weights=weights)[0]
                    total += v[rnd_index]
                    deck_counts[rnd_index] -= 1
                    episode.append([state, action, 0, (total, peek_index, list(deck_counts))])
                    print(f"You drew {v[rnd_index]}")
                else:
                    if len(peek_index) <= 2:
                        total += v[peek_index[0]]
                        deck_counts[peek_index[0]] -= 1
                        episode.append([state, action, 0, (total, peek_index, list(deck_counts))])
                        print(f"You drew {v[peek_index[0]]}")
                        peek_index.pop(0)
            elif action == "peek":
                if len(peek_index) < 2:
                    rnd_index = random.choices(range(len(v)), weights=weights)[0]
                    peek_index.append(rnd_index)
                    episode.append([state, action, -self.peek_cost, (total, peek_index, list(deck_counts))])
                    print(f"You peeked {v[rnd_index]}")
                else:
                    print("You cannot peek twice in a row!")
                    episode.append([state, None, 0, None])
            elif action == "quit":
                episode.append([state, action, total, None])
                return episode
            else:
                print("Invalid action!")
    
bj = BlackJackMiron([], 4, 1, 21)
episodes = bj.play_game()
print("\n")
print(episodes)